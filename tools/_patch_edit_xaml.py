from pathlib import Path
p = Path(r'C:\\Users\\neura\\repos\\audio-device-switcher\\src\\AudioProfiles\\Views\\EditProfilePage.xaml')
p.write_text('''<?xml version="1.0" encoding="utf-8" ?>
<Page
    x:Class="AudioProfiles.Views.EditProfilePage"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <ScrollViewer>
        <StackPanel MaxWidth="760" Padding="{StaticResource PagePadding}" Spacing="16">
            <StackPanel Orientation="Horizontal" Spacing="8">
                <Button x:Name="BackButton" Click="BackButton_Click" />
                <TextBlock x:Name="TitleText" Style="{StaticResource PageTitleStyle}" VerticalAlignment="Center" />
            </StackPanel>

            <TextBlock x:Name="NameLabel" FontWeight="SemiBold" />
            <TextBox x:Name="NameBox" />

            <TextBlock x:Name="IconLabel" FontWeight="SemiBold" />
            <GridView
                x:Name="IconGrid"
                IsItemClickEnabled="True"
                SelectionMode="Single">
                <GridView.ItemTemplate>
                    <DataTemplate>
                        <StackPanel Width="84" Padding="6" Spacing="4">
                            <FontIcon HorizontalAlignment="Center" FontSize="20" Glyph="{Binding Glyph}" />
                            <TextBlock HorizontalAlignment="Center" Text="{Binding Label}" />
                        </StackPanel>
                    </DataTemplate>
                </GridView.ItemTemplate>
            </GridView>

            <TextBlock x:Name="OutputLabel" FontWeight="SemiBold" />
            <ComboBox x:Name="OutputBox" HorizontalAlignment="Stretch" />
            <TextBlock x:Name="OutputWarning" Foreground="{ThemeResource SystemFillColorCriticalBrush}" Visibility="Collapsed" />

            <TextBlock x:Name="InputLabel" FontWeight="SemiBold" />
            <ComboBox x:Name="InputBox" HorizontalAlignment="Stretch" />
            <TextBlock x:Name="InputWarning" Foreground="{ThemeResource SystemFillColorCriticalBrush}" Visibility="Collapsed" />

            <TextBlock x:Name="ShortcutLabel" FontWeight="SemiBold" />
            <TextBlock x:Name="ShortcutHelp" Style="{StaticResource SectionBodyStyle}" />
            <TextBox
                x:Name="HotkeyBox"
                IsReadOnly="True"
                KeyDown="HotkeyBox_KeyDown" />
            <Button x:Name="ClearHotkeyButton" Click="ClearHotkeyButton_Click" />

            <Expander x:Name="AdvancedExpander" IsExpanded="False">
                <StackPanel Spacing="12">
                    <TextBlock x:Name="AdvancedHelp" Style="{StaticResource SectionBodyStyle}" />
                    <ToggleSwitch x:Name="AdvancedRolesSwitch" Toggled="AdvancedRolesSwitch_Toggled" />
                    <TextBlock x:Name="AdvancedRolesHint" Style="{StaticResource SectionBodyStyle}" />
                    <StackPanel x:Name="AdvancedRolesPanel" Spacing="12" Visibility="Collapsed">
                        <TextBlock x:Name="OutputConsoleLabel" FontWeight="SemiBold" />
                        <ComboBox x:Name="OutputConsoleBox" HorizontalAlignment="Stretch" />
                        <TextBlock x:Name="OutputMultimediaLabel" FontWeight="SemiBold" />
                        <ComboBox x:Name="OutputMultimediaBox" HorizontalAlignment="Stretch" />
                        <TextBlock x:Name="OutputCommunicationsLabel" FontWeight="SemiBold" />
                        <ComboBox x:Name="OutputCommunicationsBox" HorizontalAlignment="Stretch" />
                        <TextBlock x:Name="InputConsoleLabel" FontWeight="SemiBold" />
                        <ComboBox x:Name="InputConsoleBox" HorizontalAlignment="Stretch" />
                        <TextBlock x:Name="InputMultimediaLabel" FontWeight="SemiBold" />
                        <ComboBox x:Name="InputMultimediaBox" HorizontalAlignment="Stretch" />
                        <TextBlock x:Name="InputCommunicationsLabel" FontWeight="SemiBold" />
                        <ComboBox x:Name="InputCommunicationsBox" HorizontalAlignment="Stretch" />
                    </StackPanel>
                </StackPanel>
            </Expander>

            <TextBlock x:Name="ErrorText" Foreground="{ThemeResource SystemFillColorCriticalBrush}" TextWrapping="Wrap" />

            <StackPanel Orientation="Horizontal" Spacing="8">
                <Button x:Name="SaveButton" Style="{StaticResource AccentButtonStyle}" Click="SaveButton_Click" />
                <Button x:Name="CancelButton" Click="BackButton_Click" />
            </StackPanel>
        </StackPanel>
    </ScrollViewer>
</Page>
''', encoding='utf-8')
print('EditProfilePage.xaml written', p.stat().st_size)
