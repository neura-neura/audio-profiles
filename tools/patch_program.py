from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Program.cs")
text = p.read_text(encoding="utf-8")
if "using AudioProfiles.Interop;" not in text:
    text = text.replace("using AudioProfiles.Services;", "using AudioProfiles.Interop;\nusing AudioProfiles.Services;")
old = '''        if (args.Any(a => string.Equals(a, "--self-test", StringComparison.OrdinalIgnoreCase)))
        {
            Environment.ExitCode = AudioSelfTest.Run() ? 0 : 1;
            return;
        }
'''
new = '''        if (args.Any(a => string.Equals(a, "--self-test", StringComparison.OrdinalIgnoreCase)))
        {
            NativeMethods.AttachConsole(NativeMethods.AttachParentProcess);
            Environment.ExitCode = AudioSelfTest.Run() ? 0 : 1;
            return;
        }
'''
if old not in text:
    raise SystemExit("self-test block not found")
p.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
print("patched program")
