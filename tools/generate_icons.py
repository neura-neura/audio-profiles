from __future__ import annotations

import struct
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
APP_ASSETS = ROOT / "src" / "AudioProfiles" / "Assets"
TMP = ROOT / "tmp"
FONT_PATH = Path(r"C:\Windows\Fonts\SegoeIcons.ttf")
TEAL = (15, 118, 110, 255)
TEAL_SOFT = (20, 132, 124, 255)
WHITE = (255, 255, 255, 255)
GLYPH = "\uE767"


def load_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_PATH), size=size)


def draw_tile(size: int, *, padding_ratio: float = 0.0, simple: bool | None = None) -> Image.Image:
    del simple
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad = max(0.0, size * padding_ratio)
    tile = [pad, pad, size - pad - 1, size - pad - 1]
    radius = max(2, int(round((size - 2 * pad) * 0.225)))
    draw.rounded_rectangle(tile, radius=radius, fill=TEAL)

    font_size = max(8, int(round(size * (0.58 if size >= 32 else 0.62))))
    font = load_font(font_size)
    bbox = draw.textbbox((0, 0), GLYPH, font=font)
    glyph_w = bbox[2] - bbox[0]
    glyph_h = bbox[3] - bbox[1]
    x = (size - glyph_w) / 2 - bbox[0]
    y = (size - glyph_h) / 2 - bbox[1]
    if size >= 48:
        y -= size * 0.01
        x -= size * 0.01
    draw.text((x, y), GLYPH, font=font, fill=WHITE)
    return img


def canvas(width: int, height: int, mark_size: int) -> Image.Image:
    img = Image.new("RGBA", (width, height), TEAL)
    mark = draw_tile(mark_size, padding_ratio=0.08)
    x = (width - mark_size) // 2
    y = (height - mark_size) // 2
    img.alpha_composite(mark, (x, y))
    return img


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
        w = 0 if image.width >= 256 else image.width
        h = 0 if image.height >= 256 else image.height
        entries.append(struct.pack("<BBBBHHII", w, h, 0, 0, 1, 32, len(data), offset))
        payloads.append(data)
        offset += len(data)
    header = struct.pack("<HHH", 0, 1, len(images))
    path.write_bytes(header + b"".join(entries) + b"".join(payloads))


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    logo = draw_tile(1024)
    save_png(logo, ASSETS / "logo.png")
    save_png(draw_tile(512), APP_ASSETS / "Logo.png")
    save_png(draw_tile(50), APP_ASSETS / "StoreLogo.png")
    save_png(draw_tile(48), APP_ASSETS / "LockScreenLogo.scale-200.png")
    save_png(draw_tile(88), APP_ASSETS / "Square44x44Logo.scale-200.png")
    save_png(draw_tile(48, padding_ratio=0.0), APP_ASSETS / "Square44x44Logo.targetsize-24_altform-unplated.png")
    save_png(draw_tile(48, padding_ratio=0.0), APP_ASSETS / "Square44x44Logo.targetsize-48_altform-lightunplated.png")
    save_png(draw_tile(300), APP_ASSETS / "Square150x150Logo.scale-200.png")
    save_png(canvas(620, 300, 220), APP_ASSETS / "Wide310x150Logo.scale-200.png")
    save_png(canvas(1240, 600, 360), APP_ASSETS / "SplashScreen.scale-200.png")
    ico_sizes = [16, 20, 24, 32, 40, 48, 64, 128, 256]
    write_ico([draw_tile(s) for s in ico_sizes], APP_ASSETS / "AppIcon.ico")
    save_png(draw_tile(256), TMP / "appicon-256.png")
    save_png(draw_tile(32), TMP / "appicon-32.png")
    save_png(draw_tile(16), TMP / "appicon-16.png")
    print("icons generated")


if __name__ == "__main__":
    main()
