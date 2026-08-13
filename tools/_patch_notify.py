from pathlib import Path
p = Path(r'C:\\Users\\neura\\repos\\audio-device-switcher\\src\\AudioProfiles\\Services\\NotificationService.cs')
p.write_text(r'''using AudioProfiles.Helpers;
using AudioProfiles.Interop;
using AudioProfiles.Models;
using Microsoft.Windows.AppNotifications;
using Microsoft.Windows.AppNotifications.Builder;

namespace AudioProfiles.Services;

public sealed class NotificationService
{
    private readonly AppLog _log;
    private bool _registered;
    private bool _nativeFallback;

    public NotificationService(AppLog log)
    {
        _log = log;
    }

    public void Initialize()
    {
        try
        {
            if (!AppNotificationManager.IsSupported())
            {
                _nativeFallback = true;
                _log.Info("Windows App SDK notifications are not supported. Using native Windows toasts.");
                return;
            }

            AppNotificationManager.Default.Register();
            _registered = true;
            _nativeFallback = false;
            _log.Info(AppIdentity.IsPackaged()
                ? "Registered packaged Windows App SDK notifications."
                : "Registered unpackaged Windows App SDK notifications.");
        }
        catch (Exception ex)
        {
            _registered = false;
            _nativeFallback = true;
            _log.Warn($"Windows App SDK notification registration failed; native toasts will be used. {ex.Message}");
        }
    }

    public void ShowActivation(ProfileActivationResult result)
    {
        var titleKey = result.Outcome switch
        {
            ActivationOutcomeKind.Success => "ActivatedTitle",
            ActivationOutcomeKind.Partial => "PartialTitle",
            _ => "FailedTitle"
        };
        Show(Loc.Format(titleKey, result.Profile.Name), result.Summary);
    }

    public void Show(string title, string body)
    {
        if (_registered)
        {
            try
            {
                var notification = new AppNotificationBuilder()
                    .AddText(title)
                    .AddText(body)
                    .BuildNotification();
                notification.ExpiresOnReboot = true;
                AppNotificationManager.Default.Show(notification);
                _log.Info($"Windows App SDK notification shown: {title}");
                return;
            }
            catch (Exception ex)
            {
                _log.Warn($"Windows App SDK notification show failed; using native toast. {ex.Message}");
            }
        }

        try
        {
            NativeToast.Show(title, body);
            _nativeFallback = true;
            _log.Info($"Windows notification shown: {title}");
        }
        catch (Exception ex)
        {
            _log.Error("Failed to show a Windows notification.", ex);
        }
    }

    public void Shutdown()
    {
        if (!_registered)
        {
            return;
        }

        try
        {
            AppNotificationManager.Default.Unregister();
        }
        catch (Exception ex)
        {
            _log.Error("Failed to unregister Windows notifications.", ex);
        }
    }
}
''', encoding='utf-8')
print('NotificationService written')
