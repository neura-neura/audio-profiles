from pathlib import Path
p = Path(r'C:\\Users\\neura\\repos\\audio-device-switcher\\src\\AudioProfiles\\Views\\SettingsPage.xaml')
p.write_text('''<?xml version="1.0" encoding="utf-8" ?>
<Page
    x:Class="AudioProfiles.Views.SettingsPage"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <ScrollViewer>
        <StackPanel MaxWidth="760" Padding="{StaticResource PagePadding}" Spacing="16">
            <TextBlock x:Name="TitleText" Style="{StaticResource PageTitleStyle}" />

            <TextBlock x:Name="ThemeLabel" FontWeight="SemiBold" />
            <ComboBox x:Name="ThemeBox" MinWidth="220" SelectionChanged="ThemeBox_SelectionChanged" />

            <ToggleSwitch x:Name="StartupSwitch" Toggled="StartupSwitch_Toggled" />
            <ToggleSwitch x:Name="BackgroundSwitch" Toggled="BackgroundSwitch_Toggled" />
            <ToggleSwitch x:Name="LaunchMinimizedSwitch" Toggled="LaunchMinimizedSwitch_Toggled" />
            <ToggleSwitch x:Name="NotificationSwitch" Toggled="NotificationSwitch_Toggled" />

            <Expander x:Name="AdvancedExpander" IsExpanded="False">
                <TextBlock x:Name="AdvancedHelp" Style="{StaticResource SectionBodyStyle}" />
            </Expander>

            <StackPanel Spacing="8">
                <TextBlock x:Name="AboutTitle" FontSize="20" FontWeight="SemiBold" />
                <TextBlock x:Name="AboutBody" Style="{StaticResource SectionBodyStyle}" />
                <Button x:Name="LogsButton" Click="LogsButton_Click" />
            </StackPanel>
        </StackPanel>
    </ScrollViewer>
</Page>
''', encoding='utf-8')
print('SettingsPage.xaml written')

cs = Path(r'C:\\Users\\neura\\repos\\audio-device-switcher\\src\\AudioProfiles\\Views\\SettingsPage.xaml.cs')
text = cs.read_text(encoding='utf-8')
text = text.replace('AdvancedHelp.Text = Loc.Get("AdvancedHelp");', 'AdvancedHelp.Text = Loc.Get("SettingsAdvancedHelp");')
cs.write_text(text, encoding='utf-8')
print('SettingsPage.xaml.cs updated')
