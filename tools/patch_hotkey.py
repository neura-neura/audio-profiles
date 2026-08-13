from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Services\HotkeyService.cs")
text = p.read_text(encoding="utf-8")
old = '''    private readonly AppLog _log;
    private readonly Dictionary<int, string> _hotkeyIds = [];
    private nint _hwnd;
    private NativeMethods.WndProc? _wndProc;
    private nint _classAtom;
    private bool _disposed;
'''
new = '''    private readonly AppLog _log;
    private readonly Dictionary<int, string> _hotkeyIds = [];
    private IReadOnlyList<AudioProfile> _profiles = [];
    private nint _hwnd;
    private NativeMethods.WndProc? _wndProc;
    private nint _classAtom;
    private bool _disposed;
'''
if old not in text:
    raise SystemExit("fields not found")
text = text.replace(old, new, 1)

old = '''    public void RegisterProfiles(IEnumerable<AudioProfile> profiles)
    {
        UnregisterAll();
'''
new = '''    public void RegisterProfiles(IEnumerable<AudioProfile> profiles)
    {
        _profiles = profiles.ToList();
        UnregisterAll();
'''
if old not in text:
    raise SystemExit("register method not found")
text = text.replace(old, new, 1)

old = '''        const int probeId = 0x7FFE;
        if (!NativeMethods.RegisterHotKey(_hwnd, probeId, modifiers, (uint)binding.VirtualKey))
        {
            errorKey = "ShortcutInUse";
            return false;
        }

        NativeMethods.UnregisterHotKey(_hwnd, probeId);
        return true;
'''
new = '''        UnregisterAll();
        const int probeId = 0x7FFE;
        try
        {
            if (!NativeMethods.RegisterHotKey(_hwnd, probeId, modifiers, (uint)binding.VirtualKey))
            {
                errorKey = "ShortcutInUse";
                return false;
            }

            NativeMethods.UnregisterHotKey(_hwnd, probeId);
            return true;
        }
        finally
        {
            RegisterProfiles(_profiles);
        }
'''
if old not in text:
    raise SystemExit("probe block not found")
text = text.replace(old, new, 1)
p.write_text(text, encoding="utf-8", newline="\n")
print("patched hotkeys")
