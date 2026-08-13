from pathlib import Path
p = Path(r"C:\Users\neura\repos\audio-device-switcher\README.md")
t = p.read_text(encoding="utf-8")
t = t.replace(
    "- **Advanced:** optional detailed logs, plus a shortcut to open a profile and set different devices for Default, Media, and Calls",
    "- **Advanced:** optional detailed logs, and per-role speaker/microphone assignment for a selected profile"
)
p.write_text(t, encoding="utf-8")
print("readme ok")
