using System;
using System.Runtime.InteropServices;

public static class PolicySwitch {
    [DllImport("ole32.dll")] static extern int CoInitializeEx(IntPtr p, uint c);
    [DllImport("ole32.dll")] static extern int CoCreateInstance(ref Guid clsid, IntPtr outer, uint ctx, ref Guid iid, out IntPtr ppv);
    [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate int SetDefault(IntPtr self, [MarshalAs(UnmanagedType.LPWStr)] string id, int role);
    [UnmanagedFunctionPointer(CallingConvention.StdCall)] delegate uint ReleaseFn(IntPtr self);
    public static int Main(string[] args) {
        CoInitializeEx(IntPtr.Zero, 2);
        var clsid = new Guid("870AF99C-171D-4F9E-AF0D-E63DF40C2BC9");
        var iid = new Guid("F8679F50-850A-41CF-9C72-430F290290C8");
        var hr = CoCreateInstance(ref clsid, IntPtr.Zero, 1, ref iid, out var ptr);
        if (hr < 0 || ptr == IntPtr.Zero) { Console.WriteLine("create "+hr); return 1; }
        var vtbl = Marshal.ReadIntPtr(ptr);
        var fn = Marshal.GetDelegateForFunctionPointer<SetDefault>(Marshal.ReadIntPtr(vtbl, 13 * IntPtr.Size));
        foreach (var id in args) {
            for (int role = 0; role < 3; role++) {
                var r = fn(ptr, id, role);
                Console.WriteLine(id + " role " + role + " hr=" + r);
            }
        }
        var rel = Marshal.GetDelegateForFunctionPointer<ReleaseFn>(Marshal.ReadIntPtr(vtbl, 2 * IntPtr.Size));
        rel(ptr);
        return 0;
    }
}
