#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère les images de marque à partir du logo vectoriel assets/img/favicon.svg.
Le SVG est la source unique : modifiez-le, puis relancez ce script.
Usage : python3 _sources/build_images.py   (depuis la racine du site)
"""

import io
import os

import cairosvg
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.getcwd(), "assets", "img")
SVG = os.path.join(OUT, "favicon.svg")
GF = "/usr/share/fonts/truetype/google-fonts/"

BG_TOP = (14, 23, 48)
BG_BOTTOM = (7, 11, 22)
BLUE = (47, 125, 255)
BLUE_DEEP = (26, 86, 214)
CYAN = (95, 217, 255)
RED = (226, 80, 74)
WHITE = (255, 255, 255)
MUTED = (148, 164, 198)


def font(name, size):
    return ImageFont.truetype(os.path.join(GF, name), size)


def render_mark(size):
    """Rend le logo vectoriel en image RVBA à la taille demandée."""
    png = cairosvg.svg2png(url=SVG, output_width=size, output_height=size)
    return Image.open(io.BytesIO(png)).convert("RGBA")


def vertical_gradient(size, top, bottom):
    w, h = size
    base = Image.new("RGB", (1, h))
    px = base.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(round(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return base.resize((w, h))


def radial_glow(size, center, radius, color, strength=120):
    layer = Image.new("RGB", size, (0, 0, 0))
    d = ImageDraw.Draw(layer)
    steps = 60
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = strength * (1 - i / steps) ** 2
        c = tuple(round(color[j] * a / 255) for j in range(3))
        d.ellipse([center[0] - r, center[1] - r, center[0] + r, center[1] + r], fill=c)
    return layer


def add(img, layer):
    import numpy as np
    return Image.fromarray(
        np.clip(np.asarray(img, int) + np.asarray(layer, int), 0, 255).astype("uint8"))


def build_og():
    W, H = 1200, 630

    base = vertical_gradient((W, H), BG_TOP, BG_BOTTOM)
    grid = base.copy()
    g = ImageDraw.Draw(grid)
    for x in range(0, W, 48):
        g.line([(x, 0), (x, H)], fill=WHITE, width=1)
    for y in range(0, H, 48):
        g.line([(0, y), (W, y)], fill=WHITE, width=1)
    img = add(Image.blend(base, grid, 0.13), radial_glow((W, H), (260, 30), 640, BLUE, 130))

    d = ImageDraw.Draw(img)

    third = W / 3
    d.rectangle([0, 0, third, 8], fill=BLUE_DEEP)
    d.rectangle([third, 0, third * 2, 8], fill=(244, 247, 255))
    d.rectangle([third * 2, 0, W, 8], fill=RED)

    f_word = font("Poppins-Bold.ttf", 36)
    f_eyebrow = font("Poppins-Medium.ttf", 22)
    f_title = font("Poppins-Bold.ttf", 66)
    f_sub = font("Poppins-Medium.ttf", 30)
    f_chip = font("Poppins-Medium.ttf", 24)

    mark = render_mark(104)
    img.paste(mark, (86, 84), mark)

    d.text((208, 92), "ABONNEMENT", font=f_eyebrow, fill=MUTED)
    d.text((208, 120), "IPTV France", font=f_word, fill=WHITE)

    d.text((86, 250), "Comparez les formules", font=f_title, fill=WHITE)
    d.text((86, 326), "d’abonnement IPTV", font=f_title, fill=CYAN)

    d.text((86, 428), "12 à 24 mois  ·  jusqu’à 5 connexions  ·  appareils compatibles",
           font=f_sub, fill=MUTED)

    chip = "ÉDITION 2026"
    box = d.textbbox((0, 0), chip, font=f_chip)
    cw, ch = box[2] - box[0] + 40, box[3] - box[1] + 26
    d.rounded_rectangle([86, 504, 86 + cw, 504 + ch], radius=ch // 2, outline=(70, 96, 150), width=2)
    d.text((86 + 20 - box[0], 504 + 13 - box[1]), chip, font=f_chip, fill=CYAN)

    site = "abonnement-iptv-france.website"
    d.text((W - 86 - d.textbbox((0, 0), site, font=f_chip)[2], 517), site, font=f_chip, fill=MUTED)

    img.save(os.path.join(OUT, "og-image.png"), optimize=True)
    return "og-image.png"


def build_icons():
    render_mark(512).save(os.path.join(OUT, "logo.png"), optimize=True)

    touch = Image.new("RGB", (180, 180), BG_BOTTOM)
    mark = render_mark(148)
    touch.paste(mark, (16, 16), mark)
    touch.save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
    return ["logo.png", "apple-touch-icon.png"]


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in [build_og()] + build_icons():
        path = os.path.join(OUT, name)
        print("écrit : assets/img/%s (%d octets)" % (name, os.path.getsize(path)))
