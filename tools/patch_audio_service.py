from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Services\AudioDeviceService.cs")
text = p.read_text(encoding="utf-8")
old = '''        try
        {
            var dataFlow = flow == AudioFlow.Playback ? EDataFlow.eRender : EDataFlow.eCapture;
            HResult.ThrowIfFailed(
                enumerator.EnumAudioEndpoints(dataFlow, 0x0000000F, out var collection),
                "Unable to enumerate audio endpoints.");

            collection.GetCount(out var count);
            var defaults = GetDefaultIds(enumerator, dataFlow);
            var devices = new List<AudioDeviceInfo>((int)count);
            for (uint i = 0; i < count; i++)
            {
                collection.Item(i, out var device);
                try
                {
                    var info = ToDeviceInfo(device, flow, defaults);
                    if (info is not null)
                    {
                        devices.Add(info);
                    }
                }
                finally
                {
                    Marshal.ReleaseComObject(device);
                }
            }

            Marshal.ReleaseComObject(collection);
            return devices
                .OrderBy(d => d.Availability != DeviceAvailability.Available)
                .ThenBy(d => d.Name, StringComparer.CurrentCultureIgnoreCase)
                .ToList();
        }
'''
new = '''        try
        {
            var dataFlow = flow == AudioFlow.Playback ? EDataFlow.eRender : EDataFlow.eCapture;
            var defaults = GetDefaultIds(enumerator, dataFlow);
            var raw = MmDeviceNative.Enumerate(dataFlow);
            var devices = raw.Select(device => ToDeviceInfo(device, flow, defaults)).ToList();
            return devices
                .OrderBy(d => d.Availability != DeviceAvailability.Available)
                .ThenBy(d => d.Name, StringComparer.CurrentCultureIgnoreCase)
                .ToList();
        }
'''
if old not in text:
    raise SystemExit("enumerate block not found")
text = text.replace(old, new, 1)

old = '''            PolicyConfigSwitcher.SetDefaultEndpoint(device.Id, roles);
'''
new = '''            MmDeviceNative.SetDefaultEndpoint(device.Id, roles);
'''
if old not in text:
    raise SystemExit("set default not found")
text = text.replace(old, new, 1)

old = '''    private static AudioDeviceInfo? ToDeviceInfo(IMMDevice device, AudioFlow flow, DefaultIds defaults)
    {
        device.GetId(out var id);
        device.GetState(out var state);
        var name = ReadFriendlyName(device) ?? id;
        var availability = state switch
'''
new = '''    private static AudioDeviceInfo ToDeviceInfo(MmDeviceNative.RawDevice device, AudioFlow flow, DefaultIds defaults)
    {
        var id = device.Id;
        var state = device.State;
        var name = device.Name;
        var availability = state switch
'''
if old not in text:
    raise SystemExit("ToDeviceInfo not found")
text = text.replace(old, new, 1)
p.write_text(text, encoding="utf-8", newline="\n")
print("patched audio service")
