using AudioProfiles.Helpers;
using AudioProfiles.Models;
using AudioProfiles.Services;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Automation;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Navigation;
using Windows.System;

namespace AudioProfiles.Views;

public sealed partial class EditProfilePage : Page
{
    private AppController Controller => App.Instance.Controller;
    private AudioProfile _profile = new();
    private bool _isNew = true;
    private bool _ready;

    public EditProfilePage()
    {
        InitializeComponent();
        AutomationProperties.SetName(BackButton, Loc.Get("Back"));
        ToolTipService.SetToolTip(BackButton, Loc.Get("Back"));
        AutomationProperties.SetName(CancelButton, Loc.Get("Cancel"));
        NameLabel.Text = Loc.Get("Name");
        IconLabel.Text = Loc.Get("Icon");
        OutputLabel.Text = Loc.Get("Output");
        InputLabel.Text = Loc.Get("Input");
        ShortcutLabel.Text = Loc.Get("Shortcut");
        ShortcutHelp.Text = Loc.Get("ShortcutHelp");
        HotkeyBox.PlaceholderText = Loc.Get("PressShortcut");
        ClearHotkeyButton.Content = Loc.Get("ClearShortcut");
        AdvancedExpander.Header = Loc.Get("Advanced");
        AdvancedHelp.Text = Loc.Get("AdvancedProfileHelp");
        AdvancedRolesSwitch.Header = Loc.Get("UseAdvancedRoles");
        AdvancedRolesHint.Text = Loc.Get("AdvancedRolesHint");
        OutputConsoleLabel.Text = Loc.Format("OutputRole", Loc.Get("RoleDefault"));
        OutputMultimediaLabel.Text = Loc.Format("OutputRole", Loc.Get("RoleMedia"));
        OutputCommunicationsLabel.Text = Loc.Format("OutputRole", Loc.Get("RoleCalls"));
        InputConsoleLabel.Text = Loc.Format("InputRole", Loc.Get("RoleDefault"));
        InputMultimediaLabel.Text = Loc.Format("InputRole", Loc.Get("RoleMedia"));
        InputCommunicationsLabel.Text = Loc.Format("InputRole", Loc.Get("RoleCalls"));
        SaveButton.Content = Loc.Get("Save");
        CancelButton.Content = Loc.Get("Cancel");
        AutomationProperties.SetName(NameBox, Loc.Get("Name"));
        AutomationProperties.SetName(OutputBox, Loc.Get("Output"));
        AutomationProperties.SetName(InputBox, Loc.Get("Input"));
        AutomationProperties.SetName(HotkeyBox, Loc.Get("Shortcut"));
        AutomationProperties.SetName(OutputConsoleBox, OutputConsoleLabel.Text);
        AutomationProperties.SetName(OutputMultimediaBox, OutputMultimediaLabel.Text);
        AutomationProperties.SetName(OutputCommunicationsBox, OutputCommunicationsLabel.Text);
        AutomationProperties.SetName(InputConsoleBox, InputConsoleLabel.Text);
        AutomationProperties.SetName(InputMultimediaBox, InputMultimediaLabel.Text);
        AutomationProperties.SetName(InputCommunicationsBox, InputCommunicationsLabel.Text);
    }

    protected override void OnNavigatedTo(NavigationEventArgs e)
    {
        base.OnNavigatedTo(e);
        var existing = e.Parameter as string;
        var found = Controller.Profiles.FirstOrDefault(p => p.Id == existing);
        _isNew = found is null;
        _profile = found?.Clone() ?? new AudioProfile();
        TitleText.Text = _isNew ? Loc.Get("NewProfile") : Loc.Get("EditProfile");
        NameBox.Text = _profile.Name;
        BindIcons();
        BindDevices();
        HotkeyBox.Text = HotkeyFormatter.ToDisplay(_profile.Hotkey);
        ErrorText.Text = string.Empty;
        _ready = false;
        AdvancedRolesSwitch.IsOn = _profile.UseAdvancedRoles;
        AdvancedExpander.IsExpanded = _profile.UseAdvancedRoles;
        UpdateAdvancedVisibility();
        _ready = true;
    }

    private void BindIcons()
    {
        var items = Enum.GetValues<ProfileIconKind>().Select(kind => new IconChoice
        {
            Kind = kind,
            Glyph = ProfileIcons.Glyph(kind),
            Label = ProfileIcons.DisplayName(kind)
        }).ToList();
        IconGrid.ItemsSource = items;
        IconGrid.SelectedItem = items.FirstOrDefault(i => i.Kind == _profile.Icon) ?? items[0];
    }

    private void BindDevices()
    {
        var outputs = Controller.Audio.GetDevices(AudioFlow.Playback);
        var inputs = Controller.Audio.GetDevices(AudioFlow.Recording);
        BindBox(OutputBox, OutputWarning, outputs, _profile.Output, Loc.Get("ChooseOutput"));
        BindBox(InputBox, InputWarning, inputs, _profile.Input, Loc.Get("ChooseInput"));
        BindBox(OutputConsoleBox, null, outputs, RoleOrPrimary(_profile.OutputConsole, _profile.Output), Loc.Get("ChooseOutput"));
        BindBox(OutputMultimediaBox, null, outputs, RoleOrPrimary(_profile.OutputMultimedia, _profile.Output), Loc.Get("ChooseOutput"));
        BindBox(OutputCommunicationsBox, null, outputs, RoleOrPrimary(_profile.OutputCommunications, _profile.Output), Loc.Get("ChooseOutput"));
        BindBox(InputConsoleBox, null, inputs, RoleOrPrimary(_profile.InputConsole, _profile.Input), Loc.Get("ChooseInput"));
        BindBox(InputMultimediaBox, null, inputs, RoleOrPrimary(_profile.InputMultimedia, _profile.Input), Loc.Get("ChooseInput"));
        BindBox(InputCommunicationsBox, null, inputs, RoleOrPrimary(_profile.InputCommunications, _profile.Input), Loc.Get("ChooseInput"));
    }

    private static SavedDeviceReference RoleOrPrimary(SavedDeviceReference? role, SavedDeviceReference primary) =>
        role is not null && !string.IsNullOrWhiteSpace(role.Id) ? role : primary;

    private static void BindBox(ComboBox box, TextBlock? warning, IReadOnlyList<AudioDeviceInfo> devices, SavedDeviceReference current, string placeholder)
    {
        var items = devices.Select(d => new DeviceChoice
        {
            Id = d.Id,
            Name = d.Availability == DeviceAvailability.Available ? d.Name : $"{d.Name} ({Loc.Get("NotConnected")})",
            Available = d.Availability == DeviceAvailability.Available
        }).ToList();

        if (!string.IsNullOrWhiteSpace(current.Id) && items.All(i => !string.Equals(i.Id, current.Id, StringComparison.OrdinalIgnoreCase)))
        {
            items.Insert(0, new DeviceChoice
            {
                Id = current.Id,
                Name = $"{(string.IsNullOrWhiteSpace(current.Name) ? current.Id : current.Name)} ({Loc.Get("NotConnected")})",
                Available = false
            });
        }

        box.ItemsSource = items;
        box.DisplayMemberPath = nameof(DeviceChoice.Name);
        box.SelectedItem = items.FirstOrDefault(i => string.Equals(i.Id, current.Id, StringComparison.OrdinalIgnoreCase));
        box.PlaceholderText = placeholder;
        if (warning is not null)
        {
            warning.Visibility = (!string.IsNullOrWhiteSpace(current.Id) && items.FirstOrDefault(i => i.Id == current.Id)?.Available == false)
                ? Visibility.Visible
                : Visibility.Collapsed;
            warning.Text = Loc.Get("NotConnected");
        }
    }

    private void AdvancedRolesSwitch_Toggled(object sender, RoutedEventArgs e)
    {
        if (!_ready)
        {
            return;
        }

        if (AdvancedRolesSwitch.IsOn)
        {
            SeedAdvancedFromSimple();
        }

        UpdateAdvancedVisibility();
    }

    private void SeedAdvancedFromSimple()
    {
        CopySelection(OutputBox, OutputConsoleBox, OutputMultimediaBox, OutputCommunicationsBox);
        CopySelection(InputBox, InputConsoleBox, InputMultimediaBox, InputCommunicationsBox);
    }

    private static void CopySelection(ComboBox source, params ComboBox[] targets)
    {
        foreach (var target in targets)
        {
            if (target.SelectedItem is null)
            {
                target.SelectedItem = source.SelectedItem;
            }
        }
    }

    private void UpdateAdvancedVisibility()
    {
        AdvancedRolesPanel.Visibility = AdvancedRolesSwitch.IsOn ? Visibility.Visible : Visibility.Collapsed;
    }

    private void HotkeyBox_KeyDown(object sender, KeyRoutedEventArgs e)
    {
        e.Handled = true;
        var key = HotkeyFormatter.ResolvePressedKey(e.Key, e.OriginalKey);
        var control = Microsoft.UI.Input.InputKeyboardSource.GetKeyStateForCurrentThread(VirtualKey.Control).HasFlag(Windows.UI.Core.CoreVirtualKeyStates.Down);
        var alt = Microsoft.UI.Input.InputKeyboardSource.GetKeyStateForCurrentThread(VirtualKey.Menu).HasFlag(Windows.UI.Core.CoreVirtualKeyStates.Down);
        var shift = Microsoft.UI.Input.InputKeyboardSource.GetKeyStateForCurrentThread(VirtualKey.Shift).HasFlag(Windows.UI.Core.CoreVirtualKeyStates.Down);
        var windows = Microsoft.UI.Input.InputKeyboardSource.GetKeyStateForCurrentThread(VirtualKey.LeftWindows).HasFlag(Windows.UI.Core.CoreVirtualKeyStates.Down)
            || Microsoft.UI.Input.InputKeyboardSource.GetKeyStateForCurrentThread(VirtualKey.RightWindows).HasFlag(Windows.UI.Core.CoreVirtualKeyStates.Down);

        if (!HotkeyFormatter.TryCreate(key, control, alt, shift, windows, out var binding, out var errorKey))
        {
            ErrorText.Text = errorKey is null ? string.Empty : Loc.Get(errorKey);
            return;
        }

        if (HotkeyFormatter.Conflicts(binding, Controller.Profiles, _profile.Id))
        {
            ErrorText.Text = Loc.Get("ShortcutInUse");
            return;
        }

        if (!Controller.Hotkeys.TryRegister(binding, out var registerError))
        {
            ErrorText.Text = Loc.Get(registerError ?? "ShortcutInUse");
            return;
        }

        _profile.Hotkey = binding;
        HotkeyBox.Text = HotkeyFormatter.ToDisplay(binding);
        ErrorText.Text = string.Empty;
    }

    private void ClearHotkeyButton_Click(object sender, RoutedEventArgs e)
    {
        _profile.Hotkey = new HotkeyBinding();
        HotkeyBox.Text = Loc.Get("NoShortcut");
        ErrorText.Text = string.Empty;
    }

    private void SaveButton_Click(object sender, RoutedEventArgs e)
    {
        _profile.Name = NameBox.Text?.Trim() ?? string.Empty;
        if (string.IsNullOrWhiteSpace(_profile.Name))
        {
            ErrorText.Text = Loc.Get("MissingName");
            return;
        }

        if (IconGrid.SelectedItem is IconChoice icon)
        {
            _profile.Icon = icon.Kind;
        }

        if (OutputBox.SelectedItem is not DeviceChoice output || InputBox.SelectedItem is not DeviceChoice input)
        {
            ErrorText.Text = Loc.Get("MissingDevices");
            return;
        }

        _profile.Output = ToReference(output);
        _profile.Input = ToReference(input);
        _profile.UseAdvancedRoles = AdvancedRolesSwitch.IsOn;
        if (_profile.UseAdvancedRoles)
        {
            if (!TryReadRole(OutputConsoleBox, out var outputConsole) ||
                !TryReadRole(OutputMultimediaBox, out var outputMultimedia) ||
                !TryReadRole(OutputCommunicationsBox, out var outputCommunications) ||
                !TryReadRole(InputConsoleBox, out var inputConsole) ||
                !TryReadRole(InputMultimediaBox, out var inputMultimedia) ||
                !TryReadRole(InputCommunicationsBox, out var inputCommunications))
            {
                ErrorText.Text = Loc.Get("MissingAdvancedDevices");
                return;
            }

            _profile.OutputConsole = outputConsole;
            _profile.OutputMultimedia = outputMultimedia;
            _profile.OutputCommunications = outputCommunications;
            _profile.InputConsole = inputConsole;
            _profile.InputMultimedia = inputMultimedia;
            _profile.InputCommunications = inputCommunications;
        }
        else
        {
            _profile.OutputConsole = null;
            _profile.OutputMultimedia = null;
            _profile.OutputCommunications = null;
            _profile.InputConsole = null;
            _profile.InputMultimedia = null;
            _profile.InputCommunications = null;
        }

        Controller.AddOrUpdateProfile(_profile);
        App.Instance.MainAppWindow?.NavigateToProfiles();
    }

    private static bool TryReadRole(ComboBox box, out SavedDeviceReference reference)
    {
        if (box.SelectedItem is DeviceChoice choice)
        {
            reference = ToReference(choice);
            return true;
        }

        reference = new SavedDeviceReference();
        return false;
    }

    private static SavedDeviceReference ToReference(DeviceChoice choice) => new()
    {
        Id = choice.Id,
        Name = StripUnavailable(choice.Name)
    };

    private void BackButton_Click(object sender, RoutedEventArgs e)
    {
        App.Instance.MainAppWindow?.NavigateToProfiles();
    }

    private static string StripUnavailable(string name)
    {
        var marker = $" ({Loc.Get("NotConnected")})";
        return name.EndsWith(marker, StringComparison.Ordinal) ? name[..^marker.Length] : name;
    }

    private sealed class IconChoice
    {
        public ProfileIconKind Kind { get; init; }
        public string Glyph { get; init; } = string.Empty;
        public string Label { get; init; } = string.Empty;
    }

    private sealed class DeviceChoice
    {
        public string Id { get; init; } = string.Empty;
        public string Name { get; init; } = string.Empty;
        public bool Available { get; init; }
    }
}
