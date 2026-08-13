using System.Runtime.InteropServices;

namespace AudioProfiles.Interop;

internal static class NativeMethods
{
    public const int WmHotkey = 0x0312;
    public const int WmTrayIcon = 0x8001;
    public const int WmCommand = 0x0111;
    public const int WmDestroy = 0x0002;
    public const int WmClose = 0x0010;
    public const int WmLButtonUp = 0x0202;
    public const int WmRButtonUp = 0x0205;
    public const int WmContextMenu = 0x007B;
    public const int WmApp = 0x8000;
    public const int NimAdd = 0x00000000;
    public const int NimModify = 0x00000001;
    public const int NimDelete = 0x00000002;
    public const int NimSetVersion = 0x00000004;
    public const int NieNotifyIconVersion4 = 4;
    public const int NifMessage = 0x00000001;
    public const int NifIcon = 0x00000002;
    public const int NifTip = 0x00000004;
    public const int NifShowTip = 0x00000080;
    public const int MfString = 0x00000000;
    public const int MfSeparator = 0x00000800;
    public const int MfChecked = 0x00000008;
    public const int MfGrayed = 0x00000001;
    public const int TpmRightButton = 0x0002;
    public const int TpmBottomAlign = 0x0020;
    public const int TpmReturnCmd = 0x0100;
    public const int SwHide = 0;
    public const int SwShow = 5;
    public const int SwRestore = 9;
    public const int CsHRedraw = 0x0002;
    public const int CsVRedraw = 0x0001;
    public const int WsExNoActivate = 0x08000000;
    public const int WsExToolWindow = 0x00000080;
    public const int WsPopup = unchecked((int)0x80000000);
    public const int CwUseDefault = unchecked((int)0x80000000);
    public const uint ModAlt = 0x0001;
    public const uint ModControl = 0x0002;
    public const uint ModShift = 0x0004;
    public const uint ModWin = 0x0008;
    public const uint ModNoRepeat = 0x4000;
    public const int IdiApplication = 32512;
    public const uint ImageIcon = 1;
    public const uint LrDefaultSize = 0x00000040;
    public const uint LrLoadFromFile = 0x00000010;
    public const int GwlpWndProc = -4;

    public delegate nint WndProc(nint hWnd, uint msg, nint wParam, nint lParam);

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct NotifyIconData
    {
        public int cbSize;
        public nint hWnd;
        public uint uID;
        public uint uFlags;
        public uint uCallbackMessage;
        public nint hIcon;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 128)]
        public string szTip;
        public uint dwState;
        public uint dwStateMask;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)]
        public string szInfo;
        public uint uVersion;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 64)]
        public string szInfoTitle;
        public uint dwInfoFlags;
        public Guid guidItem;
        public nint hBalloonIcon;
    }

    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
    public struct WndClassEx
    {
        public uint cbSize;
        public uint style;
        public nint lpfnWndProc;
        public int cbClsExtra;
        public int cbWndExtra;
        public nint hInstance;
        public nint hIcon;
        public nint hCursor;
        public nint hbrBackground;
        public string? lpszMenuName;
        public string lpszClassName;
        public nint hIconSm;
    }

    [StructLayout(LayoutKind.Sequential)]
    public struct Point
    {
        public int X;
        public int Y;
    }

    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern ushort RegisterClassEx(ref WndClassEx lpwcx);

    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern nint CreateWindowEx(
        int dwExStyle,
        string lpClassName,
        string lpWindowName,
        int dwStyle,
        int x,
        int y,
        int nWidth,
        int nHeight,
        nint hWndParent,
        nint hMenu,
        nint hInstance,
        nint lpParam);

    [DllImport("user32.dll")]
    public static extern nint DefWindowProc(nint hWnd, uint msg, nint wParam, nint lParam);

    [DllImport("user32.dll")]
    public static extern bool DestroyWindow(nint hWnd);

    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool RegisterHotKey(nint hWnd, int id, uint fsModifiers, uint vk);

    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool UnregisterHotKey(nint hWnd, int id);

    [DllImport("shell32.dll", CharSet = CharSet.Unicode)]
    public static extern bool Shell_NotifyIcon(uint dwMessage, ref NotifyIconData lpData);

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern nint LoadImage(nint hInst, string name, uint type, int cx, int cy, uint fuLoad);

    [DllImport("user32.dll")]
    public static extern nint LoadIcon(nint hInstance, nint lpIconName);

    [DllImport("user32.dll")]
    public static extern bool DestroyIcon(nint hIcon);

    [DllImport("user32.dll")]
    public static extern nint CreatePopupMenu();

    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    public static extern bool AppendMenu(nint hMenu, uint uFlags, nuint uIDNewItem, string lpNewItem);

    [DllImport("user32.dll")]
    public static extern bool DestroyMenu(nint hMenu);

    [DllImport("user32.dll")]
    public static extern uint TrackPopupMenuEx(nint hmenu, uint fuFlags, int x, int y, nint hwnd, nint lptpm);

    [DllImport("user32.dll")]
    public static extern bool GetCursorPos(out Point lpPoint);

    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(nint hWnd);

    [DllImport("user32.dll")]
    public static extern bool ShowWindow(nint hWnd, int nCmdShow);

    [DllImport("user32.dll")]
    public static extern bool BringWindowToTop(nint hWnd);

    [DllImport("user32.dll")]
    public static extern bool AllowSetForegroundWindow(int dwProcessId);

    [DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
    public static extern nint GetModuleHandle(string? lpModuleName);

    [DllImport("ole32.dll")]
    public static extern int CoCreateInstance(
        ref Guid rclsid,
        nint pUnkOuter,
        uint dwClsContext,
        ref Guid riid,
        out nint ppv);

    public const uint ClsctxInprocServer = 1;
    public const int AttachParentProcess = -1;
    public const uint CoInitApartmentThreaded = 0x2;

    [DllImport("kernel32.dll")]
    public static extern bool AttachConsole(int dwProcessId);

    [DllImport("ole32.dll")]
    public static extern int CoInitializeEx(nint pvReserved, uint dwCoInit);

    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    public static extern nint LoadLibrary(string lpFileName);

    [DllImport("shell32.dll", CharSet = CharSet.Unicode)]
    public static extern int SetCurrentProcessExplicitAppUserModelID(string appID);

    public static nint LowWord(nint value) => value & 0xFFFF;
    public static nint HighWord(nint value) => (value >> 16) & 0xFFFF;
}
