from pathlib import Path
p = Path(r'C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Models\AppModels.cs')
text = p.read_text(encoding='utf-8')
needle = '    public string Summary { get; init; } = string.Empty;\n}\n'
insert = needle + '\npublic readonly record struct RoleAssignment(AudioFlow Flow, AudioRole Role, SavedDeviceReference Device);\n'
if needle not in text:
    raise SystemExit('needle not found in AppModels')
if 'record struct RoleAssignment' not in text:
    p.write_text(text.replace(needle, insert), encoding='utf-8')
print('AppModels updated', p.stat().st_size)
