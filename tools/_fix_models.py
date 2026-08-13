from pathlib import Path

path = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Models\AppModels.cs")
text = path.read_text(encoding="utf-8")
old = """    public bool LaunchMinimized { get; set; }
    public string? LastActivatedProfileId { get; set; }"""
new = """    public bool LaunchMinimized { get; set; }
    public bool WriteDetailedLogs { get; set; }
    public string? LastActivatedProfileId { get; set; }"""
if old not in text:
    raise SystemExit("AppModels marker not found")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("updated AppModels")
