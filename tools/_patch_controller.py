from pathlib import Path
p = Path(r'C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Services\AppController.cs')
text = p.read_text(encoding='utf-8')
old = '''    public string DetectActiveProfileId()
    {
        var defaults = Audio.GetCurrentDefaults();
        var match = State.Profiles.FirstOrDefault(profile =>
            string.Equals(profile.Output.Id, defaults.OutputId, StringComparison.OrdinalIgnoreCase) &&
            string.Equals(profile.Input.Id, defaults.InputId, StringComparison.OrdinalIgnoreCase));
        return match?.Id ?? string.Empty;
    }
'''
new = '''    public string DetectActiveProfileId()
    {
        var match = State.Profiles.FirstOrDefault(_activation.MatchesCurrentDefaults);
        return match?.Id ?? string.Empty;
    }
'''
if old not in text:
    raise SystemExit('DetectActiveProfileId not found')
p.write_text(text.replace(old, new, 1), encoding='utf-8')
print('AppController updated')
