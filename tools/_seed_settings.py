from pathlib import Path
p = Path.home() / "AppData" / "Local" / "AudioProfiles" / "settings.json"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(r'''{
  "Version": 1,
  "Profiles": [
    {
      "Id": "desktop",
      "Name": "Desktop",
      "Icon": "Desktop",
      "Output": { "Id": "{0.0.0.00000000}.{0499eba4-83f4-4a4f-a428-e15a553be2f1}", "Name": "Speaker Ugreen Soundcard (KT USB Audio)" },
      "Input": { "Id": "{0.0.1.00000000}.{a6de350f-fd95-40f4-806d-f5895693fb34}", "Name": "Micro Ugreen Soundcard (KT USB Audio)" },
      "Hotkey": { "Enabled": true, "Control": true, "Alt": true, "Shift": false, "Windows": false, "VirtualKey": 49 }
    },
    {
      "Id": "sofa",
      "Name": "Sofa",
      "Icon": "Sofa",
      "Output": { "Id": "{0.0.0.00000000}.{3d82d90d-b2fa-4b6c-8d84-ebf52895fec6}", "Name": "Roku TV (NVIDIA High Definition Audio)" },
      "Input": { "Id": "{0.0.1.00000000}.{404f0782-6ea6-4105-a91d-cfb1dfa80c31}", "Name": "Micro Webcam (EMEET SmartCam C950)" },
      "Hotkey": { "Enabled": true, "Control": true, "Alt": true, "Shift": false, "Windows": false, "VirtualKey": 50 }
    },
    {
      "Id": "vr",
      "Name": "VR",
      "Icon": "Vr",
      "Output": { "Id": "{0.0.0.00000000}.{2050e021-7563-4eb2-8814-75d5731006cb}", "Name": "Audifonos (este es) (Realtek USB Audio)" },
      "Input": { "Id": "{0.0.1.00000000}.{f1d81a87-a039-4af0-a45e-1524778c2851}", "Name": "Micro Audifonos (este es) (Realtek USB Audio)" },
      "Hotkey": { "Enabled": true, "Control": true, "Alt": true, "Shift": false, "Windows": false, "VirtualKey": 51 }
    }
  ],
  "Settings": {
    "Theme": "System",
    "StartWithWindows": false,
    "KeepRunningInBackground": true,
    "ShowNotifications": true,
    "LaunchMinimized": false,
    "LastActivatedProfileId": "desktop",
    "WindowWidth": 1040,
    "WindowHeight": 760
  }
}
''', encoding="utf-8", newline="\n")
print("seeded", p, p.stat().st_size)
