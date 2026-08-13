from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Interop\CoreAudioInterop.cs")
text = p.read_text(encoding="utf-8")
old = "internal static class PolicyConfigSwitcher"
new = "// Windows has no public API to set the default endpoint. PolicyConfigClient is the COM object used by the Sound control panel.\ninternal static class PolicyConfigSwitcher"
if old not in text:
    raise SystemExit("policy class not found")
p.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
print("patched policy comment")
