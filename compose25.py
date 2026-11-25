#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (1024x1024).

Flat editorial art, one palette, no photos, no network. Deterministic:
running this script twice writes a byte-identical entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (253, 251, 245)
INK = (18, 18, 18)
GREY = (90, 88, 80)
RED = (176, 30, 36)
DARKRED = (140, 20, 26)
GREEN = (29, 107, 52)
GOLD = (184, 134, 11)
NAVY = (18, 32, 64)
MIDNAVY = (24, 42, 78)
SKY = (168, 196, 224)
ORANGE = (232, 122, 44)
FLAME = (244, 178, 44)
DARK = (32, 28, 30)
LIGHTGREY = (200, 198, 190)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, keeping words whole."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK):
    draw.text(xy, s, font=fnt, fill=fill)


def centred(draw, cx, y, s, fnt, fill=INK):
    w = draw.textlength(s, font=fnt)
    draw.text((cx - w / 2, y), s, font=fnt, fill=fill)


def rule(draw, y, x0=16, x1=1008, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def pill(draw, x, y, label, fill):
    """A small CONFIRMED / REPORTED tag with white bold text."""
    fnt = font(SANS_B, 10)
    w = draw.textlength(label, font=fnt) + 14
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=fill)
    draw.text((x + 7, y + 2), label, font=fnt, fill=(255, 255, 255))
    return x + w


def source_line(draw, x, y, tag, source):
    end = pill(draw, x, y, tag, GREEN if tag == "CONFIRMED" else GOLD)
    text(draw, (end + 6, y + 1), "Source: " + source, font(SANS, 11), GREY)


def card_source(draw, x, y, tag, source):
    """Pictured-card tag line: pill plus the source name, no 'Source:'."""
    end = pill(draw, x, y, tag, GREEN if tag == "CONFIRMED" else GOLD)
    text(draw, (end + 6, y + 1), source, font(SANS, 11), GREY)


def kicker(draw, x, y, s):
    text(draw, (x, y), s, font(SANS_B, 11), RED)


def headline(draw, x, y, s, size=22, width=318, leading=26):
    fnt = font(SERIF_B, size)
    lines = wrap(draw, s, fnt, width)
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=fnt, fill=INK)
    return y + len(lines) * leading


def body(draw, x, y, s, width=318, size=11, leading=14):
    fnt = font(SANS, size)
    for i, line in enumerate(wrap(draw, s, fnt, width)):
        draw.text((x, y + i * leading), line, font=fnt, fill=INK)
    return y + len(wrap(draw, s, fnt, width)) * leading


# ---- lead pictures -------------------------------------------------------

def flame(draw, x, y, w, h):
    """A flat orange-yellow flame triangle with a smaller inner flame."""
    draw.polygon([(x, y + h), (x + w / 2, y), (x + w, y + h)], fill=ORANGE)
    draw.polygon([(x + w * 0.25, y + h), (x + w / 2, y + h * 0.35),
                  (x + w * 0.75, y + h)], fill=FLAME)


def smoke(draw, x, y, r=9):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(45, 42, 44))
    draw.ellipse([x + r * 0.7, y - r * 0.5, x + r * 2.1, y + r * 0.9],
                 fill=(45, 42, 44))


def refinery_tower(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(110, 108, 104))
    for i in range(3):
        yy = y + 6 + i * (h - 8) // 3
        draw.line([(x + 2, yy), (x + w - 2, yy)], fill=(80, 78, 74), width=2)


def drone_cross(draw, x, y, s=7):
    draw.line([(x - s, y), (x + s, y)], fill=(220, 220, 220), width=2)
    draw.line([(x, y - s), (x, y + s)], fill=(220, 220, 220), width=2)
    draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=RED)


def lead_refinery(draw, x, y, w, h):
    """Ras Tanura: orange dusk sky, refinery towers on fire, Riyadh tower."""
    draw.rectangle([x, y, x + w, y + h], fill=(224, 138, 78))
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=DARK)
    for tx, tw in ((x + 12, 26), (x + 52, 26), (x + 92, 22)):
        refinery_tower(draw, tx, y + h * 0.42, tw, h * 0.58)
    flame(draw, x + 8, y + h * 0.22, 30, h * 0.24)
    flame(draw, x + 48, y + h * 0.28, 26, h * 0.20)
    flame(draw, x + 88, y + h * 0.30, 24, h * 0.18)
    smoke(draw, x + 28, y + h * 0.16)
    smoke(draw, x + 62, y + h * 0.12)
    draw.rectangle([x + 128, y + h * 0.62, x + 168, y + h * 0.86],
                   fill=(150, 148, 144))
    # Riyadh tower: pale blue slab with a gold diamond window.
    draw.polygon([(x + 205, y + h), (x + 212, y + 4), (x + 238, y + 4),
                  (x + 246, y + h)], fill=(146, 178, 214))
    for i in range(5):
        yy = y + 18 + i * 11
        draw.line([(x + 214, yy), (x + 240, yy)], fill=(110, 148, 190),
                  width=2)
    draw.polygon([(x + 214, y + 48), (x + 226, y + 38), (x + 238, y + 48),
                  (x + 226, y + 58)], fill=FLAME)
    drone_cross(draw, x + 262, y + 22)


def lead_gaza(draw, x, y, w, h):
    """Night street in Gaza: dark building, lit windows, blast at the side."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 16, 48))
    for sx, sy in ((x + 20, y + 10), (x + 90, y + 6), (x + 160, y + 14),
                   (x + 230, y + 8), (x + 280, y + 16)):
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(240, 240, 200))
    draw.ellipse([x + 258, y + 8, x + 292, y + 30], fill=(90, 90, 96))
    draw.ellipse([x + 276, y + 18, x + 306, y + 38], fill=(110, 110, 116))
    draw.rectangle([x + 18, y + 26, x + 268, y + h], fill=(96, 94, 90))
    for r in range(3):
        for c in range(9):
            wx = x + 30 + c * 27
            wy = y + 36 + r * 15
            lit = (r + c) % 3 == 0
            draw.rectangle([wx, wy, wx + 12, wy + 8],
                           fill=FLAME if lit else (40, 38, 40))
    draw.polygon([(x + 268, y + 34), (x + 306, y + 28), (x + 318, y + 40),
                  (x + 306, y + 52), (x + 318, y + 62), (x + 292, y + 66),
                  (x + 268, y + 62)], fill=ORANGE)
    draw.polygon([(x + 272, y + 42), (x + 296, y + 40), (x + 306, y + 48),
                  (x + 292, y + 56), (x + 274, y + 54)], fill=FLAME)


def lead_ukraine(draw, x, y, w, h):
    """Samara night: purple sky, two refineries burning, drones overhead."""
    draw.rectangle([x, y, x + w, y + h], fill=(88, 52, 102))
    draw.rectangle([x, y + h * 0.55, x + w, y + h], fill=(24, 20, 30))
    for tx in (x + 16, x + 140):
        refinery_tower(draw, tx, y + h * 0.40, 26, h * 0.60)
    flame(draw, x + 12, y + h * 0.18, 32, h * 0.26)
    flame(draw, x + 44, y + h * 0.24, 26, h * 0.20)
    flame(draw, x + 136, y + h * 0.20, 30, h * 0.24)
    smoke(draw, x + 30, y + h * 0.12)
    smoke(draw, x + 152, y + h * 0.10)
    draw.rectangle([x + 84, y + h * 0.62, x + 124, y + h * 0.86],
                   fill=(150, 148, 144))
    draw.rectangle([x + 196, y + h * 0.60, x + 240, y + h * 0.86],
                   fill=(150, 148, 144))
    flame(draw, x + 206, y + h * 0.38, 22, h * 0.22)
    for dx, dy in ((x + 90, y + 16), (x + 180, y + 12), (x + 250, y + 20),
                   (x + 292, y + 34)):
        drone_cross(draw, dx, dy)


# ---- pictured cards -------------------------------------------------------

def pic_markets(draw, x, y, w, h):
    """Falling chart on dark green, KOSPI -6.2%, Dow 50,000, red arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(12, 66, 34))
    for i in range(5):
        yy = y + 8 + i * (h - 16) // 4
        draw.line([(x + 4, yy), (x + w - 4, yy)], fill=(30, 96, 52), width=1)
    text(draw, (x + 8, y + 4), "KOSPI  -6.2%", font(SANS_B, 11),
         (255, 255, 255))
    text(draw, (x + 8, y + 20), "DOW 50,000", font(SANS_B, 9), FLAME)
    pts = [(x + 10, y + 26), (x + 50, y + 34), (x + 90, y + 30),
           (x + 120, y + 44), (x + 150, y + 50), (x + 175, y + 58)]
    draw.line(pts, fill=(238, 70, 60), width=2)
    draw.rectangle([x + w - 52, y + h - 26, x + w - 8, y + h - 4],
                   fill=(140, 20, 26))
    draw.polygon([(x + w - 40, y + h - 22), (x + w - 20, y + h - 22),
                  (x + w - 30, y + h - 8)], fill=(255, 255, 255))
    draw.rectangle([x + w - 33, y + h - 24, x + w - 27, y + h - 20],
                   fill=(255, 255, 255))


def pic_hormuz(draw, x, y, w, h):
    """Two tankers on a dark sea, one burning, mines below the waterline."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 214, 232))
    draw.rectangle([x, y + h * 0.42, x + w, y + h], fill=(22, 48, 92))
    for i in range(4):
        yy = y + h * 0.52 + i * 10
        draw.line([(x + 4, yy), (x + w - 4, yy)], fill=(48, 84, 138), width=1)
    draw.rectangle([x + 10, y + h * 0.52, x + 88, y + h * 0.68],
                   fill=(168, 168, 164))
    draw.rectangle([x + 10, y + h * 0.46, x + 88, y + h * 0.52],
                   fill=(176, 40, 40))
    draw.rectangle([x + 96, y + h * 0.52, x + 150, y + h * 0.68],
                   fill=(168, 168, 164))
    draw.rectangle([x + 96, y + h * 0.46, x + 150, y + h * 0.52],
                   fill=(176, 40, 40))
    draw.rectangle([x + 158, y + h * 0.56, x + 184, y + h * 0.68],
                   fill=(220, 220, 216))
    # Taller flames than the first pass: in entry.png they rise from the
    # deck almost to the top of the sky, so both start near the top of
    # the picture and end at the tanker deck (y + h * 0.46).
    flame(draw, x + 14, y + h * 0.02, 34, h * 0.44)
    flame(draw, x + 46, y + h * 0.08, 26, h * 0.38)
    smoke(draw, x + 30, y + h * 0.04)
    draw.rectangle([x + 66, y + h * 0.30, x + 76, y + h * 0.46],
                   fill=(240, 240, 236))
    draw.rectangle([x + 118, y + h * 0.32, x + 128, y + h * 0.46],
                   fill=(240, 240, 236))
    for mx, my in ((x + 52, y + h * 0.82), (x + 132, y + h * 0.86)):
        draw.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(10, 10, 12))
        for dx, dy in ((-7, 0), (7, 0), (0, -7), (0, 7)):
            draw.line([(mx, my), (mx + dx, my + dy)], fill=(10, 10, 12),
                      width=2)


def pic_huawei(draw, x, y, w, h):
    """Huawei red logo box, courthouse columns, GUILTY 10/12 stamp."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    draw.rectangle([x + 8, y + 8, x + 56, y + h - 8], fill=(176, 30, 36))
    draw.ellipse([x + 24, y + 16, x + 40, y + 40], fill=(255, 255, 255))
    text(draw, (x + 14, y + h - 22), "HUAWEI", font(SANS_B, 8),
         (255, 255, 255))
    draw.rectangle([x + 66, y + 12, x + w - 8, y + 20],
                   fill=(226, 220, 204))
    for i in range(4):
        cx = x + 82 + i * 26
        draw.rectangle([cx, y + 20, cx + 10, y + h - 12],
                       fill=(226, 220, 204))
    draw.rectangle([x + 66, y + h - 14, x + w - 8, y + h - 8],
                   fill=(226, 220, 204))
    # Wider stamp at larger type: in entry.png GUILTY 10/12 spans
    # almost the full width of the courthouse, centred on the columns.
    stamp(draw, x + 55, y + h - 32, 130, 20, "GUILTY 10/12", -14, size=17)


def stamp(draw, x, y, w, h, s, angle=-14, size=12):
    """A red diagonal rubber stamp, drawn on its own layer and rotated."""
    layer = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([8, 8, w + 8, h + 8], outline=RED, width=3)
    ld.text((12, 10), s, font=font(SANS_B, size), fill=RED)
    rot = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    draw._image.paste(rot, (int(x + w / 2 - rot.width / 2),
                            int(y + h / 2 - rot.height / 2)), rot)


def pic_dell(draw, x, y, w, h):
    """Three server racks and a rising gold arrow, AI $22bn."""
    draw.rectangle([x, y, x + w, y + h], fill=(10, 22, 52))
    for i, rx in enumerate((x + 10, x + 56, x + 102)):
        draw.rectangle([rx, y + 8, rx + 38, y + h - 8], fill=(16, 16, 20))
        for r in range(5):
            ry = y + 14 + r * 9
            draw.rectangle([rx + 5, ry, rx + 22, ry + 4], fill=(40, 40, 46))
            col = (60, 200, 90) if (r + i) % 2 else (220, 60, 50)
            draw.ellipse([rx + 28, ry, rx + 33, ry + 5], fill=col)
    pts = [(x + 128, y + h - 14), (x + 146, y + h - 26), (x + 160, y + h - 22),
           (x + 176, y + 12)]
    draw.line(pts, fill=FLAME, width=3)
    draw.polygon([(x + 168, y + 8), (x + 184, y + 8), (x + 178, y + 22)],
                 fill=FLAME)
    text(draw, (x + 138, y + h - 16), "AI $22bn", font(SANS_B, 10), FLAME)


def pic_colombia(draw, x, y, w, h):
    """ÉXITO supermarket front, two troops below, green check."""
    draw.rectangle([x, y, x + w, y + h], fill=(240, 238, 230))
    draw.rectangle([x, y, x + w, y + 14], fill=(176, 30, 36))
    text(draw, (x + 8, y + 2), "ÉXITO", font(SANS_B, 10), (255, 255, 255))
    for i in range(8):
        wx = x + 10 + i * 22
        draw.rectangle([wx, y + 20, wx + 14, y + 42], fill=(168, 200, 224))
    draw.rectangle([x, y + 46, x + w, y + h], fill=(120, 118, 112))
    for tx in (x + 56, x + 128):
        draw.ellipse([tx, y + 48, tx + 12, y + 60], fill=(30, 40, 70))
        draw.rectangle([tx - 4, y + 60, tx + 16, y + h - 2],
                       fill=(24, 34, 66))
        draw.ellipse([tx + 12, y + 52, tx + 16, y + 56], fill=FLAME)
    draw.ellipse([x + w - 30, y + 2, x + w - 4, y + 28], fill=GREEN)
    draw.line([(x + w - 25, y + 15), (x + w - 18, y + 22), (x + w - 8, y + 8)],
              fill=(255, 255, 255), width=3)


def pic_pacific(draw, x, y, w, h):
    """Union Jack and Solomons flag above a handshake."""
    draw.rectangle([x, y, x + w, y + h], fill=(168, 196, 224))
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=(150, 152, 156))
    # Union Jack, simplified.
    fx, fy, fw, fh = x + 12, y + 8, 62, 34
    draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(20, 40, 110))
    draw.line([(fx, fy), (fx + fw, fy + fh)], fill=(255, 255, 255), width=6)
    draw.line([(fx + fw, fy), (fx, fy + fh)], fill=(255, 255, 255), width=6)
    draw.line([(fx + fw // 2, fy), (fx + fw // 2, fy + fh)],
              fill=(255, 255, 255), width=10)
    draw.line([(fx, fy + fh // 2), (fx + fw, fy + fh // 2)],
              fill=(255, 255, 255), width=10)
    draw.line([(fx + fw // 2, fy), (fx + fw // 2, fy + fh)],
              fill=(200, 30, 40), width=5)
    draw.line([(fx, fy + fh // 2), (fx + fw, fy + fh // 2)],
              fill=(200, 30, 40), width=5)
    # Solomons flag: blue over green, diagonal, stars.
    gx, gy, gw, gh = x + 104, y + 8, 62, 34
    draw.rectangle([gx, gy, gx + gw, gy + gh], fill=(0, 90, 160))
    draw.polygon([(gx, gy + gh), (gx + gw, gy), (gx + gw, gy + gh)],
                 fill=(0, 130, 60))
    draw.line([(gx, gy + gh), (gx + gw, gy)], fill=(250, 210, 0), width=2)
    for sx, sy in ((gx + 12, gy + 8), (gx + 26, gy + 6), (gx + 40, gy + 10),
                   (gx + 20, gy + 16), (gx + 34, gy + 18)):
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # Handshake: two dark sleeves meeting at a tan clasp.
    draw.polygon([(x + 30, y + h), (x + 78, y + h - 22), (x + 96, y + h - 22),
                  (x + 60, y + h)], fill=(40, 40, 48))
    draw.polygon([(x + 168, y + h), (x + 120, y + h - 22),
                  (x + 102, y + h - 22), (x + 138, y + h)], fill=(40, 40, 48))
    draw.ellipse([x + 82, y + h - 26, x + 116, y + h - 4], fill=(232, 190, 140))


def pic_space(draw, x, y, w, h):
    """Rocket lifting off beside a station, Pakistan crescent at right."""
    draw.rectangle([x, y, x + w, y + h], fill=(10, 10, 34))
    for sx, sy in ((x + 14, y + 8), (x + 60, y + 6), (x + 110, y + 12),
                   (x + 160, y + 8), (x + 90, y + 20), (x + 140, y + 26)):
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # Rocket.
    draw.polygon([(x + 22, y + 18), (x + 30, y + 8), (x + 38, y + 18)],
                 fill=(200, 30, 40))
    draw.rectangle([x + 22, y + 18, x + 38, y + 52], fill=(240, 240, 236))
    draw.ellipse([x + 26, y + 24, x + 34, y + 32], fill=(90, 140, 210))
    flame(draw, x + 23, y + 52, 14, 12)
    # Station: grey module with blue solar panels.
    draw.rectangle([x + 88, y + 26, x + 132, y + 40], fill=(200, 198, 192))
    draw.rectangle([x + 62, y + 30, x + 88, y + 36], fill=(70, 90, 150))
    draw.rectangle([x + 132, y + 30, x + 158, y + 36], fill=(70, 90, 150))
    draw.ellipse([x + 106, y + 20, x + 114, y + 28], fill=FLAME)
    # Pakistan crescent and star.
    draw.ellipse([x + 164, y + h - 26, x + 186, y + h - 4], fill=(0, 130, 60))
    draw.ellipse([x + 170, y + h - 24, x + 190, y + h - 6], fill=(10, 10, 34))
    draw.polygon([(x + 182, y + h - 22), (x + 184, y + h - 17),
                  (x + 189, y + h - 17), (x + 185, y + h - 14),
                  (x + 186, y + h - 9), (x + 182, y + h - 12),
                  (x + 178, y + h - 9), (x + 179, y + h - 14),
                  (x + 174, y + h - 17), (x + 180, y + h - 17)],
                 fill=(255, 255, 255))


def pic_sudan(draw, x, y, w, h):
    """Brown city blocks under an orange sky, one blast, drone cross."""
    draw.rectangle([x, y, x + w, y + h], fill=(224, 150, 92))
    draw.rectangle([x, y + h * 0.5, x + w, y + h], fill=(110, 84, 52))
    for bx, bw, bh in ((x + 8, 52, 26), (x + 66, 40, 34), (x + 112, 56, 30),
                       (x + 172, 26, 22)):
        draw.rectangle([bx, y + h * 0.5 - bh + 22, bx + bw, y + h * 0.5 + 22],
                       fill=(96, 70, 40))
        for wx in range(3):
            draw.rectangle([bx + 6 + wx * 14, y + h * 0.5 - bh + 30,
                            bx + 12 + wx * 14, y + h * 0.5 - bh + 38],
                           fill=(50, 38, 26))
    # Taller, narrower flame, set further left: in entry.png a slim
    # flame rises from behind the second block's roof almost to the top
    # of the sky, with its smoke cloud above it to the left.
    flame(draw, x + 54, y + 2, 18, 24)
    smoke(draw, x + 50, y + 0)
    drone_cross(draw, x + 168, y + 14)


def pic_cop31(draw, x, y, w, h):
    """Pale dome and columns, yellow sun, COP31: NO DEAL stamp."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 226, 196))
    draw.ellipse([x + 78, y - 6, x + 138, y + 44], fill=(214, 196, 160))
    draw.rectangle([x + 60, y + 40, x + w - 10, y + h], fill=(206, 188, 150))
    for i in range(5):
        cx = x + 70 + i * 24
        draw.rectangle([cx, y + 44, cx + 8, y + h - 6], fill=(226, 210, 176))
    draw.ellipse([x + w - 34, y + 8, x + w - 10, y + 32], fill=FLAME)
    # Narrower stamp, shifted left: in entry.png COP31: NO DEAL
    # starts at the card's left edge at the same height as here
    # (red spans y596-631), with smaller type that fits inside the border.
    stamp(draw, x + 1, y + h - 28, 84, 18, "COP31: NO DEAL", -12, size=9)


def pic_tariffs(draw, x, y, w, h):
    """Container ship on a dark sea, TARIFF stamp across the boxes."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 214, 232))
    draw.rectangle([x, y + h * 0.45, x + w, y + h], fill=(16, 44, 96))
    for i in range(4):
        yy = y + h * 0.55 + i * 10
        draw.line([(x + 4, yy), (x + w - 4, yy)], fill=(48, 84, 138), width=1)
    cols = [(200, 40, 40), (0, 130, 60), (240, 200, 40), (40, 90, 180),
            (200, 40, 40), (0, 130, 60), (240, 200, 40)]
    for i, col in enumerate(cols):
        bx = x + 10 + i * 24
        draw.rectangle([bx, y + h * 0.30, bx + 20, y + h * 0.52], fill=col)
        draw.line([(bx + 10, y + h * 0.30), (bx + 10, y + h * 0.52)],
                  fill=(255, 255, 255), width=1)
    draw.rectangle([x + 178, y + h * 0.34, x + 192, y + h * 0.52],
                   fill=(240, 240, 236))
    draw.rectangle([x + 6, y + h * 0.52, x + w - 6, y + h * 0.60],
                   fill=(140, 20, 26))
    stamp(draw, x + 96, y + 10, 80, 18, "TARIFF", -16)


# ---- dotted world map -----------------------------------------------------

# LAND rows are (col_start, col_end) pairs, one list per row (26 rows):
LAND_ROWS = [
    [(2, 15), (17, 21), (30, 36), (44, 50)],
    [(2, 16), (17, 20), (29, 37), (42, 52)],
    [(3, 15), (28, 30), (30, 38), (40, 54)],
    [(4, 16), (29, 38), (39, 56)],
    [(5, 16), (29, 37), (38, 57), (59, 60)],
    [(5, 16), (30, 37), (38, 58), (59, 60)],
    [(6, 15), (30, 37), (38, 58)],
    [(7, 14), (30, 37), (39, 57)],
    [(7, 14), (30, 37), (40, 56)],
    [(8, 13), (30, 37), (41, 55)],
    [(8, 13), (29, 37), (42, 54)],
    [(9, 12), (29, 37), (43, 53)],
    [(9, 12), (11, 14), (30, 36), (44, 53)],
    [(10, 12), (11, 15), (30, 36), (46, 54)],
    [(11, 14), (31, 36), (48, 56)],
    [(11, 15), (31, 35), (49, 55)],
    [(11, 15), (31, 35)],
    [(12, 15), (31, 34), (52, 59)],
    [(12, 14), (31, 34), (52, 59)],
    [(12, 14), (53, 58)],
    [(12, 14), (53, 58)],
    [(12, 13)],
    [(12, 13)],
    [(12, 13)],
    [(12, 13)],
    [(12, 12)],
]

PINS = [
    (214, 872, "1"), (206, 862, "2"), (222, 846, "3"), (296, 866, "4"),
    (232, 882, "5"), (118, 848, "6"), (96, 866, "7"), (110, 888, "8"),
    (322, 912, "9"), (288, 848, "10"), (204, 894, "11"), (200, 844, "12"),
    (134, 862, "13"),
]


def draw_map(draw, x0, y0, cell=5.2):
    for r, spans in enumerate(LAND_ROWS):
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cx = x0 + c * cell + cell / 2
                cy = y0 + r * cell + cell / 2
                draw.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6],
                             fill=MIDNAVY)
    fnt = font(SANS_B, 11)
    for px, py, num in PINS:
        draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                     outline=(255, 255, 255), width=1)
        w = draw.textlength(num, font=fnt)
        draw.text((px - w / 2, py - 7), num, font=fnt, fill=(255, 255, 255))


# ---- page assembly --------------------------------------------------------

STRIP = [
    ("KOSPI", "-6.16%"), ("NIKKEI", "-2.78%"), ("DOW", "50,019"),
    ("BRENT", "$93.60"), ("DELL REV", "+103%"), ("HUAWEI", "10/12"),
    ("HOSTAGES", "FREED"), ("TANKERS", "2"), ("DRONES DOWNED", "145"),
    ("LANDMINE DEAD", "7,000"),
]

LEADS = [
    ("HOUTHIS \u2022 SAUDI ARABIA",
     "Houthis claim Ras Tanura refinery strike; Riyadh tower hit",
     "Yemen's Houthis say they hit Saudi Arabia's largest refinery and "
     "Riyadh's financial district. Satellite images show thick black "
     "smoke; the coalition says it shot down four drones. A tower strike "
     "a day earlier injured 11.",
     "REPORTED", "Reuters / Houthi spox", "refinery"),
    ("GAZA \u2022 ISRAEL\u2013HAMAS WAR",
     "Israeli strike kills Hamas internal security chief",
     "An Israeli air strike killed Mohammad Abuelouf, who headed Hamas's "
     "internal security service, along with his wife and two children, "
     "Gaza's interior ministry and medics say.",
     "CONFIRMED", "Gaza interior ministry", "gaza"),
    ("UKRAINE \u2022 RUSSIA",
     "Ukrainian drones set two Rosneft refineries ablaze",
     "Overnight strikes hit the Syzran and Kuibyshev refineries in "
     "Russia's Samara region; both were left ablaze. Moscow says 145 "
     "Ukrainian drones were shot down across Russia.",
     "CONFIRMED", "Reuters", "ukraine"),
]

CARDS = [
    ("MARKETS \u2022 ASIA", "Asia tumbles as chip sell-off spreads; Dow tops 50,000",
     "CONFIRMED", "Reuters / AP", "markets"),
    ("HORMUZ \u2022 UPDATE", "Two tankers hit mines in the Strait of Hormuz",
     "REPORTED", "IRGC statement", "hormuz"),
    ("US \u2022 HUAWEI", "Brooklyn jury convicts Huawei on 10 of 12 counts",
     "CONFIRMED", "Reuters / AP", "huawei"),
    ("TECH \u2022 DELL", "Dell posts record $54.9bn quarter on AI servers",
     "CONFIRMED", "Dell / SEC filing", "dell"),
    ("COLOMBIA", "Troops free all hostages in Cartagena supermarket siege",
     "CONFIRMED", "Reuters", "colombia"),
    ("PACIFIC", "Australia, Solomons sign treaty barring foreign bases",
     "CONFIRMED", "Reuters", "pacific"),
    ("SPACE", "Shenzhou-24 docks; Pakistan's first astronaut in orbit",
     "CONFIRMED", "Reuters", "space"),
    ("SUDAN", "RSF drone strikes kill 19 civilians in two cities",
     "CONFIRMED", "Reuters", "sudan"),
    ("VATICAN \u2022 CLIMATE", "Pope warns as COP31 talks end without a deal",
     "CONFIRMED", "Reuters", "cop31"),
    ("US \u2022 TRADE", "US proposes fresh tariffs on 14 partners, India included",
     "REPORTED", "Reuters", "tariffs"),
]

PIC_FNS = {"markets": pic_markets, "hormuz": pic_hormuz,
           "huawei": pic_huawei, "dell": pic_dell,
           "colombia": pic_colombia, "pacific": pic_pacific,
           "space": pic_space, "sudan": pic_sudan,
           "cop31": pic_cop31, "tariffs": pic_tariffs}
LEAD_FNS = {"refinery": lead_refinery, "gaza": lead_gaza,
            "ukraine": lead_ukraine}

TIMELINE = [
    ("00:10", "Ukraine drones hit Syzran, Kuibyshev refineries"),
    ("01:30", "Asian markets open sharply lower"),
    ("03:20", "Houthis claim Ras Tanura refinery strike"),
    ("06:45", "Coalition: four drones downed over Ras Tanura"),
    ("08:00", "Huawei verdict reported from Brooklyn"),
    ("09:52", "Dell posts record $54.9bn quarter"),
    ("11:40", "Israel kills Hamas security chief Abuelouf"),
    ("13:15", "Colombia troops free Cartagena hostages"),
    ("15:00", "Australia\u2013Solomons treaty signed in Canberra"),
]

ALSO_LEFT = [
    ("M. EAST", "Coalition strikes Hodeidah, Saada and Amran in reply"),
    ("M. EAST", "India condemns Riyadh attack; two nationals hurt"),
    ("M. EAST", "NASA imagery shows smoke over Ras Tanura"),
    ("M. EAST", "Second Riyadh tower strike in a week, after Nov 19 hit"),
    ("M. EAST", "Aramco, Saudi government silent on refinery hit"),
    ("N. AMER", "CIA/ODNI systems hit by cyberattack; no classified loss"),
    ("N. AMER", "Trump pardons two turkeys for Thanksgiving"),
    ("N. AMER", "Trump gives Giuliani the Medal of Freedom"),
    ("N. AMER", "Jensen Huang says he is in therapy as rally fades"),
    ("N. AMER", "Huawei to appeal; sentencing set for Sept 2027"),
    ("ASIA", "Bangladesh garment workers win 36% pay rise"),
]
ALSO_RIGHT = [
    ("ASIA", "N. Korea expels Swiss diplomat, shuts office"),
    ("ASIA", "Nvidia falls 5.9% a day after 31.5% surge"),
    ("ASIA", "SoftBank -14.8% as Nikkei slides 2.78%"),
    ("ASIA", "Samsung -9.9%, SK Hynix -11.1% in Seoul rout"),
    ("AFRICA", "WHO evacuates staff from DR Congo hospital"),
    ("AFRICA", "Landmine toll hits 5-year high of 7,000; Myanmar, Syria worst"),
    ("MARKETS", "Brent jumps above $93 on Ras Tanura claim"),
    ("MARKETS", "Taiex falls ~5% as chip rout spreads"),
    ("MARKETS", "Dow's first 50,000 close; S&P down 8th time in 9 days"),
]

DATE_CHECK_LINES = (
    "Four tankers hit mines in Hormuz (Mon 24 Nov) \u2022 Asia surges "
    "on Nvidia return (Mon 24 Nov) \u2022 Hamas chief Abu Nahel killed "
    "(Mon 24 Nov)",
    "Zaporizhzhia strike kills 2 (Mon 24 Nov) \u2022 350+ drones at "
    "Moscow (Mon 24 Nov) \u2022 Hanoi blast kills six (Mon 24 Nov) "
    "\u2022 Haftar in Ankara (Mon 24 Nov)",
)


def draw_briefs(draw, x, y, width, items, size=11):
    fnt = font(SANS, size)
    bold = font(SANS_B, size)
    lh = 11 if size <= 10 else 13
    yy = y
    for region, s in items:
        label = region + "  "
        lw = draw.textlength(label, font=bold)
        lines = wrap(draw, s, fnt, width - lw)
        draw.text((x, yy), label, font=bold, fill=RED)
        for i, line in enumerate(lines):
            draw.text((x + lw, yy + i * lh), line, font=fnt, fill=INK)
        yy += max(1, len(lines)) * lh + 1
    return yy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    rule(draw, 10, width=2)
    text(draw, (16, 16), "EST. 2026 \u2022 ONE DAY, ONE PAGE",
         font(SANS_B, 11), GREY)
    right = "PRICE: FREE \u2022 1024 x 1024"
    text(draw, (1008 - draw.textlength(right, font=font(SANS_B, 11)), 16),
         right, font(SANS_B, 11), GREY)
    centred(draw, 512, 28, "THE WORLD IN ONE DAY", font(SERIF_B, 66))
    centred(draw, 512, 96, "WEDNESDAY 25 NOVEMBER 2026",
            font(SANS_B, 25), RED)
    rule(draw, 126, width=3)
    rule(draw, 130, width=1)

    # Numbers strip.
    draw.rectangle([16, 136, 1008, 168], fill=(14, 14, 14))
    col_w = 992 / len(STRIP)
    for i, (label, value) in enumerate(STRIP):
        cx = 16 + col_w * (i + 0.5)
        centred(draw, cx, 139, label, font(SANS_B, 9), (170, 170, 165))
        centred(draw, cx, 151, value, font(SANS_B, 15), (255, 255, 255))

    # Three leads.
    lead_w, gap = 318, 19
    for i, (kick, head, body_text, tag, src, art) in enumerate(LEADS):
        x = 16 + i * (lead_w + gap)
        kicker(draw, x, 176, kick)
        headline(draw, x, 192, head, size=22, width=lead_w)
        LEAD_FNS[art](draw, x, 246, lead_w, 74)
        body(draw, x, 326, body_text, width=lead_w)
        source_line(draw, x, 386, tag, src)
    rule(draw, 408, width=2)

    # The day in pictures: two rows of five cards.
    text(draw, (16, 410), "THE DAY IN PICTURES", font(SERIF_B, 20))
    note = "Every picture shows its own story"
    text(draw, (1008 - draw.textlength(note, font=font(SANS, 11)), 415),
         note, font(SANS, 11), GREY)
    card_w, card_gap = 188, 13
    for row in range(2):
        for col in range(5):
            idx = row * 5 + col
            kick, head, tag, src, art = CARDS[idx]
            x = 16 + col * (card_w + card_gap)
            img_y = 434 + row * 134
            PIC_FNS[art](draw, x, img_y, card_w, 64)
            kicker(draw, x, img_y + 68, kick)
            fnt = font(SANS_B, 11)
            for j, line in enumerate(wrap(draw, head, fnt, card_w)):
                draw.text((x, img_y + 82 + j * 14), line, font=fnt, fill=INK)
            card_source(draw, x, img_y + 114, tag, src)
    rule(draw, 700, width=2)

    # The day in UTC: nine entries in three columns.
    text(draw, (16, 708), "THE DAY IN UTC", font(SERIF_B, 20))
    for i, (t, s) in enumerate(TIMELINE):
        col, r = i % 3, i // 3
        x = 16 + col * 330
        y = 730 + r * 17
        text(draw, (x, y), t, font(SANS_B, 11), RED)
        text(draw, (x + 44, y), s, font(SANS, 11))
    rule(draw, 782, width=2)

    # Map and ALSO ON briefs. The subtitle sits between the heading and
    # the map; the map and briefs start 12px lower than before, keeping
    # the heading-to-map gap tight so everything still clears the
    # date-check box at y=970.
    text(draw, (16, 790), "WHERE THE NEWS HAPPENED", font(SERIF_B, 18))
    text(draw, (352, 790), "ALSO ON", font(SERIF_B, 18))
    text(draw, (16, 810), "Pins mark the pictured stories",
         font(SANS, 11), GREY)
    draw_map(draw, 18, 824, cell=5.0)
    draw_briefs(draw, 352, 824, 320, ALSO_LEFT, size=10)
    draw_briefs(draw, 688, 824, 320, ALSO_RIGHT, size=10)

    # Date check box and sources footer. Two fixed lines, so the
    # "(Mon 24 Nov)" items are never split across lines.
    draw.rectangle([16, 970, 1008, 1006], outline=RED, width=2)
    fnt = font(SANS, 12)
    bold = font(SANS_B, 12)
    head_txt = "DATE CHECK \u2014 NOT TODAY'S NEWS:  "
    line1, line2 = DATE_CHECK_LINES
    draw.text((24, 974), head_txt, font=bold, fill=RED)
    draw.text((24 + draw.textlength(head_txt, font=bold), 974), line1,
              font=fnt, fill=INK)
    draw.text((24, 988), line2, font=fnt, fill=INK)
    text(draw, (16, 1009),
         "SOURCES: Reuters, AP, Gulf News, OilPrice, Japan Times, WSJ, Dell, "
         "SEC filing, ABC News, The Statesman", font(SANS, 10), GREY)

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
