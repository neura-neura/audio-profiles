using AudioProfiles.Models;
using Windows.ApplicationModel;

namespace AudioProfiles.Services;

public sealed class StartupService
{
    private readonly AppLog _log;
    private const string TaskId = "AudioProfilesStartup";

    public StartupService(AppLog log)
    {
        _log = log;
    }

    public async Task ApplyAsync(AppSettings settings)
    {
        try
        {
            if (IsPackaged())
            {
                var task = await StartupTask.GetAsync(TaskId);
                if (settings.StartWithWindows)
                {
                    if (task.State is StartupTaskState.Disabled)
                    {
                        await task.RequestEnableAsync();
                    }
                }
                else if (task.State is StartupTaskState.Enabled or StartupTaskState.EnabledByPolicy)
                {
                    task.Disable();
                }
                return;
            }

            ApplyStartupShortcut(settings.StartWithWindows);
        }
        catch (Exception ex)
        {
            _log.Error("Failed to update Start with Windows.", ex);
            ApplyStartupShortcut(settings.StartWithWindows);
        }
    }

    public bool WasStartedByWindows()
    {
        try
        {
            var args = Program.LaunchArgs.Concat(Environment.GetCommandLineArgs());
            if (args.Any(a => a.Contains("startup", StringComparison.OrdinalIgnoreCase)))
            {
                return true;
            }
        }
        catch
        {
            // Ignore.
        }

        return false;
    }

    public bool ShouldShowInForeground()
    {
        try
        {
            return Program.LaunchArgs
                .Concat(Environment.GetCommandLineArgs())
                .Any(a => string.Equals(a, "--foreground", StringComparison.OrdinalIgnoreCase));
        }
        catch
        {
            return false;
        }
    }

    private void ApplyStartupShortcut(bool enabled)
    {
        try
        {
            var startupFolder = Environment.GetFolderPath(Environment.SpecialFolder.Startup);
            var shortcutPath = Path.Combine(startupFolder, "Audio Profiles.lnk");
            if (!enabled)
            {
                if (File.Exists(shortcutPath))
                {
                    File.Delete(shortcutPath);
                }
                return;
            }

            var exe = Environment.ProcessPath;
            if (string.IsNullOrWhiteSpace(exe))
            {
                return;
            }

            var shellType = Type.GetTypeFromProgID("WScript.Shell");
            if (shellType is null)
            {
                _log.Error("WScript.Shell is unavailable for startup shortcut creation.");
                return;
            }

            dynamic shell = Activator.CreateInstance(shellType)!;
            dynamic shortcut = shell.CreateShortcut(shortcutPath);
            shortcut.TargetPath = exe;
            shortcut.WorkingDirectory = Path.GetDirectoryName(exe);
            shortcut.Arguments = "--startup";
            shortcut.Description = "Audio Profiles";
            shortcut.Save();
        }
        catch (Exception ex)
        {
            _log.Error("Failed to create or remove the startup shortcut.", ex);
        }
    }

    private static bool IsPackaged()
    {
        return AppIdentity.IsPackaged();
    }
}
