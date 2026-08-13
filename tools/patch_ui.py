from pathlib import Path

root = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles")

p = root / "Views/ProfilesPage.xaml.cs"
text = p.read_text(encoding="utf-8")
if "using Microsoft.UI.Xaml.Automation;" not in text:
    text = text.replace(
        "using Microsoft.UI.Xaml;",
        "using Microsoft.UI.Xaml;\nusing Microsoft.UI.Xaml.Automation;",
    )
text = text.replace("Â·", "·")
p.write_text(text, encoding="utf-8", newline="\n")

p = root / "Views/EditProfilePage.xaml.cs"
text = p.read_text(encoding="utf-8")
if "using Microsoft.UI.Xaml.Automation;" not in text:
    text = text.replace(
        "using Microsoft.UI.Xaml;",
        "using Microsoft.UI.Xaml;\nusing Microsoft.UI.Xaml.Automation;",
    )
p.write_text(text, encoding="utf-8", newline="\n")

p = root / "Helpers/StringCatalog.cs"
text = p.read_text(encoding="utf-8")
text = text.replace("couldn''t", "couldn't")
text = text.replace("can''t", "can't")
p.write_text(text, encoding="utf-8", newline="\n")

print("patched pages and strings")
