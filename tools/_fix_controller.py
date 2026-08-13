from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Services\AppController.cs")
t = p.read_text(encoding="utf-8")
old = """    public async Task InitializeAsync()
    {
        Log.Info("Application startup.");
        Notifications.Initialize();
"""
new = """    public async Task InitializeAsync()
    {
        Log.Info("Application startup.");
        Log.Verbose = Settings.WriteDetailedLogs;
        Notifications.Initialize();
"""
if old not in t:
    raise SystemExit("controller marker not found")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("updated AppController")
