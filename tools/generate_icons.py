from __future__ import annotations

import struct
from io import BytesIO
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
APP_ASSETS = ROOT / "src" / "AudioProfiles" / "Assets"
TMP = ROOT / "tmp"
MASTER = ASSETS / "logo-transparent.png"
PREVIEW = ASSETS / "logo.png"
PREVIEW_BACKGROUND = (244, 245, 247, 255)


def load_master() -> Image.Image:
    if not MASTER.exists():
        raise FileNotFoundError(f"Approved icon master not found: {MASTER}")

    return Image.open(MASTER).convert("RGBA")


def resize_master(master: Image.Image, size: int) -> Image.Image:
    return master.resize((size, size), Image.Resampling.LANCZOS)


def preview(master: Image.Image) -> Image.Image:
    image = Image.new("RGBA", master.size, PREVIEW_BACKGROUND)
    image.alpha_composite(master)
    return image


def canvas(master: Image.Image, width: int, height: int, icon_size: int) -> Image.Image:
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    icon = resize_master(master, icon_size)
    image.alpha_composite(icon, ((width - icon_size) // 2, (height - icon_size) // 2))
    return image


def save_png(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG")


def write_ico(images: list[Image.Image], path: Path) -> None:
    entries = []
    payloads = []
    offset = 6 + 16 * len(images)
    for image in images:
        output = BytesIO()
        image.save(output, format="PNG")
        data = output.getvalue()
        width = 0 if image.width >= 256 else image.width
        height = 0 if image.height >= 256 else image.height
        entries.append(struct.pack("<BBBBHHII", width, height, 0, 0, 1, 32, len(data), offset))
        payloads.append(data)
        offset += len(data)

    header = struct.pack("<HHH", 0, 1, len(images))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(header + b"".join(entries) + b"".join(payloads))


def main() -> None:
    master = load_master()
    save_png(preview(master), PREVIEW)

    save_png(resize_master(master, 512), APP_ASSETS / "Logo.png")
    save_png(resize_master(master, 50), APP_ASSETS / "StoreLogo.png")
    save_png(resize_master(master, 48), APP_ASSETS / "LockScreenLogo.scale-200.png")
    save_png(resize_master(master, 88), APP_ASSETS / "Square44x44Logo.scale-200.png")
    save_png(resize_master(master, 48), APP_ASSETS / "Square44x44Logo.targetsize-24_altform-unplated.png")
    save_png(resize_master(master, 48), APP_ASSETS / "Square44x44Logo.targetsize-48_altform-lightunplated.png")
    save_png(resize_master(master, 300), APP_ASSETS / "Square150x150Logo.scale-200.png")
    save_png(canvas(master, 620, 300, 220), APP_ASSETS / "Wide310x150Logo.scale-200.png")
    save_png(canvas(master, 1240, 600, 360), APP_ASSETS / "SplashScreen.scale-200.png")

    ico_sizes = [16, 20, 24, 32, 40, 48, 64, 128, 256]
    write_ico([resize_master(master, size) for size in ico_sizes], APP_ASSETS / "AppIcon.ico")

    TMP.mkdir(parents=True, exist_ok=True)
    save_png(resize_master(master, 256), TMP / "appicon-256.png")
    save_png(resize_master(master, 32), TMP / "appicon-32.png")
    save_png(resize_master(master, 16), TMP / "appicon-16.png")
    print("icons generated from the approved 1024x1024 master")


if __name__ == "__main__":
    main()
