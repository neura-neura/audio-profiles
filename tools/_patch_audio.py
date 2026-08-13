from pathlib import Path
p = Path(r'C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Services\AudioDeviceService.cs')
text = p.read_text(encoding='utf-8')
old = '''    public DeviceSwitchResult SetDefaultDevice(SavedDeviceReference reference, AudioFlow flow, bool applyAllRoles = true)
    {
        if (string.IsNullOrWhiteSpace(reference.Id))
        {
            return new DeviceSwitchResult
            {
                Requested = reference,
                Succeeded = false,
                ErrorMessage = Loc.Format("DeviceUnavailable", reference.Name)
            };
        }

        var device = FindDevice(flow, reference.Id);
        if (device is null || device.Availability != DeviceAvailability.Available)
        {
            var name = string.IsNullOrWhiteSpace(reference.Name) ? reference.Id : reference.Name;
            return new DeviceSwitchResult
            {
                Requested = reference,
                Succeeded = false,
                ErrorMessage = Loc.Format("DeviceUnavailable", name)
            };
        }

        try
        {
            var roles = applyAllRoles
                ? new[] { ERole.eConsole, ERole.eMultimedia, ERole.eCommunications }
                : new[] { ERole.eMultimedia };
            MmDeviceNative.SetDefaultEndpoint(device.Id, roles, _log);
            return new DeviceSwitchResult
            {
                Requested = new SavedDeviceReference { Id = device.Id, Name = device.Name },
                Succeeded = true
            };
        }
        catch (Exception ex)
        {
            _log.Error($"Failed to set default {flow} device '{device.Name}'.", ex);
            return new DeviceSwitchResult
            {
                Requested = reference,
                Succeeded = false,
                ErrorMessage = Loc.Format("DeviceUnavailable", device.Name)
            };
        }
    }
'''
new = '''    public DeviceSwitchResult SetDefaultDevice(SavedDeviceReference reference, AudioFlow flow, bool applyAllRoles = true)
    {
        var roles = applyAllRoles
            ? new[] { AudioRole.Console, AudioRole.Multimedia, AudioRole.Communications }
            : new[] { AudioRole.Multimedia };
        return SetDefaultDevice(reference, flow, roles);
    }

    public DeviceSwitchResult SetDefaultDevice(SavedDeviceReference reference, AudioFlow flow, AudioRole role) =>
        SetDefaultDevice(reference, flow, [role]);

    public DeviceSwitchResult SetDefaultDevice(SavedDeviceReference reference, AudioFlow flow, IReadOnlyList<AudioRole> roles)
    {
        if (string.IsNullOrWhiteSpace(reference.Id))
        {
            return new DeviceSwitchResult
            {
                Requested = reference,
                Succeeded = false,
                ErrorMessage = Loc.Format("DeviceUnavailable", reference.Name)
            };
        }

        var device = FindDevice(flow, reference.Id);
        if (device is null || device.Availability != DeviceAvailability.Available)
        {
            var name = string.IsNullOrWhiteSpace(reference.Name) ? reference.Id : reference.Name;
            return new DeviceSwitchResult
            {
                Requested = reference,
                Succeeded = false,
                ErrorMessage = Loc.Format("DeviceUnavailable", name)
            };
        }

        try
        {
            var nativeRoles = roles.Select(ToNativeRole).ToArray();
            MmDeviceNative.SetDefaultEndpoint(device.Id, nativeRoles, _log);
            return new DeviceSwitchResult
            {
                Requested = new SavedDeviceReference { Id = device.Id, Name = device.Name },
                Succeeded = true
            };
        }
        catch (Exception ex)
        {
            _log.Error($"Failed to set default {flow} device '{device.Name}'.", ex);
            return new DeviceSwitchResult
            {
                Requested = reference,
                Succeeded = false,
                ErrorMessage = Loc.Format("DeviceUnavailable", device.Name)
            };
        }
    }

    public (string? ConsoleId, string? MultimediaId, string? CommunicationsId) GetDefaultIds(AudioFlow flow)
    {
        var dataFlow = flow == AudioFlow.Playback ? EDataFlow.eRender : EDataFlow.eCapture;
        var defaults = GetDefaultIds(dataFlow);
        return (defaults.Console, defaults.Multimedia, defaults.Communications);
    }

    private static ERole ToNativeRole(AudioRole role) => role switch
    {
        AudioRole.Console => ERole.eConsole,
        AudioRole.Communications => ERole.eCommunications,
        _ => ERole.eMultimedia
    };
'''
if old not in text:
    raise SystemExit('SetDefaultDevice block not found')
p.write_text(text.replace(old, new, 1), encoding='utf-8')
print('AudioDeviceService updated')
