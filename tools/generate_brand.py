"""Builds DuckBoard's launcher icons from branding/duckboard-icon.png.

The source is a rounded-square illustration on a white field. The white outside the
rounded shape is flood-filled to transparency, then rendered with enough margin that
launchers do not crop into the duck: adaptive foregrounds sit at 74% of the canvas,
legacy icons at 88%, round icons at 80%.
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "app", "src", "main", "res")
SRC = os.path.join(ROOT, "branding", "duckboard-icon.png")

TOP = (255, 255, 255)
BOTTOM = (255, 255, 255)
ADAPTIVE_SCALE = 0.52
LEGACY_SCALE = 0.72
ROUND_SCALE = 0.64

BACKGROUND_XML = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:pathData="M0,0h108v108h-108z"
        android:fillColor="#FFFFFF" />
</vector>
"""


def cut_mark() -> Image.Image:
    image = Image.open(SRC).convert("RGB")
    work = image.copy()
    magenta = (255, 0, 255)
    for point in ((0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1)):
        ImageDraw.floodfill(work, point, magenta, thresh=30)
    arr = np.asarray(work)
    outside = (arr[:, :, 0] > 250) & (arr[:, :, 1] < 5) & (arr[:, :, 2] > 250)
    rgba = Image.open(SRC).convert("RGBA")
    alpha = np.where(outside, 0, 255).astype(np.uint8)
    rgba.putalpha(Image.fromarray(alpha))
    bbox = rgba.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    return rgba


def gradient(size: int, circle: bool = False) -> Image.Image:
    img = Image.new("RGBA", (size, size))
    px = img.load()
    for y in range(size):
        t = y / max(1, size - 1)
        color = (
            round(TOP[0] * (1 - t) + BOTTOM[0] * t),
            round(TOP[1] * (1 - t) + BOTTOM[1] * t),
            round(TOP[2] * (1 - t) + BOTTOM[2] * t),
            255,
        )
        for x in range(size):
            px[x, y] = color
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    if circle:
        md.ellipse((0, 0, size - 1, size - 1), fill=255)
    else:
        md.rounded_rectangle((0, 0, size - 1, size - 1), radius=round(size * 0.22), fill=255)
    img.putalpha(mask)
    return img


def compose(mark: Image.Image, size: int, scale: float, circle: bool = False) -> Image.Image:
    base = gradient(size, circle)
    art_size = max(1, round(size * scale))
    art = mark.resize((art_size, art_size), Image.LANCZOS)
    offset = ((size - art_size) // 2, (size - art_size) // 2)
    base.alpha_composite(art, offset)
    return base


def adaptive_foreground(mark: Image.Image, size: int) -> Image.Image:
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    art_size = max(1, round(size * ADAPTIVE_SCALE))
    art = mark.resize((art_size, art_size), Image.LANCZOS)
    out.alpha_composite(art, ((size - art_size) // 2, (size - art_size) // 2))
    return out


def main() -> None:
    mark = cut_mark()

    for folder, size in {
        "mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192,
    }.items():
        target = os.path.join(RES, f"mipmap-{folder}")
        os.makedirs(target, exist_ok=True)
        compose(mark, size, LEGACY_SCALE).save(os.path.join(target, "ic_launcher.png"))
        compose(mark, size, ROUND_SCALE, circle=True).save(os.path.join(target, "ic_launcher_round.png"))

    for folder, size in {
        "mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432,
    }.items():
        target = os.path.join(RES, f"drawable-{folder}")
        os.makedirs(target, exist_ok=True)
        adaptive_foreground(mark, size).save(os.path.join(target, "ic_launcher_foreground.png"))
        mono = os.path.join(target, "ic_launcher_monochrome.png")
        if os.path.exists(mono):
            os.remove(mono)

    bg_dir = os.path.join(RES, "drawable-v24")
    os.makedirs(bg_dir, exist_ok=True)
    with open(os.path.join(bg_dir, "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
        f.write(BACKGROUND_XML)

    mark.resize((512, 512), Image.LANCZOS).save(os.path.join(ROOT, "branding", "duckboard-mark.png"))

    preview = Image.new("RGBA", (900, 320), (245, 245, 245, 255))
    preview.alpha_composite(compose(mark, 260, LEGACY_SCALE), (20, 30))
    preview.alpha_composite(compose(mark, 260, ROUND_SCALE, circle=True), (320, 30))

    # What the launcher actually shows: the central 72/108 of an adaptive icon.
    adaptive = gradient(432)
    adaptive.alpha_composite(adaptive_foreground(mark, 432), (0, 0))
    visible = adaptive.crop((72, 72, 360, 360))
    mask = Image.new("L", (288, 288), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 287, 287), radius=82, fill=255)
    adaptive_icon = Image.new("RGBA", (288, 288), (0, 0, 0, 0))
    adaptive_icon.paste(visible, (0, 0), mask)
    preview.alpha_composite(adaptive_icon.resize((260, 260), Image.LANCZOS), (620, 30))
    preview.save(os.path.join(ROOT, "branding", "icon-preview.png"))
    print("wrote padded adaptive + legacy icons from", os.path.basename(SRC))


if __name__ == "__main__":
    main()
