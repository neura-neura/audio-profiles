from pathlib import Path

p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\MainWindow.xaml.cs")
text = p.read_text(encoding="utf-8")
old = '''    public void NavigateToProfiles()
    {
        RootNavigation.SelectedItem = ProfilesNavItem;
        if (ContentFrame.Content is not ProfilesPage)
        {
            ContentFrame.Navigate(typeof(ProfilesPage));
        }
    }

    public void NavigateToSettings()
    {
        RootNavigation.SelectedItem = SettingsNavItem;
        if (ContentFrame.Content is not SettingsPage)
        {
            ContentFrame.Navigate(typeof(SettingsPage));
        }
    }
'''
new = '''    public void NavigateToProfiles()
    {
        if (!ReferenceEquals(RootNavigation.SelectedItem, ProfilesNavItem))
        {
            RootNavigation.SelectedItem = ProfilesNavItem;
        }

        if (ContentFrame.Content is not ProfilesPage)
        {
            ContentFrame.Navigate(typeof(ProfilesPage));
        }
    }

    public void NavigateToSettings()
    {
        if (!ReferenceEquals(RootNavigation.SelectedItem, SettingsNavItem))
        {
            RootNavigation.SelectedItem = SettingsNavItem;
        }

        if (ContentFrame.Content is not SettingsPage)
        {
            ContentFrame.Navigate(typeof(SettingsPage));
        }
    }
'''
if old not in text:
    raise SystemExit('nav methods not found')
p.write_text(text.replace(old, new), encoding='utf-8', newline='\n')
print('patched navigation')
