using AudioProfiles.Helpers;
using AudioProfiles.Models;
using Microsoft.UI.Dispatching;

namespace AudioProfiles.Services;

public sealed class AppController : IDisposable
{
    private readonly DispatcherQueue _dispatcher;
    private readonly SettingsStore _store;
    private readonly ProfileActivationService _activation;
    private bool _disposed;

    public AppController(DispatcherQueue dispatcher)
    {
        _dispatcher = dispatcher;
        Log = new AppLog();
        _store = new SettingsStore(Log);
        State = _store.Load();
        Audio = new AudioDeviceService(Log);
        _activation = new ProfileActivationService(Audio, Log);
        Notifications = new NotificationService(Log);
        Hotkeys = new HotkeyService(Log);
        Tray = new TrayService(Log);
        Startup = new StartupService(Log);

        Audio.DevicesChanged += (_, _) => RunOnUi(RefreshFromHardware);
        Hotkeys.HotkeyPressed += (_, profileId) => RunOnUi(() => ActivateProfile(profileId));
        Tray.OpenRequested += (_, _) => OpenRequested?.Invoke(this, EventArgs.Empty);
        Tray.ExitRequested += (_, _) => ExitRequested?.Invoke(this, EventArgs.Empty);
        Tray.ProfileRequested += (_, profileId) => RunOnUi(() => ActivateProfile(profileId));
    }

    public AppLog Log { get; }
    public AppState State { get; }
    public AudioDeviceService Audio { get; }
    public NotificationService Notifications { get; }
    public HotkeyService Hotkeys { get; }
    public TrayService Tray { get; }
    public StartupService Startup { get; }

    public event EventHandler? StateChanged;
    public event EventHandler? OpenRequested;
    public event EventHandler? ExitRequested;

    public IReadOnlyList<AudioProfile> Profiles => State.Profiles;
    public AppSettings Settings => State.Settings;

    public async Task InitializeAsync()
    {
        Log.Info("Application startup.");
        Log.Verbose = Settings.WriteDetailedLogs;
        Notifications.Initialize();
        await Startup.ApplyAsync(Settings);
        RefreshFromHardware();
        Hotkeys.RegisterProfiles(State.Profiles);
        Tray.Update(State.Profiles, DetectActiveProfileId());
    }

    public string DetectActiveProfileId()
    {
        var match = State.Profiles.FirstOrDefault(_activation.MatchesCurrentDefaults);
        return match?.Id ?? string.Empty;
    }

    public string CurrentProfileName()
    {
        var id = DetectActiveProfileId();
        return string.IsNullOrEmpty(id)
            ? Loc.Get("CustomProfile")
            : State.Profiles.FirstOrDefault(p => p.Id == id)?.Name ?? Loc.Get("CustomProfile");
    }

    public ProfileActivationResult ActivateProfile(string profileId)
    {
        var profile = State.Profiles.FirstOrDefault(p => p.Id == profileId);
        if (profile is null)
        {
            Log.Warn($"Activation requested for unknown profile '{profileId}'.");
            return new ProfileActivationResult
            {
                Profile = new AudioProfile { Name = Loc.Get("CustomProfile") },
                Outcome = ActivationOutcomeKind.Failed,
                Summary = Loc.Get("FailedTitle")
            };
        }

        var result = _activation.Activate(profile);
        if (result.Outcome != ActivationOutcomeKind.Failed)
        {
            Settings.LastActivatedProfileId = profile.Id;
            Persist();
        }

        RefreshFromHardware();
        if (Settings.ShowNotifications)
        {
            Notifications.ShowActivation(result);
        }

        return result;
    }

    public void AddOrUpdateProfile(AudioProfile profile)
    {
        var existing = State.Profiles.FindIndex(p => p.Id == profile.Id);
        if (existing >= 0)
        {
            State.Profiles[existing] = profile;
        }
        else
        {
            State.Profiles.Add(profile);
        }

        PersistAndBroadcast();
    }

    public void DeleteProfile(string profileId)
    {
        State.Profiles.RemoveAll(p => p.Id == profileId);
        if (Settings.LastActivatedProfileId == profileId)
        {
            Settings.LastActivatedProfileId = null;
        }

        PersistAndBroadcast();
    }

    public void Persist()
    {
        try
        {
            _store.Save(State);
        }
        catch (Exception ex)
        {
            Log.Error("Failed to save configuration.", ex);
        }
    }

    public void PersistAndBroadcast()
    {
        Persist();
        Hotkeys.RegisterProfiles(State.Profiles);
        Tray.Update(State.Profiles, DetectActiveProfileId());
        StateChanged?.Invoke(this, EventArgs.Empty);
    }

    public void RefreshFromHardware()
    {
        Tray.Update(State.Profiles, DetectActiveProfileId());
        StateChanged?.Invoke(this, EventArgs.Empty);
    }

    public void ApplyTheme(Microsoft.UI.Xaml.Application app)
    {
        _ = app;
    }

    public Microsoft.UI.Xaml.ElementTheme ResolveElementTheme() => Settings.Theme switch
    {
        AppTheme.Light => Microsoft.UI.Xaml.ElementTheme.Light,
        AppTheme.Dark => Microsoft.UI.Xaml.ElementTheme.Dark,
        _ => Microsoft.UI.Xaml.ElementTheme.Default
    };

    private void RunOnUi(Action action)
    {
        if (_dispatcher.HasThreadAccess)
        {
            action();
            return;
        }

        _dispatcher.TryEnqueue(() => action());
    }

    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }

        _disposed = true;
        Log.Info("Application shutdown.");
        Audio.Dispose();
        Hotkeys.Dispose();
        Tray.Dispose();
        Notifications.Shutdown();
    }
}
