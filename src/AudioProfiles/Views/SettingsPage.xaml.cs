using System.Diagnostics;
using AudioProfiles.Helpers;
using AudioProfiles.Models;
using AudioProfiles.Services;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Navigation;

namespace AudioProfiles.Views;

public sealed partial class SettingsPage : Page
{
    private AppController Controller => App.Instance.Controller;
    private bool _ready;

    public SettingsPage()
    {
        InitializeComponent();
        TitleText.Text = Loc.Get("Settings");
        ThemeLabel.Text = Loc.Get("Theme");
        StartupSwitch.Header = Loc.Get("StartWithWindows");
        BackgroundSwitch.Header = Loc.Get("KeepBackground");
        LaunchMinimizedSwitch.Header = Loc.Get("LaunchMinimized");
        NotificationSwitch.Header = Loc.Get("ShowNotifications");
        AdvancedExpander.Header = Loc.Get("Advanced");
        AdvancedHelp.Text = Loc.Get("SettingsAdvancedHelp");
        AdvancedLoggingSwitch.Header = Loc.Get("WriteDetailedLogs");
        AdvancedRolesHint.Text = Loc.Get("SettingsAdvancedRolesHint");
        AdvancedRolesSwitch.Header = Loc.Get("UseAdvancedRoles");
        OutputConsoleLabel.Text = Loc.Format("OutputRole", Loc.Get("RoleDefault"));
        OutputMultimediaLabel.Text = Loc.Format("OutputRole", Loc.Get("RoleMedia"));
        OutputCommunicationsLabel.Text = Loc.Format("OutputRole", Loc.Get("RoleCalls"));
        InputConsoleLabel.Text = Loc.Format("InputRole", Loc.Get("RoleDefault"));
        InputMultimediaLabel.Text = Loc.Format("InputRole", Loc.Get("RoleMedia"));
        InputCommunicationsLabel.Text = Loc.Format("InputRole", Loc.Get("RoleCalls"));
        OpenAdvancedProfileButton.Content = Loc.Get("OpenProfileAdvanced");
        AboutTitle.Text = Loc.Get("About");
        AboutAuthor.Text = Loc.Get("AboutAuthor");
        GitHubProfileLink.Content = Loc.Get("OpenGitHubProfile");
        GitHubRepoLink.Content = Loc.Get("OpenGitHubRepo");
        LogsButton.Content = Loc.Get("OpenLogs");
        ThemeBox.ItemsSource = new[]
        {
            new ThemeChoice(AppTheme.System, Loc.Get("ThemeSystem")),
            new ThemeChoice(AppTheme.Light, Loc.Get("ThemeLight")),
            new ThemeChoice(AppTheme.Dark, Loc.Get("ThemeDark"))
        };
        ThemeBox.DisplayMemberPath = nameof(ThemeChoice.Label);
        AdvancedProfileBox.DisplayMemberPath = nameof(ProfileChoice.Label);
    }

    protected override void OnNavigatedTo(NavigationEventArgs e)
    {
        base.OnNavigatedTo(e);
        _ready = false;
        ThemeBox.SelectedItem = ((ThemeChoice[])ThemeBox.ItemsSource!).First(t => t.Value == Controller.Settings.Theme);
        StartupSwitch.IsOn = Controller.Settings.StartWithWindows;
        BackgroundSwitch.IsOn = Controller.Settings.KeepRunningInBackground;
        LaunchMinimizedSwitch.IsOn = Controller.Settings.LaunchMinimized;
        NotificationSwitch.IsOn = Controller.Settings.ShowNotifications;
        AdvancedLoggingSwitch.IsOn = Controller.Settings.WriteDetailedLogs;
        BindAdvancedProfiles();
        BindAdvancedRoles();
        var version = typeof(App).Assembly.GetName().Version?.ToString(3) ?? "1.0.0";
        AboutBody.Text = Loc.Format("AboutBody", version);
        _ready = true;
    }

    private void BindAdvancedProfiles()
    {
        var items = Controller.Profiles
            .Select(profile => new ProfileChoice(profile.Id, profile.Name))
            .ToList();
        AdvancedProfileBox.ItemsSource = items;
        AdvancedProfileBox.PlaceholderText = Loc.Get("ChooseProfileForAdvanced");
        var hasProfiles = items.Count > 0;
        AdvancedProfileBox.IsEnabled = hasProfiles;
        AdvancedRolesSwitch.IsEnabled = hasProfiles;
        OpenAdvancedProfileButton.IsEnabled = hasProfiles;
        if (!hasProfiles)
        {
            AdvancedProfileBox.SelectedItem = null;
            return;
        }

        var lastId = Controller.Settings.LastActivatedProfileId;
        AdvancedProfileBox.SelectedItem = items.FirstOrDefault(item => item.Id == lastId) ?? items[0];
    }

    private AudioProfile? SelectedProfile()
    {
        if (AdvancedProfileBox.SelectedItem is not ProfileChoice choice)
        {
            return null;
        }

        return Controller.Profiles.FirstOrDefault(profile => profile.Id == choice.Id);
    }

    private void BindAdvancedRoles()
    {
        var profile = SelectedProfile();
        var hasProfile = profile is not null;
        AdvancedRolesSwitch.IsEnabled = hasProfile;
        OpenAdvancedProfileButton.IsEnabled = hasProfile;
        if (profile is null)
        {
            AdvancedRolesSwitch.IsOn = false;
            AdvancedRolesPanel.Visibility = Visibility.Collapsed;
            return;
        }

        AdvancedRolesSwitch.IsOn = profile.UseAdvancedRoles;
        AdvancedRolesPanel.Visibility = profile.UseAdvancedRoles ? Visibility.Visible : Visibility.Collapsed;
        var outputs = Controller.Audio.GetDevices(AudioFlow.Playback);
        var inputs = Controller.Audio.GetDevices(AudioFlow.Recording);
        BindRoleBox(OutputConsoleBox, outputs, RoleOrPrimary(profile.OutputConsole, profile.Output), Loc.Get("ChooseOutput"));
        BindRoleBox(OutputMultimediaBox, outputs, RoleOrPrimary(profile.OutputMultimedia, profile.Output), Loc.Get("ChooseOutput"));
        BindRoleBox(OutputCommunicationsBox, outputs, RoleOrPrimary(profile.OutputCommunications, profile.Output), Loc.Get("ChooseOutput"));
        BindRoleBox(InputConsoleBox, inputs, RoleOrPrimary(profile.InputConsole, profile.Input), Loc.Get("ChooseInput"));
        BindRoleBox(InputMultimediaBox, inputs, RoleOrPrimary(profile.InputMultimedia, profile.Input), Loc.Get("ChooseInput"));
        BindRoleBox(InputCommunicationsBox, inputs, RoleOrPrimary(profile.InputCommunications, profile.Input), Loc.Get("ChooseInput"));
    }

    private static SavedDeviceReference RoleOrPrimary(SavedDeviceReference? role, SavedDeviceReference primary) =>
        role is not null && !string.IsNullOrWhiteSpace(role.Id) ? role : primary;

    private static void BindRoleBox(ComboBox box, IReadOnlyList<AudioDeviceInfo> devices, SavedDeviceReference current, string placeholder)
    {
        var items = devices.Select(device => new DeviceChoice
        {
            Id = device.Id,
            Name = device.Availability == DeviceAvailability.Available ? device.Name : $"{device.Name} ({Loc.Get("NotConnected")})",
            DisplayName = device.Name
        }).ToList();

        if (!string.IsNullOrWhiteSpace(current.Id) && items.All(item => !string.Equals(item.Id, current.Id, StringComparison.OrdinalIgnoreCase)))
        {
            var name = string.IsNullOrWhiteSpace(current.Name) ? current.Id : current.Name;
            items.Insert(0, new DeviceChoice
            {
                Id = current.Id,
                Name = $"{name} ({Loc.Get("NotConnected")})",
                DisplayName = name
            });
        }

        box.ItemsSource = items;
        box.DisplayMemberPath = nameof(DeviceChoice.Name);
        box.PlaceholderText = placeholder;
        box.SelectedItem = items.FirstOrDefault(item => string.Equals(item.Id, current.Id, StringComparison.OrdinalIgnoreCase));
    }

    private void PersistSelectedAdvancedRoles()
    {
        var profile = SelectedProfile();
        if (profile is null)
        {
            return;
        }

        profile.UseAdvancedRoles = AdvancedRolesSwitch.IsOn;
        if (!profile.UseAdvancedRoles)
        {
            profile.OutputConsole = null;
            profile.OutputMultimedia = null;
            profile.OutputCommunications = null;
            profile.InputConsole = null;
            profile.InputMultimedia = null;
            profile.InputCommunications = null;
        }
        else
        {
            profile.OutputConsole = ToReference(OutputConsoleBox, profile.Output);
            profile.OutputMultimedia = ToReference(OutputMultimediaBox, profile.Output);
            profile.OutputCommunications = ToReference(OutputCommunicationsBox, profile.Output);
            profile.InputConsole = ToReference(InputConsoleBox, profile.Input);
            profile.InputMultimedia = ToReference(InputMultimediaBox, profile.Input);
            profile.InputCommunications = ToReference(InputCommunicationsBox, profile.Input);
        }

        Controller.AddOrUpdateProfile(profile);
    }

    private static SavedDeviceReference ToReference(ComboBox box, SavedDeviceReference fallback)
    {
        if (box.SelectedItem is DeviceChoice choice)
        {
            return new SavedDeviceReference
            {
                Id = choice.Id,
                Name = choice.DisplayName
            };
        }

        return new SavedDeviceReference { Id = fallback.Id, Name = fallback.Name };
    }

    private void ThemeBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (!_ready || ThemeBox.SelectedItem is not ThemeChoice choice)
        {
            return;
        }

        Controller.Settings.Theme = choice.Value;
        Controller.Persist();
        App.Instance.MainAppWindow?.ApplyTheme();
    }

    private async void StartupSwitch_Toggled(object sender, RoutedEventArgs e)
    {
        if (!_ready)
        {
            return;
        }

        Controller.Settings.StartWithWindows = StartupSwitch.IsOn;
        await Controller.Startup.ApplyAsync(Controller.Settings);
        Controller.Persist();
    }

    private void BackgroundSwitch_Toggled(object sender, RoutedEventArgs e)
    {
        if (!_ready)
        {
            return;
        }

        Controller.Settings.KeepRunningInBackground = BackgroundSwitch.IsOn;
        Controller.Persist();
    }

    private void LaunchMinimizedSwitch_Toggled(object sender, RoutedEventArgs e)
    {
        if (!_ready)
        {
            return;
        }

        Controller.Settings.LaunchMinimized = LaunchMinimizedSwitch.IsOn;
        Controller.Persist();
    }

    private void NotificationSwitch_Toggled(object sender, RoutedEventArgs e)
    {
        if (!_ready)
        {
            return;
        }

        Controller.Settings.ShowNotifications = NotificationSwitch.IsOn;
        Controller.Persist();
    }

    private void AdvancedLoggingSwitch_Toggled(object sender, RoutedEventArgs e)
    {
        if (!_ready)
        {
            return;
        }

        Controller.Settings.WriteDetailedLogs = AdvancedLoggingSwitch.IsOn;
        Controller.Log.Verbose = AdvancedLoggingSwitch.IsOn;
        Controller.Persist();
    }

    private void AdvancedProfileBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (!_ready)
        {
            return;
        }

        var previous = _ready;
        _ready = false;
        BindAdvancedRoles();
        _ready = previous;
    }

    private void AdvancedRolesSwitch_Toggled(object sender, RoutedEventArgs e)
    {
        if (!_ready)
        {
            return;
        }

        AdvancedRolesPanel.Visibility = AdvancedRolesSwitch.IsOn ? Visibility.Visible : Visibility.Collapsed;
        PersistSelectedAdvancedRoles();
    }

    private void AdvancedRoleBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (!_ready || !AdvancedRolesSwitch.IsOn)
        {
            return;
        }

        PersistSelectedAdvancedRoles();
    }

    private void OpenAdvancedProfileButton_Click(object sender, RoutedEventArgs e)
    {
        if (AdvancedProfileBox.SelectedItem is not ProfileChoice choice)
        {
            App.Instance.MainAppWindow?.NavigateToEditor(null);
            return;
        }

        App.Instance.MainAppWindow?.NavigateToEditor(choice.Id);
    }

    private void LogsButton_Click(object sender, RoutedEventArgs e)
    {
        Process.Start(new ProcessStartInfo
        {
            FileName = Controller.Log.DirectoryPath,
            UseShellExecute = true
        });
    }

    private void GitHubProfileLink_Click(object sender, RoutedEventArgs e)
    {
        OpenUrl(AppIdentity.AuthorUrl);
    }

    private void GitHubRepoLink_Click(object sender, RoutedEventArgs e)
    {
        OpenUrl(AppIdentity.RepositoryUrl);
    }

    private static void OpenUrl(string url)
    {
        Process.Start(new ProcessStartInfo
        {
            FileName = url,
            UseShellExecute = true
        });
    }

    private sealed record ThemeChoice(AppTheme Value, string Label);
    private sealed record ProfileChoice(string Id, string Label);

    private sealed class DeviceChoice
    {
        public string Id { get; init; } = string.Empty;
        public string Name { get; init; } = string.Empty;
        public string DisplayName { get; init; } = string.Empty;
    }
}
