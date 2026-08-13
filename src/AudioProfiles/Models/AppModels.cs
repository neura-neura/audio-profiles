namespace AudioProfiles.Models;

public enum AudioFlow
{
    Playback,
    Recording
}

public enum AudioRole
{
    Console,
    Multimedia,
    Communications
}

public enum AppTheme
{
    System,
    Light,
    Dark
}

public enum ProfileIconKind
{
    Desktop,
    Sofa,
    Tv,
    Speaker,
    Headphones,
    Vr
}

public enum DeviceAvailability
{
    Available,
    Disconnected,
    Disabled,
    Unknown
}

public sealed class AudioDeviceInfo
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public required AudioFlow Flow { get; init; }
    public DeviceAvailability Availability { get; init; } = DeviceAvailability.Available;
    public bool IsDefaultConsole { get; init; }
    public bool IsDefaultMultimedia { get; init; }
    public bool IsDefaultCommunications { get; init; }
}

public sealed class SavedDeviceReference
{
    public string Id { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
}

public sealed class HotkeyBinding
{
    public bool Enabled { get; set; }
    public bool Control { get; set; } = true;
    public bool Alt { get; set; } = true;
    public bool Shift { get; set; }
    public bool Windows { get; set; }
    public int VirtualKey { get; set; }

    public bool HasKey => VirtualKey > 0;

    public HotkeyBinding Clone() => new()
    {
        Enabled = Enabled,
        Control = Control,
        Alt = Alt,
        Shift = Shift,
        Windows = Windows,
        VirtualKey = VirtualKey
    };
}

public sealed class AudioProfile
{
    public string Id { get; set; } = Guid.NewGuid().ToString("N");
    public string Name { get; set; } = string.Empty;
    public ProfileIconKind Icon { get; set; } = ProfileIconKind.Speaker;
    public SavedDeviceReference Output { get; set; } = new();
    public SavedDeviceReference Input { get; set; } = new();
    public HotkeyBinding Hotkey { get; set; } = new();
    public bool UseAdvancedRoles { get; set; }
    public SavedDeviceReference? OutputConsole { get; set; }
    public SavedDeviceReference? OutputMultimedia { get; set; }
    public SavedDeviceReference? OutputCommunications { get; set; }
    public SavedDeviceReference? InputConsole { get; set; }
    public SavedDeviceReference? InputMultimedia { get; set; }
    public SavedDeviceReference? InputCommunications { get; set; }

    public AudioProfile Clone() => new()
    {
        Id = Id,
        Name = Name,
        Icon = Icon,
        Output = new SavedDeviceReference { Id = Output.Id, Name = Output.Name },
        Input = new SavedDeviceReference { Id = Input.Id, Name = Input.Name },
        Hotkey = Hotkey.Clone(),
        UseAdvancedRoles = UseAdvancedRoles,
        OutputConsole = CloneRef(OutputConsole),
        OutputMultimedia = CloneRef(OutputMultimedia),
        OutputCommunications = CloneRef(OutputCommunications),
        InputConsole = CloneRef(InputConsole),
        InputMultimedia = CloneRef(InputMultimedia),
        InputCommunications = CloneRef(InputCommunications)
    };

    private static SavedDeviceReference? CloneRef(SavedDeviceReference? source) =>
        source is null ? null : new SavedDeviceReference { Id = source.Id, Name = source.Name };
}

public sealed class AppSettings
{
    public AppTheme Theme { get; set; } = AppTheme.System;
    public bool StartWithWindows { get; set; }
    public bool KeepRunningInBackground { get; set; } = true;
    public bool ShowNotifications { get; set; } = true;
    public bool LaunchMinimized { get; set; }
    public bool WriteDetailedLogs { get; set; }
    public string? LastActivatedProfileId { get; set; }
    public double? WindowLeft { get; set; }
    public double? WindowTop { get; set; }
    public double WindowWidth { get; set; } = 920;
    public double WindowHeight { get; set; } = 720;
}

public sealed class AppState
{
    public int Version { get; set; } = 1;
    public List<AudioProfile> Profiles { get; set; } = [];
    public AppSettings Settings { get; set; } = new();
}

public enum ActivationOutcomeKind
{
    Success,
    Partial,
    Failed
}

public sealed class DeviceSwitchResult
{
    public required SavedDeviceReference Requested { get; init; }
    public bool Succeeded { get; init; }
    public string? ErrorMessage { get; init; }
}

public sealed class ProfileActivationResult
{
    public required AudioProfile Profile { get; init; }
    public ActivationOutcomeKind Outcome { get; init; }
    public DeviceSwitchResult Output { get; init; } = new() { Requested = new SavedDeviceReference(), Succeeded = false };
    public DeviceSwitchResult Input { get; init; } = new() { Requested = new SavedDeviceReference(), Succeeded = false };
    public string Summary { get; init; } = string.Empty;
}

public readonly record struct RoleAssignment(AudioFlow Flow, AudioRole Role, SavedDeviceReference Device);
