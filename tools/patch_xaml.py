from pathlib import Path
root = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles")

(root / "Views/ProfilesPage.xaml").write_text(r'''<?xml version="1.0" encoding="utf-8" ?>
<Page
    x:Class="AudioProfiles.Views.ProfilesPage"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

    <Grid Padding="{StaticResource PagePadding}">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto" />
            <RowDefinition Height="*" />
        </Grid.RowDefinitions>

        <Grid>
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="*" />
                <ColumnDefinition Width="Auto" />
            </Grid.ColumnDefinitions>
            <StackPanel Spacing="4">
                <TextBlock x:Name="TitleText" Style="{StaticResource PageTitleStyle}" />
                <TextBlock x:Name="CurrentProfileText" Style="{StaticResource SectionBodyStyle}" />
            </StackPanel>
            <StackPanel Grid.Column="1" Orientation="Horizontal" Spacing="8">
                <Button x:Name="RefreshButton" Style="{StaticResource LargeButtonStyle}" Click="RefreshButton_Click" />
                <Button x:Name="AddButton" Style="{StaticResource LargeAccentButtonStyle}" Click="AddButton_Click" />
            </StackPanel>
        </Grid>

        <Grid Grid.Row="1" Margin="0,20,0,0">
            <StackPanel
                x:Name="EmptyState"
                MaxWidth="560"
                HorizontalAlignment="Center"
                VerticalAlignment="Center"
                Spacing="16"
                Visibility="Collapsed">
                <FontIcon FontSize="42" Glyph="&#xE8D6;" Foreground="{StaticResource BrandTealBrush}" />
                <TextBlock x:Name="EmptyTitle" Style="{StaticResource PageTitleStyle}" HorizontalAlignment="Center" TextAlignment="Center" />
                <TextBlock x:Name="EmptyBody" Style="{StaticResource SectionBodyStyle}" HorizontalAlignment="Center" TextAlignment="Center" />
                <Button x:Name="EmptyCreateButton" HorizontalAlignment="Center" Style="{StaticResource LargeAccentButtonStyle}" Click="AddButton_Click" />
            </StackPanel>

            <ListView
                x:Name="ProfileList"
                IsItemClickEnabled="True"
                ItemClick="ProfileList_ItemClick"
                SelectionMode="None">
                <ListView.ItemContainerStyle>
                    <Style TargetType="ListViewItem">
                        <Setter Property="HorizontalContentAlignment" Value="Stretch" />
                        <Setter Property="Padding" Value="0,0,0,12" />
                        <Setter Property="MinHeight" Value="96" />
                    </Style>
                </ListView.ItemContainerStyle>
                <ListView.ItemTemplate>
                    <DataTemplate>
                        <Border
                            Padding="20"
                            Background="{Binding CardBrush}"
                            BorderBrush="{Binding BorderBrush}"
                            BorderThickness="1"
                            CornerRadius="16">
                            <Grid ColumnSpacing="16">
                                <Grid.ColumnDefinitions>
                                    <ColumnDefinition Width="Auto" />
                                    <ColumnDefinition Width="*" />
                                    <ColumnDefinition Width="Auto" />
                                </Grid.ColumnDefinitions>
                                <Border
                                    Width="56"
                                    Height="56"
                                    Background="{StaticResource BrandTealBrush}"
                                    CornerRadius="16">
                                    <FontIcon
                                        HorizontalAlignment="Center"
                                        VerticalAlignment="Center"
                                        FontSize="24"
                                        Foreground="White"
                                        Glyph="{Binding Glyph}" />
                                </Border>
                                <StackPanel Grid.Column="1" VerticalAlignment="Center" Spacing="4">
                                    <StackPanel Orientation="Horizontal" Spacing="10">
                                        <TextBlock FontSize="24" FontWeight="SemiBold" Text="{Binding Name}" />
                                        <Border
                                            Padding="10,4"
                                            Background="{StaticResource BrandAmberBrush}"
                                            CornerRadius="999"
                                            Visibility="{Binding ActiveVisibility}">
                                            <TextBlock FontWeight="SemiBold" Text="{Binding ActiveLabel}" />
                                        </Border>
                                    </StackPanel>
                                    <TextBlock FontSize="16" Opacity="0.82" Text="{Binding DeviceSummary}" TextWrapping="Wrap" />
                                    <TextBlock FontSize="14" Opacity="0.7" Text="{Binding StatusText}" TextWrapping="Wrap" />
                                </StackPanel>
                                <StackPanel Grid.Column="2" VerticalAlignment="Center" Spacing="8">
                                    <Button
                                        MinHeight="44"
                                        Click="EditButton_Click"
                                        Content="{Binding ActionLabel}"
                                        Tag="{Binding Id}" />
                                    <Button
                                        MinHeight="44"
                                        Click="DeleteButton_Click"
                                        Content="{Binding DeleteLabel}"
                                        Tag="{Binding Id}" />
                                </StackPanel>
                            </Grid>
                        </Border>
                    </DataTemplate>
                </ListView.ItemTemplate>
            </ListView>
        </Grid>
    </Grid>
</Page>
''', encoding="utf-8", newline="\n")

cs = root / "Views/ProfilesPage.xaml.cs"
text = cs.read_text(encoding="utf-8")
text = text.replace('string.Join(" Â· ", missing)', 'string.Join(" · ", missing)')
cs.write_text(text, encoding="utf-8", newline="\n")

(root / "Services/AudioSelfTest.cs").write_text(r'''using System.Runtime.InteropServices;
using System.Text;
using AudioProfiles.Interop;
using AudioProfiles.Models;

namespace AudioProfiles.Services;

internal static class AudioSelfTest
{
    public static bool Run()
    {
        NativeMethods.AttachConsole(NativeMethods.AttachParentProcess);
        NativeMethods.CoInitializeEx(nint.Zero, NativeMethods.CoInitApartmentThreaded);

        var log = new AppLog();
        var output = new StringBuilder();
        void Write(string line)
        {
            output.AppendLine(line);
            Console.WriteLine(line);
        }

        try
        {
            using var audio = new AudioDeviceService(log);
            var outputs = audio.GetDevices(AudioFlow.Playback).Where(d => d.Availability == DeviceAvailability.Available).ToList();
            var inputs = audio.GetDevices(AudioFlow.Recording).Where(d => d.Availability == DeviceAvailability.Available).ToList();
            Write($"Playback devices: {outputs.Count}");
            foreach (var device in outputs)
            {
                Write($"  OUT {device.Name} [{device.Id}]");
            }

            Write($"Capture devices: {inputs.Count}");
            foreach (var device in inputs)
            {
                Write($"  IN  {device.Name} [{device.Id}]");
            }

            var before = audio.GetCurrentDefaults();
            Write($"Current defaults: out={before.OutputId} in={before.InputId}");
            if (outputs.Count == 0 || inputs.Count == 0)
            {
                Write("Need at least one playback device and one capture device.");
                Persist(output, false);
                return false;
            }

            var originalOutput = outputs.FirstOrDefault(d => string.Equals(d.Id, before.OutputId, StringComparison.OrdinalIgnoreCase)) ?? outputs[0];
            var originalInput = inputs.FirstOrDefault(d => string.Equals(d.Id, before.InputId, StringComparison.OrdinalIgnoreCase)) ?? inputs[0];
            var targetOutput = outputs.FirstOrDefault(d => !string.Equals(d.Id, originalOutput.Id, StringComparison.OrdinalIgnoreCase)) ?? originalOutput;
            var targetInput = inputs.FirstOrDefault(d => !string.Equals(d.Id, originalInput.Id, StringComparison.OrdinalIgnoreCase)) ?? originalInput;

            var switchOut = audio.SetDefaultDevice(new SavedDeviceReference { Id = targetOutput.Id, Name = targetOutput.Name }, AudioFlow.Playback);
            var switchIn = audio.SetDefaultDevice(new SavedDeviceReference { Id = targetInput.Id, Name = targetInput.Name }, AudioFlow.Recording);
            var after = audio.GetCurrentDefaults();
            Write($"Switch output {targetOutput.Name}: {switchOut.Succeeded}");
            Write($"Switch input {targetInput.Name}: {switchIn.Succeeded}");
            Write($"Defaults after switch: out={after.OutputId} in={after.InputId}");

            var restoreOut = audio.SetDefaultDevice(new SavedDeviceReference { Id = originalOutput.Id, Name = originalOutput.Name }, AudioFlow.Playback);
            var restoreIn = audio.SetDefaultDevice(new SavedDeviceReference { Id = originalInput.Id, Name = originalInput.Name }, AudioFlow.Recording);
            var restored = audio.GetCurrentDefaults();
            Write($"Restore output {originalOutput.Name}: {restoreOut.Succeeded}");
            Write($"Restore input {originalInput.Name}: {restoreIn.Succeeded}");
            Write($"Defaults after restore: out={restored.OutputId} in={restored.InputId}");

            var switched = switchOut.Succeeded && switchIn.Succeeded &&
                           string.Equals(after.OutputId, targetOutput.Id, StringComparison.OrdinalIgnoreCase) &&
                           string.Equals(after.InputId, targetInput.Id, StringComparison.OrdinalIgnoreCase);
            var restoredOk = restoreOut.Succeeded && restoreIn.Succeeded &&
                             string.Equals(restored.OutputId, originalOutput.Id, StringComparison.OrdinalIgnoreCase) &&
                             string.Equals(restored.InputId, originalInput.Id, StringComparison.OrdinalIgnoreCase);
            var pass = switched && restoredOk;
            Write(pass ? "SELFTEST PASS" : "SELFTEST FAIL");
            Persist(output, pass);
            return pass;
        }
        catch (Exception ex)
        {
            Write(ex.ToString());
            Persist(output, false);
            return false;
        }
    }

    private static void Persist(StringBuilder output, bool pass)
    {
        try
        {
            var directory = Path.Combine(AppContext.BaseDirectory, "self-test");
            Directory.CreateDirectory(directory);
            File.WriteAllText(Path.Combine(directory, "result.txt"), output + (pass ? "PASS" : "FAIL") + Environment.NewLine);
        }
        catch
        {
        }
    }
}
''', encoding="utf-8", newline="\n")
print("wrote xaml and self-test")
