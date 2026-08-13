using AudioProfiles.Helpers;
using AudioProfiles.Models;

namespace AudioProfiles.Services;

public sealed class ProfileActivationService
{
    private readonly AudioDeviceService _audio;
    private readonly AppLog _log;

    public ProfileActivationService(AudioDeviceService audio, AppLog log)
    {
        _audio = audio;
        _log = log;
    }

    public ProfileActivationResult Activate(AudioProfile profile)
    {
        var output = ActivateFlow(profile, AudioFlow.Playback);
        var input = ActivateFlow(profile, AudioFlow.Recording);

        var outcome = (output.Succeeded, input.Succeeded) switch
        {
            (true, true) => ActivationOutcomeKind.Success,
            (false, false) => ActivationOutcomeKind.Failed,
            _ => ActivationOutcomeKind.Partial
        };

        var result = new ProfileActivationResult
        {
            Profile = profile,
            Outcome = outcome,
            Output = output,
            Input = input,
            Summary = Describe(AudioFlow.Playback, output) + Environment.NewLine + Describe(AudioFlow.Recording, input)
        };

        if (outcome == ActivationOutcomeKind.Success)
        {
            _log.Info($"Activated profile '{profile.Name}'.");
        }
        else if (outcome == ActivationOutcomeKind.Partial)
        {
            _log.Warn($"Partially activated profile '{profile.Name}'. Output={output.Succeeded} Input={input.Succeeded}");
        }
        else
        {
            _log.Error($"Failed to activate profile '{profile.Name}'.");
        }

        return result;
    }

    public bool MatchesCurrentDefaults(AudioProfile profile)
    {
        if (!profile.UseAdvancedRoles)
        {
            var defaults = _audio.GetCurrentDefaults();
            return SameId(profile.Output.Id, defaults.OutputId) && SameId(profile.Input.Id, defaults.InputId);
        }

        return MatchesAdvanced(profile, AudioFlow.Playback) && MatchesAdvanced(profile, AudioFlow.Recording);
    }

    private DeviceSwitchResult ActivateFlow(AudioProfile profile, AudioFlow flow)
    {
        if (!profile.UseAdvancedRoles)
        {
            return _audio.SetDefaultDevice(PrimaryDevice(profile, flow), flow);
        }

        var assignments = GetAdvancedAssignments(profile, flow).ToList();
        DeviceSwitchResult? lastSuccess = null;
        DeviceSwitchResult? lastFailure = null;
        foreach (var assignment in assignments)
        {
            var result = _audio.SetDefaultDevice(assignment.Device, assignment.Flow, assignment.Role);
            if (result.Succeeded)
            {
                lastSuccess = result;
            }
            else
            {
                lastFailure = result;
            }
        }

        if (lastFailure is null)
        {
            return lastSuccess ?? new DeviceSwitchResult
            {
                Requested = PrimaryDevice(profile, flow),
                Succeeded = false,
                ErrorMessage = Loc.Get("MissingAdvancedDevices")
            };
        }

        return lastFailure;
    }

    private bool MatchesAdvanced(AudioProfile profile, AudioFlow flow)
    {
        var defaults = _audio.GetDefaultIds(flow);
        foreach (var assignment in GetAdvancedAssignments(profile, flow))
        {
            var current = assignment.Role switch
            {
                AudioRole.Console => defaults.ConsoleId,
                AudioRole.Communications => defaults.CommunicationsId,
                _ => defaults.MultimediaId
            };
            if (!SameId(assignment.Device.Id, current))
            {
                return false;
            }
        }

        return true;
    }

    private static IEnumerable<RoleAssignment> GetAdvancedAssignments(AudioProfile profile, AudioFlow flow)
    {
        yield return new RoleAssignment(flow, AudioRole.Console, RoleDevice(profile, flow, AudioRole.Console));
        yield return new RoleAssignment(flow, AudioRole.Multimedia, RoleDevice(profile, flow, AudioRole.Multimedia));
        yield return new RoleAssignment(flow, AudioRole.Communications, RoleDevice(profile, flow, AudioRole.Communications));
    }

    private static SavedDeviceReference PrimaryDevice(AudioProfile profile, AudioFlow flow) =>
        flow == AudioFlow.Playback ? profile.Output : profile.Input;

    private static SavedDeviceReference RoleDevice(AudioProfile profile, AudioFlow flow, AudioRole role)
    {
        var specific = (flow, role) switch
        {
            (AudioFlow.Playback, AudioRole.Console) => profile.OutputConsole,
            (AudioFlow.Playback, AudioRole.Multimedia) => profile.OutputMultimedia,
            (AudioFlow.Playback, AudioRole.Communications) => profile.OutputCommunications,
            (AudioFlow.Recording, AudioRole.Console) => profile.InputConsole,
            (AudioFlow.Recording, AudioRole.Multimedia) => profile.InputMultimedia,
            (AudioFlow.Recording, AudioRole.Communications) => profile.InputCommunications,
            _ => null
        };

        return HasId(specific) ? specific! : new SavedDeviceReference();
    }

    private static string Describe(AudioFlow flow, DeviceSwitchResult result)
    {
        var key = flow == AudioFlow.Playback ? "OutputLine" : "InputLine";
        return result.Succeeded
            ? Loc.Format(key, result.Requested.Name)
            : Loc.Format(key, Loc.Format("DeviceUnavailable", DisplayName(result.Requested)));
    }

    private static string DisplayName(SavedDeviceReference reference) =>
        string.IsNullOrWhiteSpace(reference.Name) ? reference.Id : reference.Name;

    private static bool HasId(SavedDeviceReference? reference) =>
        !string.IsNullOrWhiteSpace(reference?.Id);

    private static bool SameId(string? left, string? right) =>
        string.Equals(left, right, StringComparison.OrdinalIgnoreCase);
}
