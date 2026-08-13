from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Interop\NativeMethods.cs")
t = p.read_text(encoding="utf-8")
old = '''    [DllImport("ole32.dll")]
    public static extern int CoInitializeEx(nint pvReserved, uint dwCoInit);
'''
new = '''    [DllImport("ole32.dll")]
    public static extern int CoInitializeEx(nint pvReserved, uint dwCoInit);

    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    public static extern nint LoadLibrary(string lpFileName);
'''
if old not in t:
    raise SystemExit("NativeMethods marker not found")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("updated NativeMethods")
