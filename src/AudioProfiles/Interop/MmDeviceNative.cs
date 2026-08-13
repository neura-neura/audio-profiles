using System.Runtime.InteropServices;
using AudioProfiles.Services;

namespace AudioProfiles.Interop;

/// <summary>
/// Raw IUnknown vtable calls for MMDevice and PolicyConfig.
/// WinUI / CsWinRT ComWrappers break classic [ComImport] casts for some Core Audio interfaces.
/// </summary>
internal static unsafe class MmDeviceNative
{
    private static readonly Guid EnumeratorClsid = CoreAudioConstants.MMDeviceEnumeratorClsid;
    private static readonly Guid EnumeratorIid = CoreAudioConstants.ImmDeviceEnumeratorIid;
    private static readonly Guid PolicyClsid = CoreAudioConstants.PolicyConfigClientClsid;
    private static readonly Guid[] PolicyIids =
    [
        CoreAudioConstants.IPolicyConfigIid,
        CoreAudioConstants.IPolicyConfig10Iid,
        CoreAudioConstants.IPolicyConfigVistaIid
    ];

    public static IReadOnlyList<RawDevice> Enumerate(EDataFlow flow, AppLog? log = null)
    {
        var enumerator = CreateEnumerator(log);
        if (enumerator == nint.Zero)
        {
            return [];
        }

        try
        {
            var enumFn = GetSlot<EnumAudioEndpoints>(enumerator, 3);
            nint collection;
            var hr = enumFn(enumerator, (int)flow, CoreAudioConstants.DeviceStateMaskAll, &collection);
            if (hr < 0)
            {
                log?.Error($"EnumAudioEndpoints failed for {flow}. HRESULT=0x{hr:X8}");
                return [];
            }

            if (collection == nint.Zero)
            {
                log?.Warn($"EnumAudioEndpoints returned no collection for {flow}.");
                return [];
            }

            try
            {
                var getCount = GetSlot<GetCount>(collection, 3);
                uint count;
                var countHr = getCount(collection, &count);
                if (countHr < 0)
                {
                    log?.Error($"IMMDeviceCollection.GetCount failed. HRESULT=0x{countHr:X8}");
                    return [];
                }

                var item = GetSlot<CollectionItem>(collection, 4);
                var devices = new List<RawDevice>((int)count);
                for (uint i = 0; i < count; i++)
                {
                    nint device;
                    var itemHr = item(collection, i, &device);
                    if (itemHr < 0 || device == nint.Zero)
                    {
                        log?.Warn($"IMMDeviceCollection.Item({i}) failed. HRESULT=0x{itemHr:X8}");
                        continue;
                    }

                    try
                    {
                        var parsed = ReadDevice(device, log);
                        if (parsed is not null)
                        {
                            devices.Add(parsed.Value);
                        }
                    }
                    finally
                    {
                        Release(device);
                    }
                }

                return devices;
            }
            finally
            {
                Release(collection);
            }
        }
        finally
        {
            Release(enumerator);
        }
    }

    public static string? GetDefaultId(EDataFlow flow, ERole role, AppLog? log = null)
    {
        var enumerator = CreateEnumerator(log);
        if (enumerator == nint.Zero)
        {
            return null;
        }

        try
        {
            var getDefault = GetSlot<GetDefaultAudioEndpoint>(enumerator, 4);
            nint device;
            var hr = getDefault(enumerator, (int)flow, (int)role, &device);
            if (hr < 0 || device == nint.Zero)
            {
                if (hr != HResult.ENotFound)
                {
                    log?.Warn($"GetDefaultAudioEndpoint({flow},{role}) failed. HRESULT=0x{hr:X8}");
                }

                return null;
            }

            try
            {
                return ReadDevice(device, log)?.Id;
            }
            finally
            {
                Release(device);
            }
        }
        finally
        {
            Release(enumerator);
        }
    }

    public static void SetDefaultEndpoint(string deviceId, ERole[] roles, AppLog? log = null)
    {
        Exception? last = null;
        foreach (var iid in PolicyIids)
        {
            var localIid = iid;
            var clsid = PolicyClsid;
            var createHr = NativeMethods.CoCreateInstance(
                ref clsid,
                nint.Zero,
                NativeMethods.ClsctxInprocServer,
                ref localIid,
                out var ptr);
            if (createHr < 0 || ptr == nint.Zero)
            {
                log?.Warn($"PolicyConfig CoCreateInstance({iid}) failed. HRESULT=0x{createHr:X8}");
                continue;
            }

            try
            {
                var setDefault = GetSlot<SetDefaultEndpointFn>(ptr, 13);
                foreach (var role in roles)
                {
                    var result = setDefault(ptr, deviceId, (int)role);
                    if (result < 0)
                    {
                        throw Marshal.GetExceptionForHR(result)
                            ?? new COMException($"PolicyConfig.SetDefaultEndpoint failed for role {role}.", result);
                    }
                }

                return;
            }
            catch (Exception ex)
            {
                last = ex;
                log?.Warn($"PolicyConfig.SetDefaultEndpoint via {iid} failed: {ex.Message}");
            }
            finally
            {
                Release(ptr);
            }
        }

        throw last ?? new COMException("Windows refused to change the default audio device.", HResult.EFail);
    }

    public static nint CreateNotificationEnumerator(AppLog? log = null) => CreateEnumerator(log);

    public static int RegisterNotifications(nint enumerator, nint client)
    {
        if (enumerator == nint.Zero || client == nint.Zero)
        {
            return HResult.EPointer;
        }

        var register = GetSlot<RegisterNotificationsFn>(enumerator, 6);
        return register(enumerator, client);
    }

    public static int UnregisterNotifications(nint enumerator, nint client)
    {
        if (enumerator == nint.Zero || client == nint.Zero)
        {
            return HResult.EPointer;
        }

        var unregister = GetSlot<UnregisterNotificationsFn>(enumerator, 7);
        return unregister(enumerator, client);
    }

    public static void ReleaseCom(nint comObject) => Release(comObject);

    private static RawDevice? ReadDevice(nint device, AppLog? log)
    {
        var getId = GetSlot<GetId>(device, 5);
        var getState = GetSlot<GetState>(device, 6);
        nint idPtr;
        var idHr = getId(device, &idPtr);
        if (idHr < 0 || idPtr == nint.Zero)
        {
            log?.Warn($"IMMDevice.GetId failed. HRESULT=0x{idHr:X8}");
            return null;
        }

        try
        {
            uint state = 0;
            getState(device, &state);
            var id = Marshal.PtrToStringUni(idPtr) ?? string.Empty;
            if (string.IsNullOrWhiteSpace(id))
            {
                return null;
            }

            return new RawDevice(id, ReadFriendlyName(device) ?? id, state);
        }
        finally
        {
            Marshal.FreeCoTaskMem(idPtr);
        }
    }

    private static string? ReadFriendlyName(nint device)
    {
        var openStore = GetSlot<OpenPropertyStore>(device, 4);
        nint store;
        if (openStore(device, CoreAudioConstants.StgmRead, &store) < 0 || store == nint.Zero)
        {
            return null;
        }

        try
        {
            var getValue = GetSlot<GetPropertyValue>(store, 5);
            foreach (var keySource in new[] { PropertyKey.PkeyDeviceFriendlyName, PropertyKey.PkeyDeviceDescription })
            {
                var key = keySource;
                PropVariant value = default;
                if (getValue(store, &key, &value) < 0)
                {
                    continue;
                }

                try
                {
                    var name = value.GetString();
                    if (!string.IsNullOrWhiteSpace(name))
                    {
                        return name;
                    }
                }
                finally
                {
                    value.Clear();
                }
            }

            return null;
        }
        finally
        {
            Release(store);
        }
    }

    private static nint CreateEnumerator(AppLog? log)
    {
        var clsid = EnumeratorClsid;
        var iid = EnumeratorIid;
        var hr = NativeMethods.CoCreateInstance(
            ref clsid,
            nint.Zero,
            NativeMethods.ClsctxInprocServer,
            ref iid,
            out var ptr);
        if (hr < 0 || ptr == nint.Zero)
        {
            log?.Error($"MMDeviceEnumerator CoCreateInstance failed. HRESULT=0x{hr:X8}");
            return nint.Zero;
        }

        return ptr;
    }

    private static T GetSlot<T>(nint comObject, int index) where T : Delegate
    {
        var vtbl = *(nint**)comObject;
        return Marshal.GetDelegateForFunctionPointer<T>(vtbl[index]);
    }

    private static void Release(nint comObject)
    {
        if (comObject == nint.Zero)
        {
            return;
        }

        var release = GetSlot<ReleaseFn>(comObject, 2);
        release(comObject);
    }

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int EnumAudioEndpoints(nint self, int dataFlow, uint stateMask, nint* collection);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int GetDefaultAudioEndpoint(nint self, int dataFlow, int role, nint* device);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int GetCount(nint self, uint* count);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int CollectionItem(nint self, uint index, nint* device);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int OpenPropertyStore(nint self, uint access, nint* store);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int GetId(nint self, nint* id);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int GetState(nint self, uint* state);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int GetPropertyValue(nint self, PropertyKey* key, PropVariant* value);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int SetDefaultEndpointFn(nint self, [MarshalAs(UnmanagedType.LPWStr)] string deviceId, int role);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int RegisterNotificationsFn(nint self, nint client);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate int UnregisterNotificationsFn(nint self, nint client);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate uint ReleaseFn(nint self);

    internal readonly record struct RawDevice(string Id, string Name, uint State);
}
