using System.Text.Json;
using System.Text.Json.Serialization;
using AudioProfiles.Models;

namespace AudioProfiles.Services;

public sealed class SettingsStore
{
    private static readonly JsonSerializerOptions Options = new()
    {
        WriteIndented = true,
        PropertyNameCaseInsensitive = true,
        Converters = { new JsonStringEnumConverter() },
        DefaultIgnoreCondition = JsonIgnoreCondition.WhenWritingNull,
        NumberHandling = JsonNumberHandling.AllowNamedFloatingPointLiterals
    };

    private readonly AppLog _log;
    private readonly string _directory;
    private readonly string _filePath;
    private readonly string _backupPath;

    public SettingsStore(AppLog log)
    {
        _log = log;
        _directory = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "AudioProfiles");
        Directory.CreateDirectory(_directory);
        _filePath = Path.Combine(_directory, "settings.json");
        _backupPath = Path.Combine(_directory, "settings.bak.json");
    }

    public string FilePath => _filePath;

    public AppState Load()
    {
        try
        {
            if (!File.Exists(_filePath))
            {
                _log.Info("No settings file found. Creating a new configuration.");
                var created = new AppState();
                Save(created);
                return created;
            }

            var json = File.ReadAllText(_filePath);
            var state = JsonSerializer.Deserialize<AppState>(json, Options);
            if (state is null)
            {
                throw new InvalidDataException("Settings file deserialized to null.");
            }

            Normalize(state);
            return state;
        }
        catch (Exception ex)
        {
            _log.Error("Failed to load settings.json. Trying backup.", ex);
            try
            {
                if (File.Exists(_backupPath))
                {
                    var json = File.ReadAllText(_backupPath);
                    var state = JsonSerializer.Deserialize<AppState>(json, Options);
                    if (state is not null)
                    {
                        Normalize(state);
                        _log.Warn("Recovered settings from backup.");
                        return state;
                    }
                }
            }
            catch (Exception backupEx)
            {
                _log.Error("Failed to load settings backup.", backupEx);
            }

            var fallback = new AppState();
            try
            {
                Save(fallback);
            }
            catch (Exception saveEx)
            {
                _log.Error("Failed to write a replacement settings file.", saveEx);
            }

            return fallback;
        }
    }

    public void Save(AppState state)
    {
        Directory.CreateDirectory(_directory);
        var json = JsonSerializer.Serialize(state, Options);
        var tempPath = _filePath + ".tmp";
        File.WriteAllText(tempPath, json);
        if (File.Exists(_filePath))
        {
            File.Copy(_filePath, _backupPath, overwrite: true);
        }

        File.Move(tempPath, _filePath, overwrite: true);
    }

    private static void Normalize(AppState state)
    {
        state.Profiles ??= [];
        state.Settings ??= new AppSettings();
        foreach (var profile in state.Profiles)
        {
            profile.Id = string.IsNullOrWhiteSpace(profile.Id) ? Guid.NewGuid().ToString("N") : profile.Id;
            profile.Name ??= string.Empty;
            profile.Output ??= new SavedDeviceReference();
            profile.Input ??= new SavedDeviceReference();
            profile.Hotkey ??= new HotkeyBinding();
        }
    }
}
