from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Helpers\StringCatalog.cs")
text = p.read_text(encoding="utf-8")
old1 = '["ShowNotifications"] = "Show notifications when switching profiles",'
new1 = old1 + '\n        ["LaunchMinimized"] = "Start minimized in the tray",'
old2 = '["ShowNotifications"] = "Mostrar notificaciones al cambiar de perfil",'
new2 = old2 + '\n        ["LaunchMinimized"] = "Iniciar minimizado en la bandeja",'
if old1 not in text or old2 not in text:
    raise SystemExit("markers not found")
p.write_text(text.replace(old1, new1).replace(old2, new2), encoding="utf-8", newline="\n")
print("updated", p.read_text(encoding="utf-8").count("LaunchMinimized"))
