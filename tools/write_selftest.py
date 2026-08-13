from pathlib import Path
Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Services\AudioSelfTest.cs").write_text(r'''using AudioProfiles.Models;

namespace AudioProfiles.Services;

internal static class AudioSelfTest
{
    public static bool Run()
    {
        using var log = new TemporaryLog();
        using var audio = new AudioDeviceService(log);
        var outputs = audio.GetDevices(AudioFlow.Playback).Where(d => d.Availability == DeviceAvailability.Available).ToList();
        var inputs = audio.GetDevices(AudioFlow.Recording).Where(d => d.Availability == DeviceAvailability.Available).ToList();
        Console.WriteLine($"Playback devices: {outputs.Count}");
        foreach (var device in outputs)
        {
            Console.WriteLine($"  OUT {device.Name} [{device.Id}]");
        }

        Console.WriteLine($"Capture devices: {inputs.Count}");
        foreach (var device in inputs)
        {
            Console.WriteLine($"  IN  {device.Name} [{device.Id}]");
        }

        var before = audio.GetCurrentDefaults();
        Console.WriteLine($"Current defaults: out={before.OutputId} in={before.InputId}");
        if (outputs.Count == 0 || inputs.Count == 0)
        {
            Console.Error.WriteLine("Need at least one playback device and one capture device.");
            return false;
        }

        var originalOutput = outputs.FirstOrDefault(d => string.Equals(d.Id, before.OutputId, StringComparison.OrdinalIgnoreCase)) ?? outputs[0];
        var originalInput = inputs.FirstOrDefault(d => string.Equals(d.Id, before.InputId, StringComparison.OrdinalIgnoreCase)) ?? inputs[0];
        var targetOutput = outputs.FirstOrDefault(d => !string.Equals(d.Id, originalOutput.Id, StringComparison.OrdinalIgnoreCase)) ?? originalOutput;
        var targetInput = inputs.FirstOrDefault(d => !string.Equals(d.Id, originalInput.Id, StringComparison.OrdinalIgnoreCase)) ?? originalInput;

        var switchOut = audio.SetDefaultDevice(new SavedDeviceReference { Id = targetOutput.Id, Name = targetOutput.Name }, AudioFlow.Playback);
        var switchIn = audio.SetDefaultDevice(new SavedDeviceReference { Id = targetInput.Id, Name = targetInput.Name }, AudioFlow.Recording);
        var after = audio.GetCurrentDefaults();
        Console.WriteLine($"Switch output {targetOutput.Name}: {switchOut.Succeeded}");
        Console.WriteLine($"Switch input {targetInput.Name}: {switchIn.Succeeded}");
        Console.WriteLine($"Defaults after switch: out={after.OutputId} in={after.InputId}");

        var restoreOut = audio.SetDefaultDevice(new SavedDeviceReference { Id = originalOutput.Id, Name = originalOutput.Name }, AudioFlow.Playback);
        var restoreIn = audio.SetDefaultDevice(new SavedDeviceReference { Id = originalInput.Id, Name = originalInput.Name }, AudioFlow.Recording);
        var restored = audio.GetCurrentDefaults();
        Console.WriteLine($"Restore output {originalOutput.Name}: {restoreOut.Succeeded}");
        Console.WriteLine($"Restore input {originalInput.Name}: {restoreIn.Succeeded}");
        Console.WriteLine($"Defaults after restore: out={restored.OutputId} in={restored.InputId}");

        var switched = switchOut.Succeeded && switchIn.Succeeded &&
                       string.Equals(after.OutputId, targetOutput.Id, StringComparison.OrdinalIgnoreCase) &&
                       string.Equals(after.InputId, targetInput.Id, StringComparison.OrdinalIgnoreCase);
        var restoredOk = restoreOut.Succeeded && restoreIn.Succeeded &&
                         string.Equals(restored.OutputId, originalOutput.Id, StringComparison.OrdinalIgnoreCase) &&
                         string.Equals(restored.InputId, originalInput.Id, StringComparison.OrdinalIgnoreCase);
        Console.WriteLine(switched && restoredOk ? "SELFTEST PASS" : "SELFTEST FAIL");
        return switched && restoredOk;
    }

    private sealed class TemporaryLog : AppLog, IDisposable
    {
        public void Dispose() { }
    }
}
''', encoding='utf-8', newline='\n')
print('wrote AudioSelfTest.cs')
