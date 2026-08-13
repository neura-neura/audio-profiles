from pathlib import Path

path = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Helpers\StringCatalog.cs")
text = path.read_text(encoding="utf-8")

en_old = '''        ["SettingsAdvancedHelp"] = "Most people can leave this closed. To use different speakers or microphones for Default, Media, and Calls, open a profile and turn on Advanced there.",
        ["About"] = "About",'''
en_new = '''        ["SettingsAdvancedHelp"] = "Most people can leave these options off. They are only needed for extra logging or if one profile must use different speakers or microphones for Default, Media, and Calls.",
        ["WriteDetailedLogs"] = "Write detailed diagnostic logs",
        ["SettingsAdvancedRolesHint"] = "Choose a profile, then turn on different devices for Default, Media, and Calls. Save the profile when you are done.",
        ["OpenProfileAdvanced"] = "Open selected profile",
        ["ChooseProfileForAdvanced"] = "Choose a profile",
        ["About"] = "About",'''

es_old = '''        ["SettingsAdvancedHelp"] = "La mayoría de las personas puede dejar esto cerrado. Para usar distintos altavoces o micrófonos en Predeterminado, Multimedia y Llamadas, abre un perfil y activa Avanzado allí.",
        ["About"] = "Acerca de",'''
es_new = '''        ["SettingsAdvancedHelp"] = "La mayoría de las personas puede dejar estas opciones desactivadas. Solo hacen falta para registros extra o si un perfil debe usar distintos altavoces o micrófonos para Predeterminado, Multimedia y Llamadas.",
        ["WriteDetailedLogs"] = "Escribir registros de diagnóstico detallados",
        ["SettingsAdvancedRolesHint"] = "Elige un perfil y activa dispositivos distintos para Predeterminado, Multimedia y Llamadas. Guarda el perfil cuando termines.",
        ["OpenProfileAdvanced"] = "Abrir perfil seleccionado",
        ["ChooseProfileForAdvanced"] = "Elige un perfil",
        ["About"] = "Acerca de",'''

if en_old not in text or es_old not in text:
    raise SystemExit("StringCatalog markers not found")
path.write_text(text.replace(en_old, en_new, 1).replace(es_old, es_new, 1), encoding="utf-8")
print("updated StringCatalog")
