from pathlib import Path
root = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles")
root.joinpath("Program.cs").write_text(r'''using AudioProfiles.Services;
using Microsoft.UI.Dispatching;
using Microsoft.UI.Xaml;
using Microsoft.Windows.AppLifecycle;

namespace AudioProfiles;

public static class Program
{
    public const string InstanceKey = "AudioProfiles.SingleInstance";

    [STAThread]
    private static void Main(string[] args)
    {
        if (args.Any(a => string.Equals(a, "--self-test", StringComparison.OrdinalIgnoreCase)))
        {
            Environment.ExitCode = AudioSelfTest.Run() ? 0 : 1;
            return;
        }

        WinRT.ComWrappersSupport.InitializeComWrappers();

        var current = AppInstance.GetCurrent();
        var mainInstance = AppInstance.FindOrRegisterForKey(InstanceKey);
        if (!mainInstance.IsCurrent)
        {
            mainInstance.RedirectActivationToAsync(current.GetActivatedEventArgs()).AsTask().GetAwaiter().GetResult();
            return;
        }

        Application.Start(_ =>
        {
            var context = new DispatcherQueueSynchronizationContext(DispatcherQueue.GetForCurrentThread());
            SynchronizationContext.SetSynchronizationContext(context);
            _ = new App();
        });
    }
}
''', encoding='utf-8', newline='\n')
print('wrote Program.cs')
