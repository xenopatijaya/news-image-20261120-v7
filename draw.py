#!/usr/bin/env python3
"""Draw entry.png (1024x1024): a newspaper front page for Friday 20 November 2026.

Deterministic: fixed-seed grain only, no network, no clock.
Build-time only; main.py ships the committed entry.png.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
M = 24                      # page margin
CW = W - 2 * M              # content width = 976
RIGHT = W - M

PAPER = (247, 241, 227)
INK = (21, 34, 46)
RED = (200, 16, 46)
NAVY = (22, 50, 74)
TEAL = (14, 125, 116)
GOLD = (201, 134, 43)
GREEN = (46, 125, 70)
PURPLE = (91, 74, 158)
GRAY = (110, 108, 100)
CREAM = (250, 246, 235)
DARKCHIP = (12, 16, 22)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-{}.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans{}.ttf"


def serif(size, style="Bold"):
    return ImageFont.truetype(SERIF.format(style), size)


def sans(size, bold=False):
    return ImageFont.truetype(SANS.format("-Bold" if bold else ""), size)


def fit_font(draw, text, path_fmt, size, max_w, bold_sans=False):
    """Largest font at or below `size` that fits max_w."""
    s = size
    while s > 6:
        f = sans(s, True) if bold_sans else ImageFont.truetype(path_fmt, s)
        if draw.textlength(text, font=f) <= max_w:
            return f
        s -= 1
    return sans(s, True) if bold_sans else ImageFont.truetype(path_fmt, s)


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, font, fill, max_w, lh, max_lines=None, align="left"):
    x, y = xy
    lines = wrap(draw, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        xx = x
        if align == "center":
            xx = x + (max_w - draw.textlength(ln, font=font)) / 2
        elif align == "right":
            xx = x + max_w - draw.textlength(ln, font=font)
        draw.text((xx, y), ln, font=font, fill=fill)
        y += lh
    return y


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- scenes
def scene_kyiv(w, h):
    img = Image.new("RGB", (w, h), (10, 20, 42))
    d = ImageDraw.Draw(img)
    for i in range(h):  # night gradient bands
        t = i / max(1, h)
        d.line([(0, i), (w, i)], fill=(int(8 + 22 * t), int(18 + 36 * t), int(38 + 48 * t)))
    rng = random.Random(11)
    for _ in range(42):  # stars
        x, y = rng.uniform(2, w - 2), rng.uniform(2, h * 0.52)
        r = rng.choice([1, 1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(235, 238, 220))
    # skyline silhouettes
    rng2 = random.Random(7)
    base = h - 30
    x = 0
    while x < w:
        bw = rng2.randint(16, 34)
        bh = rng2.randint(18, 52)
        d.rectangle([x, base - bh, x + bw, base], fill=(5, 10, 20))
        for wy in range(base - bh + 5, base - 6, 9):
            for wx in range(x + 3, x + bw - 3, 8):
                if rng2.random() < 0.4:
                    d.point((wx, wy), fill=(240, 200, 90))
        x += bw + rng2.randint(1, 5)
    # river band
    d.rectangle([0, base, w, h], fill=(18, 62, 102))
    for i in range(9):
        yy = base + 4 + i * 3
        d.line([(rng2.randint(0, 60), yy), (rng2.randint(w - 90, w), yy)], fill=(70, 130, 170))
    # two arched bridges over the river
    for bx0, bx1, deck_y in [(8, w * 0.52, base + 8), (w * 0.46, w - 8, base + 16)]:
        d.line([(bx0, deck_y), (bx1, deck_y)], fill=(190, 200, 210), width=3)
        d.arc([bx0, deck_y - 26, bx1, deck_y + 22], 180, 360, fill=(190, 200, 210), width=3)
        for px in range(int(bx0) + 8, int(bx1) - 4, 26):
            d.line([(px, deck_y), (px, h - 2)], fill=(120, 140, 160), width=2)
    # five dotted missile arcs (gold)
    targets = [(w * 0.22, base + 6), (w * 0.68, base + 14)]
    starts = [(w * 0.06, 2), (w * 0.30, 0), (w * 0.52, 4), (w * 0.78, 0), (w * 0.94, 6)]
    for i, (sx, sy) in enumerate(starts):
        tx, ty = targets[i % 2]
        cx, cy = (sx + tx) / 2, min(sy, ty) - 34 - (i % 3) * 10
        for k in range(0, 41, 3):
            t = k / 40
            px = (1 - t) ** 2 * sx + 2 * (1 - t) * t * cx + t ** 2 * tx
            py = (1 - t) ** 2 * sy + 2 * (1 - t) * t * cy + t ** 2 * ty
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(245, 190, 60))
    # two impact glows at bridge level
    for gx, gy in targets:
        d.ellipse([gx - 26, gy - 13, gx + 26, gy + 10], fill=(240, 120, 30))
        d.ellipse([gx - 15, gy - 9, gx + 15, gy + 7], fill=(250, 180, 60))
        d.polygon([(gx - 9, gy - 4), (gx + 9, gy - 4), (gx, gy - 26)], fill=RED)
    return img


def scene_cyclone(w, h):
    img = Image.new("RGB", (w, h), TEAL)
    d = ImageDraw.Draw(img)
    for i in range(h):
        t = i / max(1, h)
        d.line([(0, i), (w, i)], fill=(int(12 + 16 * t), int(118 - 30 * t), int(112 - 26 * t)))
    # tan coastline polygon on the left, irregular shore
    coast = [(0, 0), (86, 0), (74, 22), (96, 44), (70, 66), (88, 88),
             (64, 108), (78, 128), (58, h), (0, h)]
    d.polygon(coast, fill=(216, 186, 130))
    d.line(coast[1:] + [coast[1]], fill=(170, 140, 90), width=2)
    for gx, gy in [(20, 30), (34, 74), (16, 116), (44, 52)]:
        d.ellipse([gx - 5, gy - 3, gx + 5, gy + 3], fill=(120, 160, 90))
    # big white cyclone spiral
    cx, cy = w * 0.64, h * 0.48
    pts = []
    for k in range(0, 200):
        t = k / 199
        ang = t * math.pi * 7
        r = 54 - 46 * t
        pts.append((cx + r * math.cos(ang), cy + r * 0.82 * math.sin(ang)))
    d.line(pts, fill=(255, 255, 255), width=5, joint="curve")
    pts2 = [(cx + (r + 13) * math.cos(a), cy + (r + 13) * 0.82 * math.sin(a))
            for a, r in [(t * math.pi * 5 + 2.2, 40 - 26 * t) for t in [i / 60 for i in range(61)]]]
    d.line(pts2, fill=(230, 245, 245), width=3, joint="curve")
    d.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(255, 248, 220))
    # wind arcs near the coast
    for ax, ay, r in [(120, 34, 20), (108, 74, 26), (126, 112, 18)]:
        d.arc([ax - r, ay - r * 0.6, ax + r, ay + r * 0.6], 200, 40, fill=(255, 255, 255), width=3)
    # rain streaks
    rng = random.Random(23)
    for _ in range(16):
        x, y = rng.uniform(w * 0.35, w - 8), rng.uniform(6, h - 22)
        d.line([(x, y), (x - 5, y + 11)], fill=(190, 230, 235), width=2)
    # landfall point + label
    lx, ly = 82, 88
    d.ellipse([lx - 6, ly - 6, lx + 6, ly + 6], fill=RED)
    d.ellipse([lx - 2, ly - 2, lx + 2, ly + 2], fill=(255, 255, 255))
    d.text((lx + 10, ly - 6), "GOPALPUR", font=sans(9, True), fill=(255, 255, 255))
    return img


def scene_selloff(w, h):
    img = Image.new("RGB", (w, h), (8, 10, 14))
    d = ImageDraw.Draw(img, "RGBA")
    for gx in range(12, w, 18):  # faint dot grid
        for gy in range(10, h, 16):
            d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(70, 80, 95, 110))
    pts = [(8, 26), (58, 40), (108, 52), (158, 78), (208, 92), (258, 116), (308, 132)]
    d.polygon(pts + [(308, h - 4), (8, h - 4)], fill=(160, 20, 40, 70))
    d.line(pts, fill=(120, 10, 30), width=9, joint="curve")
    d.line(pts, fill=(255, 45, 70), width=5, joint="curve")
    for px, py in pts:
        d.rectangle([px - 4, py - 4, px + 4, py + 4], fill=(255, 90, 110))
    # semi-transparent data panel, right side
    pw = 118
    px0 = w - pw - 6
    d.rectangle([px0, 22, w - 6, h - 8], fill=(0, 0, 0, 178))
    rows = [("TAIPEI", "\u22126.2%"), ("SEOUL", "\u22125.2%"),
            ("TOKYO", "\u22125.1%"), ("HONG KONG", "\u22121.9%")]
    ry = 29
    for city, pct in rows:
        d.text((px0 + 8, ry), city, font=sans(10, True), fill=(250, 246, 235))
        d.text((px0 + 8, ry + 12), pct, font=sans(13, True), fill=(255, 110, 130))
        ry += 28
    return img


# ---------------------------------------------------------------- cards
def card_uk_eu(w, h):
    img = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(img)
    uw = int(w * 0.55)
    d.line([(0, 0), (uw, h)], fill=(255, 255, 255), width=9)
    d.line([(0, h), (uw, 0)], fill=(255, 255, 255), width=9)
    d.line([(0, 0), (uw, h)], fill=RED, width=3)
    d.line([(0, h), (uw, 0)], fill=RED, width=3)
    d.rectangle([uw // 2 - 9, 0, uw // 2 + 9, h], fill=(255, 255, 255))
    d.rectangle([0, h // 2 - 9, uw, h // 2 + 9], fill=(255, 255, 255))
    d.rectangle([uw // 2 - 5, 0, uw // 2 + 5, h], fill=RED)
    d.rectangle([0, h // 2 - 5, uw, h // 2 + 5], fill=RED)
    cx, cy = uw + (w - uw) // 2, h // 2
    for i in range(12):
        a = i * math.pi / 6
        star(d, cx + 27 * math.cos(a), cy + 27 * math.sin(a), 5, GOLD)
    return img


def card_poland(w, h):
    img = Image.new("RGB", (w, h), (208, 224, 236))
    d = ImageDraw.Draw(img)
    d.rectangle([0, h - 20, w, h], fill=GREEN)
    d.line([(26, 62), (118, 24)], fill=(150, 155, 160), width=17)   # missile body
    d.polygon([(112, 16), (134, 22), (116, 32)], fill=RED)          # tip
    for k in range(4):                                              # smoke dashes
        x, y = 16 - k * 2, 70 + k * 2
        d.line([(x, y), (x + 12, y - 5)], fill=(255, 255, 255), width=3)
    d.rectangle([w - 42, 26, w - 30, 62], fill=(120, 125, 130))     # tower
    d.rectangle([w - 47, 18, w - 25, 28], fill=(90, 100, 115))
    d.rectangle([w - 78, 52, w - 18, 64], fill=(105, 112, 120))     # terminal
    return img


def card_cop31(w, h):
    img = Image.new("RGB", (w, h), TEAL)
    d = ImageDraw.Draw(img)
    d.ellipse([10, 14, 74, 78], fill=(40, 110, 180))
    d.polygon([(24, 34), (40, 26), (48, 38), (34, 46), (22, 44)], fill=(70, 170, 100))
    d.polygon([(44, 56), (60, 52), (64, 64), (50, 70)], fill=(70, 170, 100))
    cx, cy, r = w - 52, h // 2 - 4, 31
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=CREAM, outline=INK, width=2)
    for i in range(12):
        a = i * math.pi / 6
        d.line([(cx + (r - 6) * math.cos(a), cy + (r - 6) * math.sin(a)),
                (cx + (r - 2) * math.cos(a), cy + (r - 2) * math.sin(a))], fill=INK, width=2)
    d.line([(cx, cy), (cx - 12, cy - 10)], fill=INK, width=4)
    d.line([(cx, cy), (cx + 6, cy - 19)], fill=INK, width=4)
    d.line([(cx, cy), (cx + 16, cy + 12)], fill=RED, width=2)
    d.rectangle([cx - 20, cy + r + 3, cx + 20, cy + r + 11], fill=RED)
    return img


def card_italy(w, h):
    img = Image.new("RGB", (w, h), (243, 236, 218))
    d = ImageDraw.Draw(img)
    for i, mx in enumerate(range(8, w - 10, 26)):  # marchers
        hy = h - 34 - (6 if i % 2 else 0)
        d.ellipse([mx, hy, mx + 13, hy + 13], fill=INK)
        d.pieslice([mx - 4, hy + 10, mx + 17, hy + 34], 180, 360, fill=INK)
    d.rectangle([139, 40, 142, 58], fill=(90, 70, 50))  # placard stick
    d.rectangle([102, 22, 178, 40], fill=RED)
    f = sans(10, True)
    tw = d.textlength("SCIOPERO", font=f)
    d.text((140 - tw / 2, 25), "SCIOPERO", font=f, fill=(255, 255, 255))
    return img


def card_japan(w, h):
    img = Image.new("RGB", (w, h), (244, 240, 228))
    d = ImageDraw.Draw(img)
    d.ellipse([12, 16, 62, 66], fill=RED)
    for i, bh in enumerate([22, 34, 47]):
        x = 84 + i * 26
        d.rectangle([x, h - 12 - bh, x + 18, h - 12], fill=NAVY)
    d.line([(80, 52), (112, 40), (140, 30), (172, 14)], fill=RED, width=4, joint="curve")
    d.polygon([(172, 14), (158, 15), (166, 26)], fill=RED)
    return img


def card_seoul(w, h):
    img = Image.new("RGB", (w, h), (148, 163, 178))
    d = ImageDraw.Draw(img)
    bx, bw = 14, 108
    d.polygon([(bx - 4, 26), (bx + bw + 4, 26), (bx + bw // 2, 8)], fill=CREAM)
    d.rectangle([bx - 2, 27, bx + bw + 2, 34], fill=CREAM)
    for i in range(5):
        x = bx + 6 + i * 21
        d.rectangle([x, 36, x + 11, 66], fill=CREAM)
    d.rectangle([bx - 4, 67, bx + bw + 4, 72], fill=CREAM)
    d.rectangle([bx - 8, 73, bx + bw + 8, 78], fill=(230, 226, 214))
    d.line([(w - 44, 30), (w - 16, 56)], fill=GOLD, width=7)        # gavel
    d.rectangle([w - 52, 22, w - 34, 34], fill=GOLD)
    d.rectangle([w - 48, 62, w - 14, 69], fill=GOLD)                # sound block
    return img


def card_hormuz(w, h):
    img = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 0), (w, 0), (w, 26), (96, 34), (40, 22), (0, 30)], fill=(150, 116, 78))
    d.polygon([(0, h), (w, h), (w, 54), (110, 50), (52, 62), (0, 56)], fill=(150, 116, 78))
    cx, cy = w // 2, h // 2 + 2  # tanker
    d.polygon([(cx - 42, cy + 6), (cx + 42, cy + 6), (cx + 32, cy + 17), (cx - 32, cy + 17)], fill=(8, 10, 14))
    d.rectangle([cx - 38, cy + 1, cx + 30, cy + 6], fill=(8, 10, 14))
    d.rectangle([cx + 14, cy - 10, cx + 28, cy + 1], fill=(8, 10, 14))
    d.rectangle([cx + 22, cy - 16, cx + 27, cy - 10], fill=(8, 10, 14))
    d.rectangle([w - 26, 4, w - 6, 24], fill=RED)
    d.line([(w - 23, 7), (w - 9, 21)], fill=(255, 255, 255), width=3)
    d.line([(w - 9, 7), (w - 23, 21)], fill=(255, 255, 255), width=3)
    return img


def card_bukele(w, h):
    img = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(img)
    for i in range(5):
        a = math.pi * (0.15 + 0.175 * i)
        star(d, w // 2 + 62 * math.cos(a + math.pi), 52 - 34 * math.sin(a), 6, GOLD)
    d.polygon([(w // 2 - 13, 18), (w // 2 + 13, 18), (w // 2 + 9, 44), (w // 2 - 9, 44)], fill=(255, 255, 255))
    d.line([(w // 2 - 7, 34), (w // 2 - 1, 40)], fill=RED, width=3)
    d.line([(w // 2 - 1, 40), (w // 2 + 8, 27)], fill=RED, width=3)
    d.rectangle([w // 2 - 34, 44, w // 2 + 34, 76], fill=(86, 130, 180))
    d.rectangle([w // 2 - 16, 48, w // 2 + 16, 53], fill=(10, 20, 34))
    return img


def card_phillips(w, h):
    img = Image.new("RGB", (w, h), GREEN)
    d = ImageDraw.Draw(img)
    f = fit_font(d, "118", SERIF.format("Bold"), 52, 92)
    d.text((6, 14), "118", font=f, fill=CREAM)
    d.line([(108, 66), (140, 22)], fill=(150, 105, 60), width=11)   # bat
    d.line([(140, 22), (150, 10)], fill=(150, 105, 60), width=6)
    d.ellipse([96, 12, 110, 26], fill=RED)                          # ball
    for i in range(3):                                              # stumps
        x = w - 30 + i * 9
        d.rectangle([x, 34, x + 5, 72], fill=CREAM)
    d.line([(w - 31, 32), (w - 4, 32)], fill=GOLD, width=3)
    return img


def card_dakar(w, h):
    img = Image.new("RGB", (w, h), TEAL)
    d = ImageDraw.Draw(img)
    for i in range(4):
        for j in range(2):
            ax, ay = 14 + i * 46, 14 + j * 52
            d.arc([ax, ay, ax + 30, ay + 14], 180, 360, fill=(255, 255, 255), width=2)
    d.polygon([(34, 52), (118, 34), (124, 44), (44, 64)], fill=(130, 92, 55))  # capsized hull
    d.line([(40, 56), (120, 38)], fill=(90, 62, 36), width=3)
    for hx, hy in [(58, 70), (96, 66)]:                             # swimmer heads
        d.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=(60, 42, 30))
        d.arc([hx - 12, hy + 2, hx + 12, hy + 14], 0, 180, fill=(255, 255, 255), width=2)
    d.ellipse([w - 44, 44, w - 12, 76], outline=(245, 130, 30), width=6)      # life ring
    d.ellipse([w - 44, 44, w - 12, 76], outline=(255, 255, 255), width=1)
    return img


CARD_SCENES = [card_uk_eu, card_poland, card_cop31, card_italy, card_japan,
               card_seoul, card_hormuz, card_bukele, card_phillips, card_dakar]

# ---------------------------------------------------------------- data (FROZEN)
DEK = ("Kyiv\u2019s bridges hit in the year\u2019s biggest barrage \u00b7 Akvan comes ashore "
       "in Odisha \u00b7 Asia\u2019s AI sell-off deepens \u00b7 Britain and the EU seal their reset")
STATS = [("3", "bridges over the Dnipro damaged in Kyiv"),
         ("300,000+", "people moved to shelters before Akvan"),
         ("\u22126.2%", "Taiwan\u2019s share index, Friday\u2019s close"),
         ("100,000", "youth visas a year in the UK-EU deal"),
         ("2.3%", "Japan\u2019s consumer inflation in October"),
         ("118", "runs by Glenn Phillips against India")]
REGIONS = [("EUROPE 9", RED), ("ASIA 7", TEAL), ("MIDDLE EAST 6", GOLD),
           ("AFRICA 5", GREEN), ("AMERICAS 5", NAVY), ("OCEANIA 3", PURPLE),
           ("GLOBAL 1", GRAY)]
LEADS = [
    ("KYIV", "OFFICIALS\u2019 COUNT", None, "KYIV, UKRAINE \u00b7 WAR",
     "Russian missiles hit three Kyiv bridges",
     "An overnight barrage of more than 110 missiles and 400 drones killed at least nine "
     "people across Ukraine and cut power and water in the capital. (Kyiv Independent, BBC)"),
    ("CYCLONE AKVAN", "WEATHER OFFICE", "LANDFALL \u00b7 8 AM", "ODISHA, INDIA \u00b7 CYCLONE",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed the coast near Gopalpur from about 8 am after more than 300,000 "
     "people were moved to shelters. No deaths were reported. (IMD, Deccan Herald)"),
    ("AI SELL-OFF", "CLOSING PRICES", None, "TAIPEI \u00b7 SEOUL \u00b7 TOKYO \u00b7 MARKETS",
     "AI sell-off sinks Asia\u2019s stock markets",
     "Taiwan\u2019s index fell 6.2% to end its worst week since 1991. Seoul lost 5.2% and "
     "Tokyo 5.1% as chipmakers led the slide. (Reuters, Bloomberg)"),
]
LEAD_SCENES = [scene_kyiv, scene_cyclone, scene_selloff]
CARDS = [
    ("UK-EU DEAL", "Agreed \u00b7 Reuters", "BRUSSELS \u00b7 DIPLOMACY",
     "UK and EU seal a \u201creset\u201d deal", "Food trade, youth visas, carbon link."),
    ("POLAND: OBJECTS DOWN", "Officials", "EASTERN POLAND \u00b7 SECURITY",
     "Russian missiles and a drone come down in Poland",
     "A Kh-101 in a field; two airports paused; no one hurt."),
    ("COP31: NO DEAL", "Deal text", "ANTALYA \u00b7 CLIMATE",
     "COP31 reaches its last day with no deal", "The draft text leaves out fossil fuels."),
    ("ITALY: STRIKE", "Unions", "ITALY \u00b7 LABOUR",
     "General strike over Italy\u2019s budget", "Workers and students march."),
    ("JAPAN: +2.3%", "Official data", "TOKYO \u00b7 ECONOMY",
     "Japan\u2019s inflation picks up to 2.3%", "A December rate rise stays in view."),
    ("SEOUL: IMPEACH", "Party vote", "SEOUL \u00b7 POLITICS",
     "Korea\u2019s ruling party to impeach the chief justice",
     "It follows an overturned conviction."),
    ("HORMUZ: SHUT", "Ship trackers", "STRAIT OF HORMUZ \u00b7 ENERGY",
     "Hormuz shut, Brent $92.50", "Tanker traffic halted; insurers pull cover."),
    ("BUKELE: 3RD BID", "Filing", "SAN SALVADOR \u00b7 POLITICS",
     "Bukele files to run for a third term", "The vote is on 28 February 2027."),
    ("PHILLIPS: 118", "Scorecard", "WELLINGTON \u00b7 CRICKET",
     "Phillips hits 118 against India", "Hundreds against India in all three formats."),
    ("DAKAR: BOAT SINKS", "Rescuers", "DAKAR, SENEGAL \u00b7 MIGRATION",
     "Migrant boat sinks; 4 dead", "A pirogue capsized off the coast; rescuers search."),
]
BRIEFS = [
    (14, "Lviv", "A strike on a railway station kills two", "BBC"),
    (15, "Moscow", "Russia decries Estonia\u2019s border closure", "Reuters"),
    (16, "Berlin", "School pupils strike against military service", "Al Jazeera"),
    (17, "London", "General says UK cyber attacks abroad", "Sky News"),
    (18, "Beijing", "China holds its loan rates for an 18th month", "Xinhua"),
    (19, "Tokyo", "SoftBank shares fall more than 14% in a day", "Al Jazeera"),
    (20, "Ganjam", "209 mm of rain falls as Akvan crosses Odisha", "PTI"),
    (21, "Lebanon", "Israeli air strikes hit the south and the east", "Anadolu"),
    (22, "Yemen", "Gunmen fire on a cargo ship off the coast", "UKMTO"),
    (23, "Abuja", "Court bars new evidence against Tinubu", "Channels TV"),
    (24, "Kampala", "Police told to enforce Ebola ban on rallies", "allAfrica"),
    (25, "Malawi", "Fuel crisis brings night-long petrol queues", "Al Jazeera"),
    (26, "Africa", "AfDB says 22 countries are in debt distress", "allAfrica"),
    (27, "New York", "Nasdaq futures fall 1.6% before the bell", "24/7 Wall St"),
    (28, "Washington", "Democrats query law firm\u2019s free work", "Al Jazeera"),
    (29, "Wellington", "Nicholls makes 175 in a stand of 216", "ICC"),
    (30, "Sydney", "Australian shares fall 1.6% in the sell-off", "Reuters"),
    (31, "Antalya", "Panama asks COP31 to cap world oil output", "Anadolu"),
    (32, "Antalya", "EU official calls the climate draft unacceptable", "RTE"),
    (33, "Turin", "ATP backs a plan to lift player pay past $350m", "Anadolu"),
]
PINS = [(1, 30, 50), (2, 85, 19), (3, 121, 25), (4, 4, 50), (5, 23, 52),
        (6, 30, 37), (7, 12, 42), (8, 139, 36), (9, 127, 37), (10, 56, 26),
        (11, -89, 13), (12, 175, -41), (13, -17, 14)]
DATE_CHECK = ("DATE CHECK \u2014 Left out as Thursday 19 November\u2019s news: the three-leader "
              "declaration in Shenzhen, Anthropic\u2019s IPO pricing, the World Court\u2019s ruling "
              "on Myanmar and GTA VI\u2019s midnight launch. Older still, not shown: the Riyadh "
              "tower attack and Voyager 1\u2019s light-day (18 Nov).")
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-85, 70), (-80, 73),
     (-76, 62), (-80, 58), (-78, 52), (-85, 50), (-90, 46), (-84, 42), (-76, 40),
     (-70, 42), (-70, 46), (-66, 45), (-60, 46), (-65, 50), (-78, 42), (-76, 36),
     (-76, 34), (-80, 32), (-81, 26), (-84, 30), (-90, 29), (-97, 26), (-97, 22),
     (-94, 18), (-90, 15), (-86, 13), (-83, 9), (-78, 8), (-92, 15), (-105, 20),
     (-110, 24), (-114, 30), (-120, 34), (-124, 40), (-124, 48), (-132, 56), (-152, 60)],
    [(-78, 8), (-72, 12), (-64, 10), (-52, 5), (-50, 0), (-44, -3), (-35, -8),
     (-40, -20), (-48, -26), (-56, -34), (-62, -39), (-65, -45), (-67, -52),
     (-69, -54), (-71, -50), (-73, -44), (-73, -37), (-71, -30), (-70, -20),
     (-75, -15), (-79, -8), (-80, -4), (-78, 2)],
    [(-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 49), (5, 50), (8, 54), (8, 57),
     (18, 56), (21, 60), (18, 66), (25, 71), (32, 70), (28, 66), (22, 65), (12, 56),
     (20, 54), (24, 58), (30, 60), (28, 41), (23, 40), (19, 42), (12, 44), (8, 44),
     (3, 43), (0, 39), (-2, 37), (-9, 37), (-9, 43)],
    [(-17, 15), (-10, 30), (-6, 35), (10, 37), (11, 34), (20, 32), (30, 31), (35, 28),
     (39, 21), (43, 12), (51, 12), (48, 5), (41, -2), (40, -10), (38, -18), (36, -22),
     (33, -26), (28, -33), (20, -35), (17, -32), (14, -22), (13, -12), (12, -6),
     (9, -1), (9, 4), (-8, 5), (-13, 8), (-17, 15)],
    [(32, 70), (45, 68), (60, 69), (75, 72), (90, 75), (105, 77), (120, 73), (135, 72),
     (150, 70), (165, 69), (178, 66), (178, 62), (162, 60), (156, 52), (142, 50),
     (140, 40), (135, 35), (129, 33), (122, 31), (121, 25), (114, 22), (108, 16),
     (106, 9), (103, 6), (100, 8), (98, 12), (95, 16), (92, 16), (89, 22), (86, 20),
     (80, 15), (77, 8), (73, 18), (68, 23), (61, 25), (57, 26), (52, 26), (48, 29),
     (50, 25), (55, 25), (58, 23), (59, 22), (55, 17), (52, 15), (45, 12), (43, 12),
     (39, 21), (35, 28), (36, 36), (30, 36), (27, 37), (30, 41), (33, 42), (36, 45),
     (33, 47), (30, 50), (28, 55), (30, 60), (32, 66)],
    [(113, -22), (114, -32), (118, -35), (124, -33), (130, -32), (135, -35), (138, -36),
     (140, -38), (145, -38), (150, -37), (153, -30), (153, -25), (150, -22), (146, -19),
     (142, -15), (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (117, -20),
     (113, -22)],
]


def chip(draw, x, y, text, font, bg, fg, pad=6):
    tw = draw.textlength(text, font=font)
    draw.rectangle([x, y, x + tw + pad * 2, y + font.size + pad], fill=bg)
    draw.text((x + pad, y + pad - 2), text, font=font, fill=fg)
    return x + tw + pad * 2


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rng = random.Random(20261120)  # fixed-seed paper grain
    for _ in range(2600):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        v = rng.choice([(238, 231, 214), (252, 247, 236)])
        d.point((x, y), fill=v)

    # ---- masthead
    y = 12
    d.text((M, y), "THE WORLD IN ONE DAY", font=sans(19, True), fill=RED)
    top_r = "33 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    f = sans(9, True)
    d.text((RIGHT - d.textlength(top_r, font=f), y + 5), top_r, font=f, fill=INK)
    y += 24
    d.rectangle([M, y, RIGHT, y + 3], fill=RED)
    y += 8
    # ---- date
    fdate = fit_font(d, "Friday 20 November 2026", SERIF.format("Bold"), 92, CW)
    d.text((M, y), "Friday 20 November 2026", font=fdate, fill=INK)
    bb = d.textbbox((M, y), "Friday 20 November 2026", font=fdate)
    y += (bb[3] - bb[1]) + 5
    y = text_block(d, (M, y), DEK, serif(16, "Italic"), INK, CW, 18, max_lines=2)
    y += 4
    # ---- stat strip
    d.rectangle([M, y, RIGHT, y + 2], fill=RED)
    y += 6
    colw = CW / 6
    for i, (num, label) in enumerate(STATS):
        x = M + i * colw
        fn = fit_font(d, num, SERIF.format("Bold"), 34, colw - 14)
        d.text((x + 4, y), num, font=fn, fill=RED if i in (0, 2, 5) else INK)
        text_block(d, (x + 4, y + 37), label, sans(9), INK, colw - 12, 10, max_lines=2)
        if i:
            d.line([(x, y + 2), (x, y + 52)], fill=RED, width=2)
    y += 60
    d.rectangle([M, y, RIGHT, y + 2], fill=RED)
    y += 7
    # ---- region chips
    x = M
    for label, color in REGIONS:
        x = chip(d, x, y, label, sans(10, True), color, CREAM, pad=7) + 8
    y += 27
    # ---- leads
    gap = 12
    lw = (CW - 2 * gap) // 3
    scene_h = 146
    lead_text_top = y + scene_h + 6
    lead_bottom = lead_text_top
    for i, (scene_fn, lead) in enumerate(zip(LEAD_SCENES, LEADS)):
        x = M + i * (lw + gap)
        banner, src_l, src_r, kicker, headline, dek = lead
        img.paste(scene_fn(lw, scene_h), (x, y))
        chip(d, x, y, banner, sans(16, True), RED, CREAM, pad=6)
        chip(d, x + 4, y + scene_h - 20, src_l, sans(8, True), DARKCHIP, CREAM, pad=4)
        if src_r:
            f2 = sans(8, True)
            tw = d.textlength(src_r, font=f2)
            d.rectangle([x + lw - tw - 12, y + scene_h - 20, x + lw - 4, y + scene_h - 4],
                        fill=NAVY)
            d.text((x + lw - tw - 8, y + scene_h - 18), src_r, font=f2, fill=CREAM)
        ty = lead_text_top
        d.ellipse([x, ty, x + 17, ty + 17], fill=RED)
        nf = sans(10, True)
        ns = str(i + 1)
        d.text((x + 8.5 - d.textlength(ns, font=nf) / 2, ty + 2), ns, font=nf, fill=CREAM)
        d.text((x + 23, ty + 2), kicker, font=sans(10, True), fill=INK)
        ty += 21
        ty = text_block(d, (x, ty), headline, serif(26), INK, lw, 28, max_lines=2)
        ty += 2
        ty = text_block(d, (x, ty), dek, sans(10), INK, lw, 12, max_lines=3)
        lead_bottom = max(lead_bottom, ty)
    y = lead_bottom + 5
    # ---- cards
    cgap = 10
    cardw = (CW - 4 * cgap) // 5
    band_h = 82
    for row in range(2):
        row_bottom = y
        for col in range(5):
            idx = row * 5 + col
            banner, tag, kicker, headline, dek = CARDS[idx]
            x = M + col * (cardw + cgap)
            img.paste(CARD_SCENES[idx](cardw, band_h), (x, y))
            bf = sans(12, True)
            while d.textlength(banner, font=bf) > cardw - 10 and bf.size > 8:
                bf = sans(bf.size - 1, True)
            chip(d, x, y, banner, bf, RED if idx % 3 else INK, CREAM, pad=4)
            tf = sans(7, True)
            ttxt = tag.upper()
            tw = d.textlength(ttxt, font=tf)
            d.rectangle([x + cardw - tw - 10, y + band_h - 16, x + cardw - 2, y + band_h - 2],
                        fill=DARKCHIP)
            d.text((x + cardw - tw - 6, y + band_h - 14), ttxt, font=tf, fill=CREAM)
            ty = y + band_h + 4
            d.text((x, ty), kicker, font=sans(8, True), fill=RED)
            ty += 12
            ty = text_block(d, (x, ty), headline, serif(15), INK, cardw, 16, max_lines=2)
            ty = text_block(d, (x, ty), dek, sans(8), INK, cardw, 9, max_lines=2)
            row_bottom = max(row_bottom, ty)
        y = row_bottom + 5
    # ---- map + briefs
    map_w = 262
    briefs_x = M + map_w + 14
    briefs_w = RIGHT - briefs_x
    col_w = (briefs_w - 14) // 2
    # pre-wrap briefs into lines of (text, font, color) tokens
    f_num, f_bold, f_reg = sans(8, True), sans(8, True), sans(8)

    def brief_lines(num, place, text, source):
        toks = [(f"{num} ", f_num, RED), (f"{place} \u2014 ", f_bold, INK),
                (text, f_reg, INK), (f" ({source})", f_reg, GRAY)]
        words = []
        for t, fnt, c in toks:
            for w_ in t.split(" "):
                if w_:
                    words.append((w_ + " ", fnt, c))
        if words:
            t0, f0, c0 = words[-1]
            words[-1] = (t0.rstrip(), f0, c0)
        lines, cur, curw = [], [], 0
        for wtxt, fnt, c in words:
            ww = d.textlength(wtxt, font=fnt)
            if cur and curw + ww > col_w:
                lines.append(cur)
                cur, curw = [], 0
            cur.append((wtxt, fnt, c))
            curw += ww
        if cur:
            lines.append(cur)
        return lines

    cols = [BRIEFS[:10], BRIEFS[10:]]
    col_lines = [[brief_lines(*b) for b in col] for col in cols]
    briefs_h = 18 + max(sum(len(bl) * 10 + 2 for bl in cl) for cl in col_lines)
    map_h = briefs_h
    d.rectangle([M, y, M + map_w, y + map_h], fill=NAVY)
    d.text((M + 10, y + 7), "WHERE IT HAPPENED", font=sans(12, True), fill=CREAM)
    mx0, my0 = M + 10, y + 28
    mw, mh = map_w - 20, map_h - 58

    def proj(lon, lat):
        return (mx0 + (lon + 170) / 360 * mw, my0 + (75 - lat) / 135 * mh)

    for cont in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in cont], fill=(232, 224, 200))
    for num, lon, lat in PINS:
        px, py = proj(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=CREAM, width=1)
        ns = str(num)
        nf = sans(7, True)
        d.text((px - d.textlength(ns, font=nf) / 2, py - 4), ns, font=nf, fill=(255, 255, 255))
    cap = "Each number is the story with that number on this page."
    text_block(d, (M + 10, y + map_h - 24), cap, sans(9), CREAM, map_w - 20, 11,
               max_lines=2)
    # briefs heading + columns
    d.text((briefs_x, y + 1), "ALSO ON FRIDAY 20 NOVEMBER \u2014 20 MORE STORIES",
           font=sans(12, True), fill=RED)
    for ci, cl in enumerate(col_lines):
        bx = briefs_x + ci * (col_w + 14)
        by = y + 18
        for bl in cl:
            for line in bl:
                lx = bx
                for wtxt, fnt, c in line:
                    d.text((lx, by), wtxt, font=fnt, fill=c)
                    lx += d.textlength(wtxt, font=fnt)
                by += 10
            by += 2
    y += briefs_h + 2
    d.text((briefs_x, y), "All briefs are dated Friday 20 November 2026.",
           font=sans(9), fill=GRAY)
    y += 13
    # ---- date check strip
    d.rectangle([M, y, RIGHT, y + 27], outline=RED, width=2)
    text_block(d, (M + 8, y + 4), DATE_CHECK, sans(9), INK, CW - 16, 12, max_lines=2)
    y += 32
    # ---- footer
    d.text((M, y), "Every story here happened, or was first reported, on Friday 20 November "
                   "2026. Officials\u2019 counts are attributed.", font=sans(9), fill=GRAY)
    fr = "Sources named beside each story \u00b7 original drawings"
    d.text((RIGHT - d.textlength(fr, font=sans(9)), y), fr, font=sans(9), fill=GRAY)

    print(f"layout bottom: footer y={y}")
    img.save(OUT)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
