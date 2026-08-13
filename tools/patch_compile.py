from pathlib import Path
import re
root = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles")

p = root / "Program.cs"
text = p.read_text(encoding="utf-8")
text = text.replace("Application.Start(_ =>", "Application.Start(p =>")
text = text.replace("            _ = new App();", "            new App();")
p.write_text(text, encoding="utf-8", newline="\n")

p = root / "MainWindow.xaml.cs"
text = p.read_text(encoding="utf-8")
text = text.replace("    private bool _forceClose;\n    private bool _hiddenStart;\n\n", "")
text = text.replace("        _hiddenStart = true;\n        AppWindow.Hide();", "        AppWindow.Hide();")
text = text.replace("        _forceClose = true;\n        SaveBounds();", "        SaveBounds();")
p.write_text(text, encoding="utf-8", newline="\n")

p = root / "Views/ProfilesPage.xaml.cs"
text = p.read_text(encoding="utf-8")
text = re.sub(r"string\.Join\(\".*?\", missing\)", "string.Join(\" · \", missing)", text)
p.write_text(text, encoding="utf-8", newline="\n")
print("compile fixes written")
