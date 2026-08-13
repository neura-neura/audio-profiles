from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\AudioProfiles.csproj")
text = p.read_text(encoding="utf-8")
old = "    <None Remove=\"Strings\\**\\*.resw\" />"
new = """    <None Remove="Strings\**\*.resw" />
    <PRIResource Remove="Strings\**\*.resw" />
    <EmbeddedResource Remove="Strings\**\*.resw" />"""
if old not in text:
    raise SystemExit("resw remove not found: " + repr(text[text.find("Strings")-80:text.find("Strings")+120] if "Strings" in text else "no strings"))
text = text.replace(old, new, 1)
p.write_text(text, encoding="utf-8", newline="\n")
print("patched csproj")
