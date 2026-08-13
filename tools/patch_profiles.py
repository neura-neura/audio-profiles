from pathlib import Path

xaml = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Views\ProfilesPage.xaml")
text = xaml.read_text(encoding="utf-8")
old = '''                                    <Button
                                        MinHeight="44"
                                        Click="EditButton_Click"
                                        Content="{x:Bind EditLabel}"
                                        Tag="{x:Bind Id}" />
'''
new = '''                                    <Button
                                        MinHeight="44"
                                        Click="EditButton_Click"
                                        Content="{x:Bind ActionLabel}"
                                        Tag="{x:Bind Id}" />
'''
if old not in text:
    raise SystemExit("edit button not found")
xaml.write_text(text.replace(old, new), encoding="utf-8", newline="\n")

cs = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Views\ProfilesPage.xaml.cs")
text = cs.read_text(encoding="utf-8")
old = '''            EditLabel = Loc.Get("Edit"),
            DeleteLabel = Loc.Get("Delete"),
'''
new = '''            EditLabel = Loc.Get("Edit"),
            ActionLabel = missing.Count == 0 ? Loc.Get("Edit") : Loc.Get("Change"),
            DeleteLabel = Loc.Get("Delete"),
'''
if old not in text:
    raise SystemExit("card labels not found")
cs.write_text(text.replace(old, new), encoding="utf-8", newline="\n")

model = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Models\ProfileCard.cs")
text = model.read_text(encoding="utf-8")
if "ActionLabel" not in text:
    text = text.replace("    public required string EditLabel { get; init; }\n", "    public required string EditLabel { get; init; }\n    public required string ActionLabel { get; init; }\n")
    model.write_text(text, encoding="utf-8", newline="\n")
print("patched profile change action")
