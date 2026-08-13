from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Views\EditProfilePage.xaml")
t = p.read_text(encoding="utf-8")
t = t.replace('<FontIcon HorizontalAlignment="Center" FontSize="20" Glyph="{Binding Glyph}" />',
              '<FontIcon HorizontalAlignment="Center" Glyph="{Binding Glyph}" />')
t = t.replace('<StackPanel Width="84" Padding="6" Spacing="4">',
              '<StackPanel Width="72" Padding="4" Spacing="2">')
p.write_text(t, encoding="utf-8")
print("updated EditProfilePage.xaml")
