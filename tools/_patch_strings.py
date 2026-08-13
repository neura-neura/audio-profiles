from pathlib import Path
p = Path(r'C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Helpers\StringCatalog.cs')
text = p.read_text(encoding='utf-8')
en_old = '        ["AdvancedHelp"] = "Most people can leave this off. When it is off, a profile uses the same speakers and microphone for every Windows audio role.",'
en_new = '''        ["AdvancedHelp"] = "Most people can leave this off. When it is off, a profile uses the same speakers and microphone for every Windows audio role.",
        ["AdvancedProfileHelp"] = "Turn this on only if you need different speakers or microphones for everyday use, media, and calls.",
        ["UseAdvancedRoles"] = "Use different devices for Windows audio roles",
        ["AdvancedRolesHint"] = "Windows has three audio roles: Default, Media, and Calls. Most apps follow Default.",
        ["RoleDefault"] = "Default",
        ["RoleMedia"] = "Media",
        ["RoleCalls"] = "Calls",
        ["OutputRole"] = "Output for {0}",
        ["InputRole"] = "Input for {0}",
        ["MissingAdvancedDevices"] = "Choose a speaker and microphone for Default, Media, and Calls.",
        ["SettingsAdvancedHelp"] = "Most people can leave this closed. To use different speakers or microphones for Default, Media, and Calls, open a profile and turn on Advanced there.",'''
es_old = '        ["AdvancedHelp"] = "La mayor\u00eda de las personas puede dejar esto desactivado. As\u00ed, un perfil usa los mismos altavoces y micr\u00f3fono para todos los roles de audio de Windows.",'
es_new = '''        ["AdvancedHelp"] = "La mayor\u00eda de las personas puede dejar esto desactivado. As\u00ed, un perfil usa los mismos altavoces y micr\u00f3fono para todos los roles de audio de Windows.",
        ["AdvancedProfileHelp"] = "Act\u00edvalo solo si necesitas distintos altavoces o micr\u00f3fonos para el uso diario, el contenido multimedia y las llamadas.",
        ["UseAdvancedRoles"] = "Usar dispositivos distintos para los roles de audio de Windows",
        ["AdvancedRolesHint"] = "Windows tiene tres roles de audio: Predeterminado, Multimedia y Llamadas. La mayor\u00eda de las aplicaciones siguen Predeterminado.",
        ["RoleDefault"] = "Predeterminado",
        ["RoleMedia"] = "Multimedia",
        ["RoleCalls"] = "Llamadas",
        ["OutputRole"] = "Salida para {0}",
        ["InputRole"] = "Entrada para {0}",
        ["MissingAdvancedDevices"] = "Elige un altavoz y un micr\u00f3fono para Predeterminado, Multimedia y Llamadas.",
        ["SettingsAdvancedHelp"] = "La mayor\u00eda de las personas puede dejar esto cerrado. Para usar distintos altavoces o micr\u00f3fonos en Predeterminado, Multimedia y Llamadas, abre un perfil y activa Avanzado all\u00ed.",'''
if en_old not in text:
    raise SystemExit('english advanced help not found')
if es_old not in text:
    raise SystemExit('spanish advanced help not found')
text = text.replace(en_old, en_new, 1).replace(es_old, es_new, 1)
p.write_text(text, encoding='utf-8')
print('StringCatalog updated')
