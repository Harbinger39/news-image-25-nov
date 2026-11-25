#!/usr/bin/env python3
"""compose25.py — THE WORLD IN ONE DAY, Wednesday 25 November 2026.

Draws a dense newspaper front page (1024x1024) with PIL, flat editorial art,
one consistent palette, no photos, no network. Deterministic: same bytes
every run. Entry: entry.png beside this file.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (253, 251, 245)
INK = (18, 18, 18)
GREY = (90, 90, 86)
RED = (178, 34, 28)
NAVY = (16, 34, 64)
GREEN = (22, 110, 58)
GOLD = (196, 148, 28)
MX = 16

FDIR = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(f"{FDIR}/{name}.ttf", size)


SERIF_B = lambda s: F("DejaVuSerif-Bold", s)
SERIF = lambda s: F("DejaVuSerif", s)
SANS = lambda s: F("DejaVuSans", s)
SANS_B = lambda s: F("DejaVuSans-Bold", s)
MONO_B = lambda s: F("DejaVuSansMono-Bold", s)


def wrap(d, text, font, maxw):
    """Greedy word wrap to maxw pixels; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, font, maxw, max_lines):
    """Wrap and trim to max_lines, adding an ellipsis if trimmed."""
    lines = wrap(d, text, font, maxw)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + " ...", font=font) > maxw:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] = (lines[-1] + " ...").strip()
    return lines


def chip(d, x, y, text, fill):
    """CONFIRMED/REPORTED tag chip; returns width used."""
    font = SANS_B(8)
    tw = d.textlength(text, font=font)
    w = int(tw) + 10
    d.rounded_rectangle([x, y, x + w, y + 12], radius=3, fill=fill)
    d.text((x + 5, y + 2), text, font=font, fill=(255, 255, 255))
    return w


def star_points(cx, cy, r_out, r_in, rot=-90):
    import math
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


class _ScaledDraw:
    """Wraps ImageDraw, scaling 322x84 design coordinates into (w, h).

    Picture functions are authored once in a 322x84 design space (the lead
    size) and reused for the smaller card boxes; the wrapper scales every
    coordinate, line width and font size so the composition stays intact.
    """
    def __init__(self, draw, sx, sy):
        self._d = draw
        self.sx = sx
        self.sy = sy

    def _xy(self, pt):
        return (pt[0] * self.sx, pt[1] * self.sy)

    def _pts(self, pts):
        return [self._xy(p) for p in pts]

    def _box(self, box):
        return [box[0] * self.sx, box[1] * self.sy,
                box[2] * self.sx, box[3] * self.sy]

    def _kw(self, kw):
        kw = dict(kw)
        if "width" in kw:
            kw["width"] = max(1, int(round(kw["width"] * min(self.sx, self.sy))))
        return kw

    def rectangle(self, box, **kw):
        return self._d.rectangle(self._box(box), **self._kw(kw))

    def ellipse(self, box, **kw):
        return self._d.ellipse(self._box(box), **self._kw(kw))

    def polygon(self, pts, **kw):
        return self._d.polygon(self._pts(pts), **kw)

    def line(self, pts, **kw):
        return self._d.line(self._pts(pts), **self._kw(kw))

    def text(self, xy, text, font=None, **kw):
        if font is not None:
            fsize = max(6, int(round(font.size * self.sx)))
            try:
                font = ImageFont.truetype(font.path, fsize)
            except Exception:
                pass
        return self._d.text(self._xy(xy), text, font=font, **kw)



# ---------------------------------------------------------------- pictures
# Every picture is drawn on its own (w, h) layer and pasted in, so no shape
# can ever poke outside its box into the text around it.

def pic_hormuz(w, h):
    im = Image.new("RGB", (w, h), (14, 42, 84))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    d.rectangle([0, 0, w, int(h * 0.30)], fill=(196, 214, 232))  # hazy sky
    d.rectangle([0, int(h * 0.30), w, h], fill=(14, 42, 84))     # sea
    for i in range(5):  # wave lines
        yy = int(h * 0.38) + i * 9
        d.line([(8, yy), (w - 8, yy)], fill=(38, 84, 138), width=2)
    # tanker 1 (left, burning)
    d.rectangle([14, 52, 96, 64], fill=(150, 155, 160))
    d.rectangle([14, 52, 96, 56], fill=(178, 34, 28))
    d.rectangle([66, 38, 92, 52], fill=(235, 235, 230))
    d.rectangle([80, 30, 88, 38], fill=(178, 34, 28))
    # flames on tanker 1
    d.polygon([(30, 52), (40, 26), (48, 52)], fill=(240, 120, 20))
    d.polygon([(44, 52), (54, 20), (64, 52)], fill=(250, 180, 30))
    d.polygon([(58, 52), (68, 32), (76, 52)], fill=(240, 120, 20))
    # smoke column
    for r, yy in ((7, 18), (9, 10), (11, 2)):
        d.ellipse([52 - r, yy, 52 + r, yy + 2 * r], fill=(40, 40, 40))
    # tanker 2 (centre)
    d.rectangle([118, 56, 200, 68], fill=(150, 155, 160))
    d.rectangle([118, 56, 200, 60], fill=(178, 34, 28))
    d.rectangle([170, 42, 196, 56], fill=(235, 235, 230))
    d.rectangle([184, 34, 192, 42], fill=(178, 34, 28))
    # tanker 3 (right)
    d.rectangle([222, 56, 304, 68], fill=(150, 155, 160))
    d.rectangle([222, 56, 304, 60], fill=(178, 34, 28))
    d.rectangle([274, 42, 300, 56], fill=(235, 235, 230))
    # naval mines
    for cx, cy in ((112, 74), (262, 76)):
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(20, 20, 20))
        for ang in range(0, 360, 45):
            import math
            a = math.radians(ang)
            d.line([(cx + 5 * math.cos(a), cy + 5 * math.sin(a)),
                    (cx + 10 * math.cos(a), cy + 10 * math.sin(a))],
                   fill=(20, 20, 20), width=2)
    return im


def pic_gaza(w, h):
    im = Image.new("RGB", (w, h), (18, 18, 46))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    for sx, sy in ((20, 8), (60, 16), (120, 6), (200, 12), (280, 8), (300, 20), (160, 14)):
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 200))
    # apartment block
    d.rectangle([30, 24, 250, h], fill=(96, 94, 88))
    d.rectangle([30, 24, 250, 30], fill=(70, 68, 64))
    for r in range(3):
        for c in range(8):
            x0, y0 = 42 + c * 26, 36 + r * 16
            lit = (r + c) % 3 == 0
            d.rectangle([x0, y0, x0 + 14, y0 + 9],
                        fill=(250, 210, 90) if lit else (40, 40, 44))
    # blast bursting from the side
    d.polygon([(250, 40), (292, 30), (312, 48), (296, 58), (308, 66),
               (282, 72), (292, 80), (250, 74)], fill=(250, 140, 20))
    d.polygon([(250, 48), (282, 42), (296, 54), (282, 62), (250, 62)],
              fill=(255, 210, 60))
    # debris + smoke
    for dx, dy in ((262, 76), (276, 70), (290, 78), (300, 68)):
        d.rectangle([dx, dy, dx + 4, dy + 3], fill=(60, 58, 54))
    d.ellipse([256, 8, 288, 30], fill=(90, 88, 84))
    d.ellipse([272, 2, 300, 20], fill=(110, 108, 104))
    return im


def pic_rastanura(w, h):
    im = Image.new("RGB", (w, h), (30, 26, 48))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    d.rectangle([0, 0, w, int(h * 0.42)], fill=(214, 130, 80))  # dusk sky
    d.rectangle([0, int(h * 0.42), w, h], fill=(40, 34, 38))
    # refinery, left: distillation towers + storage tanks
    for tx, th in ((16, 34), (44, 44), (76, 30)):
        d.rectangle([tx, 62 - th, tx + 14, 62], fill=(120, 118, 112))
        d.rectangle([tx - 2, 62 - th - 4, tx + 16, 62 - th], fill=(90, 88, 84))
        for py in range(62 - th + 6, 60, 8):
            d.line([(tx, py), (tx + 14, py)], fill=(70, 68, 64), width=1)
    d.ellipse([104, 44, 138, 62], fill=(150, 148, 142))  # tank
    d.rectangle([104, 44, 138, 62], fill=(150, 148, 142))
    d.ellipse([104, 44, 138, 52], fill=(170, 168, 162))
    # flames + black smoke over the refinery
    d.polygon([(24, 28), (34, 8), (44, 28)], fill=(240, 120, 20))
    d.polygon([(40, 28), (52, 2), (64, 28)], fill=(250, 180, 30))
    d.ellipse([44, 0, 62, 12], fill=(30, 30, 30))
    d.ellipse([54, 0, 76, 10], fill=(50, 50, 50))
    d.polygon([(86, 32), (96, 16), (106, 32)], fill=(240, 120, 20))
    # KAFD skyscraper, right: tall twisted glass tower
    d.polygon([(196, h), (204, 10), (236, 6), (244, h)], fill=(120, 150, 190))
    d.polygon([(204, 10), (236, 6), (232, 26), (208, 30)], fill=(160, 190, 220))
    for wy in range(34, h - 6, 8):
        d.line([(208, wy), (240, wy - 2)], fill=(70, 100, 140), width=1)
    # impact flash midway up the tower + falling debris
    d.polygon([(196, 46), (214, 38), (226, 48), (214, 56)], fill=(250, 160, 30))
    d.ellipse([206, 42, 222, 54], fill=(255, 210, 80))
    for dx, dy in ((188, 62), (196, 70), (206, 66)):
        d.rectangle([dx, dy, dx + 4, dy + 3], fill=(90, 88, 84))
    # drone with red light above the tower
    d.line([(252, 16), (272, 16)], fill=(200, 200, 200), width=2)
    d.line([(262, 10), (262, 22)], fill=(200, 200, 200), width=2)
    d.ellipse([260, 14, 264, 18], fill=(255, 60, 40))
    d.line([(262, 22), (262, 30)], fill=(140, 140, 140), width=1)
    return im


def pic_refinery(w, h):
    im = Image.new("RGB", (w, h), (16, 16, 40))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    for sx_, sy_ in ((24, 8), (80, 6), (150, 10), (220, 7), (290, 9)):
        d.ellipse([sx_, sy_, sx_ + 2, sy_ + 2], fill=(255, 255, 220))
    d.rectangle([0, 0, w, int(h * 0.4)], fill=(90, 60, 90))  # night sky glow
    d.rectangle([0, int(h * 0.4), w, h], fill=(30, 26, 34))
    # two refinery columns ablaze
    for cx, ch in ((40, 40), (120, 48), (210, 36)):
        d.rectangle([cx, 66 - ch, cx + 18, 66], fill=(110, 108, 102))
        d.rectangle([cx - 3, 66 - ch - 4, cx + 21, 66 - ch], fill=(80, 78, 74))
        for py in range(66 - ch + 6, 64, 8):
            d.line([(cx, py), (cx + 18, py)], fill=(64, 62, 58), width=1)
    # storage tanks
    for tx in (170, 250):
        d.rectangle([tx, 52, tx + 40, 66], fill=(140, 138, 132))
        d.ellipse([tx, 52, tx + 40, 58], fill=(160, 158, 152))
    # big flames on both columns + smoke
    d.polygon([(44, 26), (56, 2), (68, 26)], fill=(240, 120, 20))
    d.polygon([(58, 26), (72, 0), (84, 26)], fill=(250, 180, 30))
    d.polygon([(124, 18), (136, 0), (148, 18)], fill=(240, 120, 20))
    d.ellipse([58, 0, 78, 10], fill=(30, 30, 30))
    d.ellipse([128, 0, 148, 8], fill=(50, 50, 50))
    d.polygon([(214, 30), (224, 14), (234, 30)], fill=(250, 180, 30))
    # drone swarm with red lights
    for dx, dy in ((90, 12), (160, 8), (240, 14), (290, 10), (200, 22)):
        d.line([(dx - 6, dy), (dx + 6, dy)], fill=(170, 170, 170), width=2)
        d.line([(dx, dy - 6), (dx, dy + 6)], fill=(170, 170, 170), width=2)
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 60, 40))
    return im


def pic_markets(w, h):
    im = Image.new("RGB", (w, h), (10, 58, 32))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    for gy in (16, 32, 48, 64):
        d.line([(8, gy), (w - 8, gy)], fill=(30, 96, 58), width=1)
    # falling red chart line
    pts = [(12, 14), (50, 22), (90, 18), (130, 34), (170, 40),
           (210, 52), (250, 58), (292, 72)]
    d.line(pts, fill=(255, 70, 60), width=4)
    d.polygon([(292, 72), (280, 66), (282, 80)], fill=(255, 70, 60))
    d.ellipse([284, 64, 300, 80], fill=(255, 70, 60))
    # red down arrow badge
    d.rectangle([w - 74, h - 34, w - 12, h - 8], fill=(120, 10, 10))
    d.rectangle([w - 74, h - 34, w - 12, h - 8], outline=(255, 120, 110), width=2)
    d.polygon([(w - 43, h - 30), (w - 31, h - 30), (w - 31, h - 20),
               (w - 25, h - 20), (w - 37, h - 10), (w - 49, h - 20),
               (w - 43, h - 20)], fill=(255, 255, 255))
    d.text((14, 4), "KOSPI -6.2%", font=SANS_B(15), fill=(255, 255, 255))
    d.text((14, 22), "DOW 50,000", font=SANS_B(11), fill=(255, 210, 60))
    return im


def pic_huawei(w, h):
    im = Image.new("RGB", (w, h), NAVY)
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    # smartphone, left
    d.rectangle([20, 8, 92, 76], fill=(20, 20, 26))
    d.rectangle([20, 8, 92, 76], outline=(150, 150, 160), width=2)
    d.rectangle([28, 18, 84, 60], fill=(178, 34, 28))
    d.ellipse([46, 28, 66, 48], fill=(255, 255, 255))
    d.text((34, 62), "HUAWEI", font=SANS_B(9), fill=(255, 255, 255))
    # courthouse columns, centre-right
    d.rectangle([120, 20, 300, 28], fill=(232, 226, 210))
    for cx in range(132, 300, 34):
        d.rectangle([cx, 28, cx + 12, 68], fill=(210, 204, 186))
        d.rectangle([cx - 2, 26, cx + 14, 29], fill=(196, 188, 168))
    d.rectangle([120, 68, 300, 74], fill=(196, 188, 168))
    # red GUILTY 10/12 stamp, rotated
    stamp = Image.new("RGBA", (190, 26), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([1, 1, 188, 24], outline=(220, 40, 30, 255), width=3)
    sd.text((10, 5), "GUILTY  10 / 12", font=SANS_B(14), fill=(220, 40, 30, 255))
    stamp = stamp.rotate(12, expand=True, resample=Image.BICUBIC)
    stamp = stamp.resize((max(1, int(stamp.width * sx)),
                          max(1, int(stamp.height * sy))), Image.LANCZOS)
    im.paste(stamp, (int(110 * sx), int(30 * sy)), stamp)
    return im


def pic_dell(w, h):
    im = Image.new("RGB", (w, h), (10, 30, 60))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    # three server racks with status lights
    for rx in (16, 78, 140):
        d.rectangle([rx, 12, rx + 48, 72], fill=(24, 24, 30))
        d.rectangle([rx, 12, rx + 48, 72], outline=(90, 110, 140), width=1)
        for ry in range(18, 68, 10):
            d.rectangle([rx + 5, ry, rx + 43, ry + 5], fill=(40, 44, 52))
            lit = (ry // 10 + rx) % 3 == 0
            d.ellipse([rx + 38, ry + 1, rx + 42, ry + 4],
                      fill=(60, 220, 110) if lit else (200, 60, 50))
    # rising gold chart over the racks
    pts = [(200, 66), (230, 54), (258, 58), (286, 34), (310, 22)]
    d.line(pts, fill=(255, 210, 60), width=4)
    d.polygon([(310, 22), (298, 22), (308, 34)], fill=(255, 210, 60))
    d.text((200, 68), "AI $22bn", font=SANS_B(13), fill=(255, 210, 60))
    return im


def pic_cartagena(w, h):
    im = Image.new("RGB", (w, h), (232, 226, 210))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    # supermarket frontage
    d.rectangle([0, 6, w, 16], fill=(178, 34, 28))
    d.text((12, 8), "ÉXITO", font=SANS_B(10), fill=(255, 255, 255))
    d.rectangle([0, 16, w, 56], fill=(245, 243, 236))
    for wx in range(14, w - 20, 36):
        d.rectangle([wx, 22, wx + 26, 50], fill=(180, 210, 225))
        d.line([(wx + 13, 22), (wx + 13, 50)], fill=(120, 120, 120), width=2)
    d.rectangle([0, 56, w, h], fill=(110, 110, 112))  # street
    d.line([(0, 56), (w, 56)], fill=(70, 70, 72), width=2)
    # two police officers with shields, foreground
    for ox in (96, 190):
        d.ellipse([ox + 6, 58, ox + 18, 70], fill=(214, 164, 120))  # head
        d.ellipse([ox + 6, 58, ox + 18, 64], fill=(20, 40, 90))    # helmet
        d.rectangle([ox, 70, ox + 24, 82], fill=(20, 40, 90))       # body
        d.rectangle([ox + 26, 64, ox + 34, 82], fill=(40, 60, 120))  # shield
        d.ellipse([ox + 28, 70, ox + 32, 74], fill=(255, 210, 60))
    # green freed check badge
    d.ellipse([w - 46, 4, w - 14, 28], fill=(22, 110, 58))
    d.line([(w - 40, 16), (w - 32, 24), (w - 20, 10)], fill=(255, 255, 255), width=3)
    return im


def pic_treaty(w, h):
    im = Image.new("RGB", (w, h), (168, 196, 224))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    d.rectangle([0, 54, w, h], fill=(120, 128, 140))
    for bx, bh in ((10, 22), (280, 26)):
        d.rectangle([bx, 54 - bh + 22, bx + 34, 76], fill=(96, 102, 116))
    # Australian flag (left)
    d.rectangle([40, 8, 150, 46], fill=(0, 36, 125))
    d.polygon([(40, 8), (54, 8), (150, 46), (136, 46)], fill=(255, 255, 255))
    d.polygon([(150, 8), (136, 8), (40, 46), (54, 46)], fill=(255, 255, 255))
    d.rectangle([88, 8, 102, 46], fill=(255, 255, 255))
    d.rectangle([40, 24, 150, 30], fill=(255, 255, 255))
    d.rectangle([91, 8, 99, 46], fill=(200, 16, 46))
    d.rectangle([40, 25, 150, 29], fill=(200, 16, 46))
    d.ellipse([128, 12, 132, 16], fill=(255, 255, 255))
    d.ellipse([118, 34, 122, 38], fill=(255, 255, 255))
    d.ellipse([138, 34, 142, 38], fill=(255, 255, 255))
    # Solomon Islands flag (right)
    d.polygon([(172, 8), (282, 8), (282, 46), (172, 46)], fill=(0, 96, 160))
    d.polygon([(172, 46), (282, 8), (282, 46)], fill=(0, 128, 0))
    d.line([(172, 46), (282, 8)], fill=(250, 210, 60), width=4)
    for sx_, sy_ in ((196, 12), (214, 16), (232, 12), (250, 16), (268, 12)):
        d.ellipse([sx_, sy_, sx_ + 3, sy_ + 3], fill=(255, 255, 255))
    # handshake: two sleeves meeting at centre
    d.polygon([(40, h), (120, 62), (150, 74), (90, h)], fill=(40, 40, 56))
    d.polygon([(w - 40, h), (w - 120, 62), (w - 150, 74), (w - 90, h)], fill=(60, 60, 74))
    d.ellipse([128, 56, 192, 78], fill=(214, 164, 120))
    d.ellipse([140, 52, 180, 66], fill=(226, 178, 134))
    return im


def pic_space(w, h):
    im = Image.new("RGB", (w, h), (8, 8, 24))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    for sx_, sy_ in ((16, 10), (60, 6), (120, 12), (180, 8), (240, 6), (300, 12), (90, 20), (210, 18)):
        d.ellipse([sx_, sy_, sx_ + 2, sy_ + 2], fill=(255, 255, 220))
    # rocket climbing, left
    d.polygon([(52, 70), (62, 20), (72, 70)], fill=(235, 235, 230))
    d.polygon([(62, 20), (52, 34), (62, 28)], fill=(178, 34, 28))
    d.polygon([(52, 70), (44, 78), (52, 72)], fill=(178, 34, 28))
    d.polygon([(72, 70), (80, 78), (72, 72)], fill=(178, 34, 28))
    d.polygon([(56, 78), (62, 60), (68, 78)], fill=(250, 180, 30))
    d.polygon([(58, 78), (62, 66), (66, 78)], fill=(240, 120, 20))
    d.ellipse([58, 34, 66, 42], fill=(40, 120, 200))
    # space station with solar panels, right
    d.rectangle([170, 30, 250, 44], fill=(200, 200, 205))
    d.rectangle([170, 30, 250, 34], fill=(150, 150, 155))
    d.rectangle([120, 34, 170, 40], fill=(40, 60, 140))
    d.rectangle([250, 34, 300, 40], fill=(40, 60, 140))
    for px in range(124, 168, 10):
        d.line([(px, 34), (px, 40)], fill=(120, 160, 220), width=1)
    for px in range(254, 298, 10):
        d.line([(px, 34), (px, 40)], fill=(120, 160, 220), width=1)
    d.ellipse([206, 22, 214, 30], fill=(255, 210, 60))
    # green crescent + star badge (first Pakistani in orbit)
    d.ellipse([280, 52, 312, 76], fill=(0, 128, 0))
    d.ellipse([288, 54, 314, 74], fill=(8, 8, 24))
    d.polygon(star_points(300, 64, 5, 2), fill=(255, 255, 255))
    return im


def pic_sudan(w, h):
    im = Image.new("RGB", (w, h), (214, 140, 90))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    d.rectangle([0, 0, w, int(h * 0.45)], fill=(214, 140, 90))  # dusk sky
    d.rectangle([0, int(h * 0.45), w, h], fill=(90, 70, 50))
    # low desert town silhouette
    for bx, bw, bh in ((10, 60, 22), (80, 44, 30), (130, 70, 18), (210, 54, 26), (272, 40, 20)):
        d.rectangle([bx, 62 - bh, bx + bw, 62], fill=(120, 96, 70))
        for wx in range(bx + 6, bx + bw - 6, 12):
            d.rectangle([wx, 62 - bh + 6, wx + 6, 62 - bh + 12],
                        fill=(250, 210, 90) if (wx + bh) % 3 == 0 else (60, 50, 40))
    # strike flash + smoke over one block
    d.polygon([(90, 32), (102, 12), (114, 32)], fill=(250, 160, 30))
    d.polygon([(98, 32), (108, 18), (118, 32)], fill=(255, 210, 80))
    d.ellipse([96, 2, 118, 16], fill=(60, 58, 54))
    d.ellipse([108, 0, 126, 10], fill=(90, 88, 84))
    # drone with red light overhead
    d.line([(220, 12), (244, 12)], fill=(200, 200, 200), width=2)
    d.line([(232, 6), (232, 18)], fill=(200, 200, 200), width=2)
    d.ellipse([230, 10, 234, 14], fill=(255, 60, 40))
    d.line([(232, 18), (232, 26)], fill=(140, 140, 140), width=1)
    # rubble at the base
    for dx, dy in ((96, 66), (110, 68), (122, 66)):
        d.rectangle([dx, dy, dx + 6, dy + 4], fill=(60, 54, 48))
    return im


def pic_pope(w, h):
    im = Image.new("RGB", (w, h), (232, 214, 170))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    d.rectangle([0, 0, w, 30], fill=(240, 226, 190))
    d.ellipse([w - 52, 6, w - 20, 34], fill=(250, 210, 90))  # sun
    # St Peter's dome + colonnade
    d.rectangle([0, 56, w, h], fill=(196, 176, 140))
    d.ellipse([116, 8, 206, 62], fill=(214, 196, 160))
    d.rectangle([150, 2, 172, 14], fill=(214, 196, 160))
    d.line([(161, 2), (161, -4)], fill=(196, 148, 28), width=2)
    d.rectangle([96, 56, 226, 62], fill=(178, 158, 124))
    for cx in range(104, 220, 18):
        d.rectangle([cx, 62, cx + 8, 78], fill=(214, 196, 160))
    # red NO DEAL stamp
    stamp = Image.new("RGBA", (150, 26), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([1, 1, 148, 24], outline=(220, 40, 30, 255), width=3)
    sd.text((10, 5), "COP31: NO DEAL", font=SANS_B(13), fill=(220, 40, 30, 255))
    stamp = stamp.rotate(-10, expand=True, resample=Image.BICUBIC)
    stamp = stamp.resize((max(1, int(stamp.width * sx)),
                          max(1, int(stamp.height * sy))), Image.LANCZOS)
    im.paste(stamp, (int(14 * sx), int(34 * sy)), stamp)
    return im


def pic_tariff(w, h):
    im = Image.new("RGB", (w, h), (14, 42, 84))
    _W, _H = w, h
    w, h = 322, 84
    sx, sy = _W / 322.0, _H / 84.0
    d = _ScaledDraw(ImageDraw.Draw(im), sx, sy)
    d.rectangle([0, 0, w, int(h * 0.30)], fill=(196, 214, 232))  # hazy sky
    d.rectangle([0, int(h * 0.30), w, h], fill=(14, 42, 84))     # sea
    for i in range(4):
        yy = int(h * 0.40) + i * 10
        d.line([(8, yy), (w - 8, yy)], fill=(38, 84, 138), width=2)
    # container ship
    d.rectangle([30, 58, 292, 70], fill=(40, 40, 44))
    d.rectangle([30, 58, 292, 62], fill=(178, 34, 28))
    d.rectangle([256, 40, 282, 58], fill=(235, 235, 230))
    cols = [(178, 34, 28), (22, 110, 58), (196, 148, 28), (40, 90, 160)]
    for r in range(2):
        for c in range(6):
            x0 = 44 + c * 36
            y0 = 34 + r * 12
            d.rectangle([x0, y0, x0 + 32, y0 + 11], fill=cols[(r + c) % 4])
            d.line([(x0 + 8, y0), (x0 + 8, y0 + 11)], fill=(255, 255, 255), width=1)
            d.line([(x0 + 16, y0), (x0 + 16, y0 + 11)], fill=(255, 255, 255), width=1)
            d.line([(x0 + 24, y0), (x0 + 24, y0 + 11)], fill=(255, 255, 255), width=1)
    # red TARIFF stamp across the sky
    stamp = Image.new("RGBA", (150, 26), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([1, 1, 148, 24], outline=(220, 40, 30, 255), width=3)
    sd.text((10, 5), "TARIFF  +14", font=SANS_B(14), fill=(220, 40, 30, 255))
    stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
    stamp = stamp.resize((max(1, int(stamp.width * sx)),
                          max(1, int(stamp.height * sy))), Image.LANCZOS)
    im.paste(stamp, (int(90 * sx), int(2 * sy)), stamp)
    return im


# ---------------------------------------------------------------- layout

LAND = [
    (0, 8, 14), (0, 19, 21), (0, 40, 58),
    (1, 4, 7), (1, 8, 16), (1, 18, 21), (1, 30, 32), (1, 34, 58),
    (2, 5, 8), (2, 8, 16), (2, 18, 20), (2, 29, 31), (2, 33, 58),
    (3, 7, 16), (3, 28, 28), (3, 29, 31), (3, 33, 57),
    (4, 8, 15), (4, 28, 28), (4, 30, 35), (4, 36, 56), (4, 56, 57),
    (5, 7, 15), (5, 30, 36), (5, 38, 54),
    (6, 8, 15), (6, 30, 35), (6, 38, 52),
    (7, 8, 15), (7, 30, 34), (7, 35, 38), (7, 39, 51),
    (8, 8, 14), (8, 30, 33), (8, 36, 40), (8, 44, 50),
    (9, 9, 14), (9, 29, 35), (9, 36, 39), (9, 41, 50),
    (10, 9, 12), (10, 29, 36), (10, 37, 39), (10, 41, 43), (10, 46, 49),
    (11, 10, 13), (11, 30, 37), (11, 42, 44), (11, 46, 50),
    (12, 12, 13), (12, 30, 37), (12, 47, 50),
    (13, 14, 17), (13, 30, 37), (13, 47, 49), (13, 48, 52),
    (14, 14, 18), (14, 31, 36), (14, 48, 53),
    (15, 14, 18), (15, 31, 35), (15, 49, 53),
    (16, 14, 18), (16, 31, 35), (16, 50, 54),
    (17, 14, 17), (17, 31, 34), (17, 51, 56),
    (18, 15, 17), (18, 32, 34), (18, 50, 57),
    (19, 15, 17), (19, 32, 33), (19, 37, 37), (19, 50, 57),
    (20, 15, 17), (20, 32, 33), (20, 51, 56),
    (21, 15, 16), (21, 32, 33), (21, 52, 56), (21, 58, 59),
    (22, 15, 16), (22, 32, 32), (22, 53, 55), (22, 59, 59),
    (23, 15, 16), (23, 59, 59),
    (24, 15, 15),
    (25, 15, 15),
]

PINS = [  # (number, lon, lat, dx, dy)
    (1, 50.1, 26.6, -8, -26),    # Ras Tanura
    (2, 46.7, 24.7, -26, -4),    # Riyadh
    (3, 34.5, 31.5, -30, 26),    # Gaza
    (4, 48.5, 53.2, 16, -16),    # Syzran
    (5, 127, 37.5, 0, 0),        # Seoul
    (6, 56.5, 26.5, 22, 10),     # Hormuz
    (7, -74.0, 40.7, 12, -10),   # Brooklyn
    (8, -75.5, 10.4, 0, 0),      # Cartagena
    (9, 149.1, -35.3, 0, 0),     # Canberra
    (10, 100.3, 41.0, -14, -10), # Jiuquan
    (11, 24.4, 13.6, 14, 8),     # Sudan
    (12, 12.45, 41.9, -16, -14), # Rome
    (13, -77.0, 38.9, -14, 10),  # Washington
]

LEADS = [
    dict(kicker="HOUTHIS \u2022 SAUDI ARABIA",
         headline="Houthis claim Ras Tanura refinery strike; Riyadh tower hit",
         body="Yemen's Houthis say they hit Saudi Arabia's largest refinery and Riyadh's financial district. Satellite images show thick black smoke; the coalition says it shot down four drones. A tower strike a day earlier injured 11.",
         tag="REPORTED", tagfill=GOLD,
         source="Reuters / Houthi spox",
         pic=pic_rastanura),
    dict(kicker="GAZA \u2022 ISRAEL\u2013HAMAS WAR",
         headline="Israeli strike kills Hamas internal security chief",
         body="An Israeli air strike killed Mohammad Abuelouf, who headed Hamas's internal security service, along with his wife and two children, Gaza's interior ministry and medics say.",
         tag="CONFIRMED", tagfill=GREEN,
         source="Gaza interior ministry",
         pic=pic_gaza),
    dict(kicker="UKRAINE \u2022 RUSSIA",
         headline="Ukrainian drones set two Rosneft refineries ablaze",
         body="Overnight strikes hit the Syzran and Kuibyshev refineries in Russia's Samara region; both were left ablaze. Moscow says 145 Ukrainian drones were shot down across Russia.",
         tag="CONFIRMED", tagfill=GREEN,
         source="Reuters",
         pic=pic_refinery),
]

CARDS = [
    ("MARKETS \u2022 ASIA", "Asia tumbles as chip sell-off spreads; Dow tops 50,000",
     "CONFIRMED", GREEN, "Reuters / AP", pic_markets),
    ("HORMUZ \u2022 UPDATE", "Two tankers hit mines in the Strait of Hormuz",
     "REPORTED", GOLD, "IRGC statement", pic_hormuz),
    ("US \u2022 HUAWEI", "Brooklyn jury convicts Huawei on 10 of 12 counts",
     "CONFIRMED", GREEN, "Reuters / AP", pic_huawei),
    ("TECH \u2022 DELL", "Dell posts record $54.9bn quarter on AI servers",
     "CONFIRMED", GREEN, "Dell / SEC filing", pic_dell),
    ("COLOMBIA", "Troops free all hostages in Cartagena supermarket siege",
     "CONFIRMED", GREEN, "Reuters", pic_cartagena),
    ("PACIFIC", "Australia, Solomons sign treaty barring foreign bases",
     "CONFIRMED", GREEN, "Reuters", pic_treaty),
    ("SPACE", "Shenzhou-24 docks; Pakistan's first astronaut in orbit",
     "CONFIRMED", GREEN, "Reuters", pic_space),
    ("SUDAN", "RSF drone strikes kill 19 civilians in two cities",
     "CONFIRMED", GREEN, "Reuters", pic_sudan),
    ("VATICAN \u2022 CLIMATE", "Pope warns as COP31 talks end without a deal",
     "CONFIRMED", GREEN, "Reuters", pic_pope),
    ("US \u2022 TRADE", "US proposes fresh tariffs on 14 partners, India included",
     "REPORTED", GOLD, "Reuters", pic_tariff),
]

NUMBERS = [
    ("KOSPI", "-6.16%"), ("NIKKEI", "-2.78%"), ("DOW", "50,019"),
    ("BRENT", "$93.60"), ("DELL REV", "+103%"), ("HUAWEI", "10/12"),
    ("HOSTAGES", "FREED"), ("TANKERS", "2"), ("DRONES DOWNED", "145"),
    ("LANDMINE DEAD", "7,000"),
]

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

ALSO_ON = [
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


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.line([(MX, 10), (W - MX, 10)], fill=INK, width=1)
    d.text((MX, 15), "EST. 2026 \u2022 ONE DAY, ONE PAGE", font=SANS_B(10), fill=GREY)
    right = "PRICE: FREE \u2022 1024 x 1024"
    d.text((W - MX - d.textlength(right, font=SANS_B(10)), 15), right,
           font=SANS_B(10), fill=GREY)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=SERIF_B(46))) / 2, 30), title,
           font=SERIF_B(46), fill=INK)
    date = "WEDNESDAY 25 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=SANS_B(21))) / 2, 82), date,
           font=SANS_B(21), fill=RED)
    d.line([(MX, 108), (W - MX, 108)], fill=INK, width=3)
    d.line([(MX, 112), (W - MX, 112)], fill=INK, width=1)

    # ---- numbers strip
    d.rectangle([MX, 118, W - MX, 146], fill=INK)
    slot = (W - 2 * MX) / len(NUMBERS)
    for i, (label, value) in enumerate(NUMBERS):
        cx = MX + slot * i + slot / 2
        lw = d.textlength(label, font=SANS_B(8))
        d.text((cx - lw / 2, 121), label, font=SANS_B(8), fill=(170, 170, 165))
        vw = d.textlength(value, font=SANS_B(12))
        d.text((cx - vw / 2, 132), value, font=SANS_B(12), fill=(255, 255, 255))

    # ---- three leads
    COLW = (W - 2 * MX - 2 * 12) // 3
    for i, lead in enumerate(LEADS):
        x = MX + i * (COLW + 12)
        d.text((x, 154), lead["kicker"], font=SANS_B(10), fill=RED)
        hl = fit_lines(d, lead["headline"], SERIF_B(17), COLW, 2)
        yy = 168
        for line in hl:
            d.text((x, yy), line, font=SERIF_B(17), fill=INK)
            yy += 21
        img.paste(lead["pic"](COLW, 84), (x, 212))
        body = fit_lines(d, lead["body"], SANS(10), COLW, 4)
        yy = 300
        for line in body:
            d.text((x, yy), line, font=SANS(10), fill=INK)
            yy += 13
        cw = chip(d, x, 350, lead["tag"], lead["tagfill"])
        d.text((x + cw + 6, 351), "Source: " + lead["source"],
               font=SANS(9), fill=GREY)
    d.line([(MX, 364), (W - MX, 364)], fill=INK, width=1)

    # ---- the day in pictures
    d.text((MX, 370), "THE DAY IN PICTURES", font=SERIF_B(16), fill=INK)
    note = "Every picture shows its own story"
    d.text((W - MX - d.textlength(note, font=SANS(9)), 374), note,
           font=SANS(9), fill=GREY)
    CW = (W - 2 * MX - 4 * 10) // 5
    CH = 148
    for i, (kicker, headline, tag, tagfill, source, picfn) in enumerate(CARDS):
        col, row = i % 5, i // 5
        x = MX + col * (CW + 10)
        y = 390 + row * (CH + 8)
        img.paste(picfn(CW - 2, 74), (x + 1, y + 1))
        d.text((x, y + 78), kicker, font=SANS_B(8), fill=RED)
        hl = fit_lines(d, headline, SANS_B(10), CW, 3)
        yy = y + 89
        for line in hl:
            d.text((x, yy), line, font=SANS_B(10), fill=INK)
            yy += 12
        cw = chip(d, x, y + 130, tag, tagfill)
        d.text((x + cw + 5, y + 131), source, font=SANS(8), fill=GREY)

    # ---- the day in UTC
    d.line([(MX, 700), (W - MX, 700)], fill=INK, width=1)
    d.text((MX, 706), "THE DAY IN UTC", font=SERIF_B(14), fill=INK)
    for i, (t, text) in enumerate(TIMELINE):
        col, row = i % 3, i // 3
        x = MX + col * 336
        y = 724 + row * 12
        d.text((x, y), t, font=MONO_B(10), fill=RED)
        d.text((x + 38, y), text, font=SANS(9), fill=INK)

    # ---- map (21 Nov style: tall dense dotted land grid, numbered pins)
    d.line([(MX, 764), (W - MX, 764)], fill=INK, width=1)
    d.text((MX, 770), "WHERE THE NEWS HAPPENED", font=SERIF_B(14), fill=INK)
    d.text((MX, 786), "Pins mark the pictured stories", font=SANS(9), fill=GREY)
    MAPX, MAPY, MAPW, MAPH = 24, 800, 360, 168

    def lonlat_to_xy(lon, lat):
        return (MAPX + (lon + 180) / 360 * MAPW,
                MAPY + (80 - lat) / 135 * MAPH)

    for r, c0, c1 in LAND:
        for c in range(c0, c1 + 1):
            cx = MAPX + c * (MAPW / 64) + 2
            cy = MAPY + r * (MAPH / 26) + 3
            d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=NAVY)
    for num, lon, lat, dx, dy in PINS:
        px, py = lonlat_to_xy(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=INK)
        qx, qy = px + dx, py + dy
        if dx or dy:
            d.line([(px, py), (qx, qy)], fill=GREY, width=1)
        d.ellipse([qx - 7, qy - 7, qx + 7, qy + 7], fill=RED, outline=(255, 255, 255), width=1)
        num_s = str(num)
        nw = d.textlength(num_s, font=SANS_B(9))
        d.text((qx - nw / 2, qy - 6), num_s, font=SANS_B(9), fill=(255, 255, 255))

    # ---- also on
    d.text((408, 770), "ALSO ON", font=SERIF_B(14), fill=INK)
    cols = [ALSO_ON[:11], ALSO_ON[11:]]
    for ci, col_items in enumerate(cols):
        x = 408 + ci * (292 + 16)
        y = 788
        for region, text in col_items:
            lab = region + "  "
            lw = d.textlength(lab, font=SANS_B(8))
            lines = wrap(d, text, SANS(9), 292 - lw)
            lines = lines[:2]
            d.text((x, y), lab, font=SANS_B(8), fill=RED)
            yy = y
            for ln in lines:
                d.text((x + lw, yy), ln, font=SANS(9), fill=INK)
                yy += 11
            y = yy + 4

    # ---- date check box (exactly two lines inside)
    d.rectangle([16, 972, 1008, 1006], outline=RED, width=2)
    head = "DATE CHECK \u2014 NOT TODAY'S NEWS:  "
    hw = d.textlength(head, font=SANS_B(9))
    d.text((22, 975), head, font=SANS_B(9), fill=RED)
    l1 = "Four tankers hit mines in Hormuz (Mon 24 Nov) \u2022 Asia surges on Nvidia return (Mon 24 Nov) \u2022 Hamas chief Abu Nahel killed (Mon 24 Nov)"
    l2 = "Zaporizhzhia strike kills 2 (Mon 24 Nov) \u2022 350+ drones at Moscow (Mon 24 Nov) \u2022 Hanoi blast kills six (Mon 24 Nov) \u2022 Haftar in Ankara (Mon 24 Nov)"
    d.text((22 + hw, 975), l1, font=SANS(8), fill=INK)
    d.text((22, 989), l2, font=SANS(8), fill=INK)

    # ---- footer
    d.text((MX, 1012),
           "SOURCES: Reuters, AP, Gulf News, OilPrice, Japan Times, WSJ, Dell, SEC filing, ABC News, The Statesman",
           font=SANS(8), fill=GREY)
    return img


def main():
    img = draw_page()
    img.save("entry.png", format="PNG", optimize=False)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
