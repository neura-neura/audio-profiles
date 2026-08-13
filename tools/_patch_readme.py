from pathlib import Path
p = Path(r'C:\\Users\\neura\\repos\\audio-device-switcher\\README.md')
text = p.read_text(encoding='utf-8')
old_edit = '**Edit a profile.** Use **Edit** or **Change** on the card. You can rename it, replace a missing device, or assign a shortcut.'
new_edit = '**Edit a profile.** Use **Edit** or **Change** on the card. You can rename it, replace a missing device, or assign a shortcut. Open **Advanced** on that page only if you need different devices for Default, Media, and Calls.'
old_settings = '''- **Theme:** System, Light, or Dark
- **Start Audio Profiles with Windows:** off by default; when on, the app can start quietly in the tray
- **Keep running in background when window is closed:** on by default
- **Show notifications when switching profiles:** on by default
- **Start minimized in the tray:** optional'''
new_settings = '''- **Theme:** System, Light, or Dark
- **Start Audio Profiles with Windows:** off by default; when on, the app can start quietly in the tray
- **Keep running in background when window is closed:** on by default
- **Show notifications when switching profiles:** on by default
- **Start minimized in the tray:** optional
- **Advanced:** explains Windows audio roles. Per-role devices are configured on each profile'''
old_arch = '| Notifications | Native Windows toasts using the app AUMID |'
new_arch = '| Notifications | Windows App SDK toasts, with a native toast fallback |'
old_tech = 'By default a profile applies the same speaker and microphone to Console, Multimedia, and Communications.'
new_tech = 'By default a profile applies the same speaker and microphone to Console, Multimedia, and Communications. Optional per-role devices live in each profile\'s Advanced section.'
for name, old in [('edit', old_edit), ('settings', old_settings), ('arch', old_arch), ('tech', old_tech)]:
    if old not in text:
        raise SystemExit(f'missing {name}')
text = text.replace(old_edit, new_edit).replace(old_settings, new_settings).replace(old_arch, new_arch).replace(old_tech, new_tech)
p.write_text(text, encoding='utf-8')
print('README updated')
