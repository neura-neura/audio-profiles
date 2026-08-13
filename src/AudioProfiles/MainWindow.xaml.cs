using AudioProfiles.Helpers;
using AudioProfiles.Services;
using AudioProfiles.Views;
using AudioProfiles.Interop;
using Microsoft.UI.Windowing;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Windows.Graphics;

namespace AudioProfiles;

public sealed partial class MainWindow : Window
{
    private readonly AppController _controller;
    public MainWindow(AppController controller)
    {
        _controller = controller;
        InitializeComponent();

        ExtendsContentIntoTitleBar = true;
        SetTitleBar(AppTitleBar);
        AppWindow.SetIcon("Assets/AppIcon.ico");
        Title = Loc.Get("AppName");
        AppTitleBar.Title = Loc.Get("AppName");
        ProfilesNavItem.Content = Loc.Get("Profiles");
        SettingsNavItem.Content = Loc.Get("Settings");

        ApplyTheme();
        RestoreBounds();
        ContentFrame.Navigate(typeof(ProfilesPage));
        _controller.StateChanged += (_, _) => DispatcherQueue.TryEnqueue(ApplyTheme);
    }

    public void ApplyTheme()
    {
        if (Content is FrameworkElement root)
        {
            root.RequestedTheme = _controller.ResolveElementTheme();
        }
    }

    public void NavigateToProfiles()
    {
        if (!ReferenceEquals(RootNavigation.SelectedItem, ProfilesNavItem))
        {
            RootNavigation.SelectedItem = ProfilesNavItem;
        }

        if (ContentFrame.Content is not ProfilesPage)
        {
            ContentFrame.Navigate(typeof(ProfilesPage));
        }
    }

    public void NavigateToSettings()
    {
        if (!ReferenceEquals(RootNavigation.SelectedItem, SettingsNavItem))
        {
            RootNavigation.SelectedItem = SettingsNavItem;
        }

        if (ContentFrame.Content is not SettingsPage)
        {
            ContentFrame.Navigate(typeof(SettingsPage));
        }
    }

    public void NavigateToEditor(string? profileId)
    {
        ContentFrame.Navigate(typeof(EditProfilePage), profileId);
    }

    public void PrepareHiddenStart()
    {
        AppWindow.Hide();
    }

    public void HideToTray()
    {
        SaveBounds();
        AppWindow.Hide();
    }

    public void RestoreFromTray()
    {
        if (AppWindow.Presenter is OverlappedPresenter presenter)
        {
            presenter.Restore();
        }

        AppWindow.Show();
        AppWindow.MoveInZOrderAtTop();
        Activate();
        BringNativeWindowToForeground();
    }

    private void BringNativeWindowToForeground()
    {
        var hwnd = WinRT.Interop.WindowNative.GetWindowHandle(this);
        if (hwnd == nint.Zero)
        {
            return;
        }

        NativeMethods.AllowSetForegroundWindow(-1);
        NativeMethods.ShowWindow(hwnd, NativeMethods.SwRestore);
        NativeMethods.BringWindowToTop(hwnd);
        NativeMethods.SetForegroundWindow(hwnd);
    }

    public void ForceClose()
    {
        SaveBounds();
        Close();
    }

    private void RestoreBounds()
    {
        var settings = _controller.Settings;
        if (settings.WindowLeft is null || settings.WindowTop is null)
        {
            AppWindow.Resize(new SizeInt32((int)settings.WindowWidth, (int)settings.WindowHeight));
            return;
        }

        AppWindow.MoveAndResize(new RectInt32(
            (int)settings.WindowLeft.Value,
            (int)settings.WindowTop.Value,
            Math.Max(720, (int)settings.WindowWidth),
            Math.Max(560, (int)settings.WindowHeight)));
    }

    private void SaveBounds()
    {
        var area = AppWindow.Position;
        var size = AppWindow.Size;
        _controller.Settings.WindowLeft = area.X;
        _controller.Settings.WindowTop = area.Y;
        _controller.Settings.WindowWidth = size.Width;
        _controller.Settings.WindowHeight = size.Height;
        _controller.Persist();
    }

    private void RootNavigation_SelectionChanged(NavigationView sender, NavigationViewSelectionChangedEventArgs args)
    {
        if (args.SelectedItem is not NavigationViewItem item || item.Tag is not string tag)
        {
            return;
        }

        if (tag == "settings")
        {
            NavigateToSettings();
        }
        else
        {
            NavigateToProfiles();
        }
    }
}
