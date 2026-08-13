from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Services\AudioDeviceService.cs")
text = p.read_text(encoding="utf-8")
old = '''    private static string? TryGetDefaultId(IMMDeviceEnumerator enumerator, EDataFlow flow, ERole role)
    {
        var hr = enumerator.GetDefaultAudioEndpoint(flow, role, out var device);
        if (hr < 0 || device is null)
        {
            return null;
        }

        try
        {
            device.GetId(out var id);
            return id;
        }
        finally
        {
            Marshal.ReleaseComObject(device);
        }
    }
'''
new = '''    private static string? TryGetDefaultId(IMMDeviceEnumerator enumerator, EDataFlow flow, ERole role)
    {
        _ = enumerator;
        return MmDeviceNative.GetDefaultId(flow, role);
    }
'''
if old not in text:
    raise SystemExit("TryGetDefaultId not found")
p.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
print("patched defaults")
