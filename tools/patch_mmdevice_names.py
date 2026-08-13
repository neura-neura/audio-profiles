from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Interop\MmDeviceNative.cs")
text = p.read_text(encoding="utf-8")
text = text.replace("GetSlot<SetDefaultEndpoint>(ptr, 13)", "GetSlot<SetDefaultEndpointFn>(ptr, 13)")
text = text.replace("private delegate int SetDefaultEndpoint(nint self, [MarshalAs(UnmanagedType.LPWStr)] string deviceId, int role);", "private delegate int SetDefaultEndpointFn(nint self, [MarshalAs(UnmanagedType.LPWStr)] string deviceId, int role);")
text = text.replace("var release = GetSlot<Release>(comObject, 2);", "var release = GetSlot<ReleaseFn>(comObject, 2);")
text = text.replace("private delegate uint Release(nint self);", "private delegate uint ReleaseFn(nint self);")
p.write_text(text, encoding="utf-8", newline="\n")
print("renamed delegates")
