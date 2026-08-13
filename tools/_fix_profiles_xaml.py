from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Views\ProfilesPage.xaml")
t = p.read_text(encoding="utf-8")
t = t.replace('<FontIcon FontSize="32" Glyph="&#xE8D6;" Foreground="{StaticResource BrandTealBrush}" />',
              '<FontIcon FontSize="24" Glyph="&#xE8D6;" Foreground="{StaticResource BrandTealBrush}" />')
t = t.replace('Padding="16"', 'Padding="12"')
t = t.replace('''                                <Border
                                    Width="40"
                                    Height="40"
                                    Background="{StaticResource BrandTealBrush}"
                                    CornerRadius="10">
                                    <FontIcon
                                        HorizontalAlignment="Center"
                                        VerticalAlignment="Center"
                                        FontSize="18"
                                        Foreground="White"
                                        Glyph="{Binding Glyph}" />
                                </Border>''',
              '''                                <Border
                                    Width="32"
                                    Height="32"
                                    Background="{StaticResource BrandTealBrush}"
                                    CornerRadius="8">
                                    <FontIcon
                                        HorizontalAlignment="Center"
                                        VerticalAlignment="Center"
                                        FontSize="16"
                                        Foreground="White"
                                        Glyph="{Binding Glyph}" />
                                </Border>''')
t = t.replace('<TextBlock FontSize="16" FontWeight="SemiBold" Text="{Binding Name}" />',
              '<TextBlock FontWeight="SemiBold" Text="{Binding Name}" />')
p.write_text(t, encoding="utf-8")
print("updated ProfilesPage.xaml")
