from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\README.md")
t = p.read_text(encoding="utf-8")
t = t.replace(
    "- **Advanced:** explains Windows audio roles. Per-role devices are configured on each profile",
    "- **Advanced:** optional detailed logs, plus a shortcut to open a profile and set different devices for Default, Media, and Calls"
)
t = t.replace(
    "| Notifications | Windows App SDK toasts, with a native toast fallback |",
    "| Notifications | Unpackaged Windows App SDK toasts |"
)
p.write_text(t, encoding="utf-8")
print("updated README")
