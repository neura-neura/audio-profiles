from pathlib import Path
Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Interop\MmDeviceNative.cs").write_text(r'''using System.Runtime.InteropServices;
using AudioProfiles.Models;

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

    public static IReadOnlyList<RawDevice> Enumerate(EDataFlow flow)
    {
        var enumerator = CreateEnumerator();
        if (enumerator == nint.Zero)
        {
            return [];
        }

        try
        {
            var enumFn = GetSlot<EnumAudioEndpoints>(enumerator, 3);
            nint collection;
            var hr = enumFn(enumerator, (int)flow, 0x0000000F, &collection);
            if (hr < 0 || collection == nint.Zero)
            {
                return [];
            }

            try
            {
                var getCount = GetSlot<GetCount>(collection, 3);
                uint count;
                HResult.ThrowIfFailed(getCount(collection, &count), "IMMDeviceCollection.GetCount failed.");
                var item = GetSlot<CollectionItem>(collection, 4);
                var devices = new List<RawDevice>((int)count);
                for (uint i = 0; i < count; i++)
                {
                    nint device;
                    if (item(collection, i, &device) < 0 || device == nint.Zero)
                    {
                        continue;
                    }

                    try
                    {
                        var parsed = ReadDevice(device);
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

    public static string? GetDefaultId(EDataFlow flow, ERole role)
    {
        var enumerator = CreateEnumerator();
        if (enumerator == nint.Zero)
        {
            return null;
        }

        try
        {
            var getDefault = GetSlot<GetDefaultAudioEndpoint>(enumerator, 4);
            nint device;
            if (getDefault(enumerator, (int)flow, (int)role, &device) < 0 || device == nint.Zero)
            {
                return null;
            }

            try
            {
                return ReadDevice(device)?.Id;
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

    public static void SetDefaultEndpoint(string deviceId, ERole[] roles)
    {
        Exception? last = null;
        foreach (var iid in PolicyIids)
        {
            var localIid = iid;
            var clsid = PolicyClsid;
            var hr = NativeMethods.CoCreateInstance(ref clsid, nint.Zero, NativeMethods.ClsctxInprocServer, ref localIid, out var ptr);
            if (hr < 0 || ptr == nint.Zero)
            {
                continue;
            }

            try
            {
                var setDefault = GetSlot<SetDefaultEndpoint>(ptr, 13);
                foreach (var role in roles)
                {
                    var result = setDefault(ptr, deviceId, (int)role);
                    HResult.ThrowIfFailed(result, "PolicyConfig.SetDefaultEndpoint failed.");
                }

                return;
            }
            catch (Exception ex)
            {
                last = ex;
            }
            finally
            {
                Release(ptr);
            }
        }

        throw last ?? new COMException("Windows refused to change the default audio device.", HResult.EFail);
    }

    private static RawDevice? ReadDevice(nint device)
    {
        var getId = GetSlot<GetId>(device, 5);
        var getState = GetSlot<GetState>(device, 6);
        nint idPtr;
        if (getId(device, &idPtr) < 0 || idPtr == nint.Zero)
        {
            return null;
        }

        try
        {
            uint state;
            getState(device, &state);
            var id = Marshal.PtrToStringUni(idPtr) ?? string.Empty;
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
            var key = PropertyKey.PkeyDeviceFriendlyName;
            PropVariant value = default;
            if (getValue(store, &key, &value) < 0)
            {
                return null;
            }

            try
            {
                return value.GetString();
            }
            finally
            {
                value.Clear();
            }
        }
        finally
        {
            Release(store);
        }
    }

    private static nint CreateEnumerator()
    {
        var clsid = EnumeratorClsid;
        var iid = EnumeratorIid;
        var hr = NativeMethods.CoCreateInstance(ref clsid, nint.Zero, NativeMethods.ClsctxInprocServer, ref iid, out var ptr);
        return hr < 0 ? nint.Zero : ptr;
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

        var release = GetSlot<Release>(comObject, 2);
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
    private delegate int SetDefaultEndpoint(nint self, [MarshalAs(UnmanagedType.LPWStr)] string deviceId, int role);

    [UnmanagedFunctionPointer(CallingConvention.StdCall)]
    private delegate uint Release(nint self);

    internal readonly record struct RawDevice(string Id, string Name, uint State);
}
''', encoding='utf-8', newline='\n')
print('wrote MmDeviceNative.cs')
