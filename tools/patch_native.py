from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Interop\NativeMethods.cs")
text = p.read_text(encoding="utf-8")
needle = "    public const uint ClsctxInprocServer = 1;"
insert = """    public const uint ClsctxInprocServer = 1;
    public const int AttachParentProcess = -1;
    public const uint CoInitApartmentThreaded = 0x2;

    [DllImport("kernel32.dll")]
    public static extern bool AttachConsole(int dwProcessId);

    [DllImport("ole32.dll")]
    public static extern int CoInitializeEx(nint pvReserved, uint dwCoInit);
"""
if needle not in text:
    raise SystemExit("clsctx not found")
if "AttachConsole" not in text:
    text = text.replace(needle, insert, 1)
    p.write_text(text, encoding="utf-8", newline="\n")
print("patched native methods")
