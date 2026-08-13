using System.Runtime.InteropServices;
using AudioProfiles.Interop;
using AudioProfiles.Models;

namespace AudioProfiles.Services;

public sealed class HotkeyService : IDisposable
{
    private readonly AppLog _log;
    private readonly Dictionary<int, string> _hotkeyIds = [];
    private IReadOnlyList<AudioProfile> _profiles = [];
    private nint _hwnd;
    private NativeMethods.WndProc? _wndProc;
    private nint _classAtom;
    private bool _disposed;

    public event EventHandler<string>? HotkeyPressed;

    public HotkeyService(AppLog log)
    {
        _log = log;
        CreateMessageWindow();
    }

    public void RegisterProfiles(IEnumerable<AudioProfile> profiles)
    {
        _profiles = profiles.ToList();
        UnregisterAll();
        foreach (var profile in profiles)
        {
            if (!profile.Hotkey.Enabled || !profile.Hotkey.HasKey)
            {
                continue;
            }

            var id = Math.Abs(profile.Id.GetHashCode()) % 0xBFFF + 1;
            while (_hotkeyIds.ContainsKey(id))
            {
                id++;
            }

            var modifiers = NativeMethods.ModNoRepeat;
            if (profile.Hotkey.Alt) modifiers |= NativeMethods.ModAlt;
            if (profile.Hotkey.Control) modifiers |= NativeMethods.ModControl;
            if (profile.Hotkey.Shift) modifiers |= NativeMethods.ModShift;
            if (profile.Hotkey.Windows) modifiers |= NativeMethods.ModWin;

            if (!NativeMethods.RegisterHotKey(_hwnd, id, modifiers, (uint)profile.Hotkey.VirtualKey))
            {
                var error = Marshal.GetLastWin32Error();
                _log.Error($"Failed to register hotkey for '{profile.Name}'. Win32={error}");
                continue;
            }

            _hotkeyIds[id] = profile.Id;
        }
    }

    public bool TryRegister(HotkeyBinding binding, out string? errorKey)
    {
        errorKey = null;
        if (!binding.Enabled || !binding.HasKey)
        {
            return true;
        }

        if (LooksLikeReserved(binding))
        {
            errorKey = "ShortcutInvalid";
            return false;
        }

        var modifiers = NativeMethods.ModNoRepeat;
        if (binding.Alt) modifiers |= NativeMethods.ModAlt;
        if (binding.Control) modifiers |= NativeMethods.ModControl;
        if (binding.Shift) modifiers |= NativeMethods.ModShift;
        if (binding.Windows) modifiers |= NativeMethods.ModWin;

        UnregisterAll();
        const int probeId = 0x7FFE;
        try
        {
            if (!NativeMethods.RegisterHotKey(_hwnd, probeId, modifiers, (uint)binding.VirtualKey))
            {
                errorKey = "ShortcutInUse";
                return false;
            }

            NativeMethods.UnregisterHotKey(_hwnd, probeId);
            return true;
        }
        finally
        {
            RegisterProfiles(_profiles);
        }
    }

    public static bool LooksLikeReserved(HotkeyBinding binding)
    {
        if (!binding.HasKey)
        {
            return false;
        }

        var key = binding.VirtualKey;
        if (key is >= 0x70 and <= 0x7B && !binding.Control && !binding.Alt && !binding.Shift)
        {
            return true;
        }

        return key is 0x5B or 0x5C or 0x5D;
    }

    public void UnregisterAll()
    {
        foreach (var id in _hotkeyIds.Keys)
        {
            NativeMethods.UnregisterHotKey(_hwnd, id);
        }

        _hotkeyIds.Clear();
    }

    private void CreateMessageWindow()
    {
        _wndProc = WndProc;
        var className = "AudioProfilesHotkeyWindow";
        var wndClass = new NativeMethods.WndClassEx
        {
            cbSize = (uint)Marshal.SizeOf<NativeMethods.WndClassEx>(),
            lpfnWndProc = Marshal.GetFunctionPointerForDelegate(_wndProc),
            hInstance = NativeMethods.GetModuleHandle(null),
            lpszClassName = className,
            style = NativeMethods.CsHRedraw | NativeMethods.CsVRedraw
        };
        _classAtom = NativeMethods.RegisterClassEx(ref wndClass);
        _hwnd = NativeMethods.CreateWindowEx(
            NativeMethods.WsExNoActivate | NativeMethods.WsExToolWindow,
            className,
            "AudioProfilesHotkeys",
            NativeMethods.WsPopup,
            0, 0, 0, 0,
            nint.Zero, nint.Zero, wndClass.hInstance, nint.Zero);
        if (_hwnd == nint.Zero)
        {
            _log.Error("Failed to create the hotkey message window.");
        }
    }

    private nint WndProc(nint hWnd, uint msg, nint wParam, nint lParam)
    {
        if (msg == NativeMethods.WmHotkey)
        {
            var id = wParam.ToInt32();
            if (_hotkeyIds.TryGetValue(id, out var profileId))
            {
                HotkeyPressed?.Invoke(this, profileId);
            }
            return nint.Zero;
        }

        return NativeMethods.DefWindowProc(hWnd, msg, wParam, lParam);
    }

    public void Dispose()
    {
        if (_disposed)
        {
            return;
        }

        _disposed = true;
        UnregisterAll();
        if (_hwnd != nint.Zero)
        {
            NativeMethods.DestroyWindow(_hwnd);
            _hwnd = nint.Zero;
        }
    }
}
