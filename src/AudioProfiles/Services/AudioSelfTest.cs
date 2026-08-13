using System.Text;
using AudioProfiles.Interop;
using AudioProfiles.Models;

namespace AudioProfiles.Services;

internal static class AudioSelfTest
{
    public static bool Run()
    {
        NativeMethods.AttachConsole(NativeMethods.AttachParentProcess);
        NativeMethods.CoInitializeEx(nint.Zero, NativeMethods.CoInitApartmentThreaded);

        var log = new AppLog();
        var output = new StringBuilder();
        void Write(string line)
        {
            output.AppendLine(line);
            try
            {
                Console.WriteLine(line);
            }
            catch
            {
            }
        }

        try
        {
            using var audio = new AudioDeviceService(log);
            var outputs = audio.GetDevices(AudioFlow.Playback).Where(d => d.Availability == DeviceAvailability.Available).ToList();
            var inputs = audio.GetDevices(AudioFlow.Recording).Where(d => d.Availability == DeviceAvailability.Available).ToList();
            Write($"Playback devices: {outputs.Count}");
            foreach (var device in outputs)
            {
                Write($"  OUT {device.Name} [{device.Id}]");
            }

            Write($"Capture devices: {inputs.Count}");
            foreach (var device in inputs)
            {
                Write($"  IN  {device.Name} [{device.Id}]");
            }

            var before = audio.GetCurrentDefaults();
            Write($"Current defaults: out={before.OutputId} in={before.InputId}");
            if (outputs.Count == 0 || inputs.Count == 0)
            {
                Write("Need at least one playback device and one capture device.");
                Persist(output, false);
                return false;
            }

            var originalOutput = outputs.FirstOrDefault(d => string.Equals(d.Id, before.OutputId, StringComparison.OrdinalIgnoreCase)) ?? outputs[0];
            var originalInput = inputs.FirstOrDefault(d => string.Equals(d.Id, before.InputId, StringComparison.OrdinalIgnoreCase)) ?? inputs[0];
            var targetOutput = outputs.FirstOrDefault(d => !string.Equals(d.Id, originalOutput.Id, StringComparison.OrdinalIgnoreCase)) ?? originalOutput;
            var targetInput = inputs.FirstOrDefault(d => !string.Equals(d.Id, originalInput.Id, StringComparison.OrdinalIgnoreCase)) ?? originalInput;

            var switchOut = audio.SetDefaultDevice(new SavedDeviceReference { Id = targetOutput.Id, Name = targetOutput.Name }, AudioFlow.Playback);
            var switchIn = audio.SetDefaultDevice(new SavedDeviceReference { Id = targetInput.Id, Name = targetInput.Name }, AudioFlow.Recording);
            var after = audio.GetCurrentDefaults();
            Write($"Switch output {targetOutput.Name}: {switchOut.Succeeded}");
            Write($"Switch input {targetInput.Name}: {switchIn.Succeeded}");
            Write($"Defaults after switch: out={after.OutputId} in={after.InputId}");

            var restoreOut = audio.SetDefaultDevice(new SavedDeviceReference { Id = originalOutput.Id, Name = originalOutput.Name }, AudioFlow.Playback);
            var restoreIn = audio.SetDefaultDevice(new SavedDeviceReference { Id = originalInput.Id, Name = originalInput.Name }, AudioFlow.Recording);
            var restored = audio.GetCurrentDefaults();
            Write($"Restore output {originalOutput.Name}: {restoreOut.Succeeded}");
            Write($"Restore input {originalInput.Name}: {restoreIn.Succeeded}");
            Write($"Defaults after restore: out={restored.OutputId} in={restored.InputId}");

            var switched = switchOut.Succeeded && switchIn.Succeeded &&
                           string.Equals(after.OutputId, targetOutput.Id, StringComparison.OrdinalIgnoreCase) &&
                           string.Equals(after.InputId, targetInput.Id, StringComparison.OrdinalIgnoreCase);
            var restoredOk = restoreOut.Succeeded && restoreIn.Succeeded &&
                             string.Equals(restored.OutputId, originalOutput.Id, StringComparison.OrdinalIgnoreCase) &&
                             string.Equals(restored.InputId, originalInput.Id, StringComparison.OrdinalIgnoreCase);
            var pass = switched && restoredOk;
            Write(pass ? "SELFTEST PASS" : "SELFTEST FAIL");
            Persist(output, pass);
            return pass;
        }
        catch (Exception ex)
        {
            Write(ex.ToString());
            Persist(output, false);
            return false;
        }
    }

    private static void Persist(StringBuilder output, bool pass)
    {
        try
        {
            var directory = Path.Combine(AppContext.BaseDirectory, "self-test");
            Directory.CreateDirectory(directory);
            File.WriteAllText(Path.Combine(directory, "result.txt"), output + (pass ? "PASS" : "FAIL") + Environment.NewLine);
        }
        catch
        {
        }
    }
}
