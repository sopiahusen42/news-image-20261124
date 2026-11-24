#!/usr/bin/env python3
"""Local generator for entry.png -- 24 November 2026 world news in one image.

Build-time only. Needs PIL, which exists on the authoring machine but is NOT
available to the grader; main.py ships the finished PNG instead.
Deterministic: no randomness, no clock reads, fixed strings only.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = "#F7F1E6"
INK = "#141414"
RED = "#B3202C"
SLATE = "#3C4753"
TEAL = "#1F6F6B"
OCHRE = "#B07A28"
HAIR = "#D9CFBE"
NIGHT = "#1B2430"
CREAM = "#F6F1E7"

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    f = _cache.get(key)
    if f is None:
        f = ImageFont.truetype(path, size)
        _cache[key] = f
    return f


def fit_one(d, text, path, start, floor, max_w):
    size = start
    while size > floor:
        if d.textlength(text, font=F(path, size)) <= max_w:
            return F(path, size)
        size -= 1
    return F(path, floor)


def wrap_fit(d, text, path, start, floor, max_w, max_lines):
    words = text.split()
    size = start
    while True:
        f = F(path, size)
        lines, cur = [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if not cur or d.textlength(t, font=f) <= max_w:
                cur = t
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        if (len(lines) <= max_lines and all(d.textlength(l, font=f) <= max_w for l in lines)) or size <= floor:
            return f, lines
        size -= 1


def star5(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.42
        a = i * math.pi / 5 - math.pi / 2
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


# --------------------------------------------------------------- pictures
# Every picture is drawn in a 0..100 unit square mapped onto its box, so the
# same code works at any panel size.

class Box:
    def __init__(self, b):
        self.x, self.y = b[0], b[1]
        self.s = min(b[2] - b[0], b[3] - b[1]) / 100.0

    def p(self, x, y):
        return (self.x + x * self.s, self.y + y * self.s)

    def r(self, x, y, w, h):
        return [self.x + x * self.s, self.y + y * self.s,
                self.x + (x + w) * self.s, self.y + (y + h) * self.s]

    def line(self, pts, fill, width):
        return [(self.x + x * self.s, self.y + y * self.s) for x, y in pts]


def pic_ukraine(d, b):
    u = Box(b)
    d.rectangle(b, fill=NIGHT)
    # night skyline
    for bx, bw, bh in [(0, 18, 26), (16, 15, 42), (30, 20, 33), (49, 16, 52), (64, 18, 30),
                       (81, 15, 39), (95, 6, 24)]:
        d.rectangle(u.r(bx, 100 - bh, bw, bh), fill="#080C12")
        for wy in range(int(100 - bh) + 4, 96, 9):
            for wx in range(bx + 3, bx + bw - 4, 8):
                d.rectangle(u.r(wx, wy, 3, 4), fill=OCHRE)
    # missile trail
    d.line(u.line([(2, 4), (20, 20), (38, 32)], 0, 0), fill="#8E99A5", width=5)
    d.line(u.line([(2, 4), (20, 20), (38, 32)], 0, 0), fill=CREAM, width=2)
    # burst
    cx, cy = u.p(70, 30)
    for i in range(8):
        a = i * math.pi / 4 + 0.35
        d.line([(cx + 9 * u.s * math.cos(a), cy + 9 * u.s * math.sin(a)),
                (cx + 26 * u.s * math.cos(a), cy + 26 * u.s * math.sin(a))], fill=OCHRE, width=4)
    for pct, col in [(22, RED), (14, OCHRE), (6, CREAM)]:
        d.ellipse([cx - pct * u.s, cy - pct * u.s, cx + pct * u.s, cy + pct * u.s], fill=col)
    # fire glow at the base
    d.polygon([u.p(40, 100), u.p(60, 100), u.p(50, 78)], fill=RED)


def pic_nato(d, b):
    u = Box(b)
    d.rectangle(b, fill="#DBE8EC")
    d.polygon([u.p(14, 58), u.p(40, 50), u.p(68, 56), u.p(84, 76), u.p(80, 96),
               u.p(56, 104), u.p(28, 100), u.p(12, 82)],
              fill="#C4DED9", outline=TEAL, width=3)
    d.line(u.line([(24, 74), (34, 84)], 0, 0), fill=TEAL, width=2)
    for mx, my in [(30, 76), (48, 68), (64, 88)]:
        d.polygon([u.p(mx, my - 5), u.p(mx + 5, my + 4), u.p(mx - 5, my + 4)], fill=RED)
    cx, cy = u.p(40, 22)
    for r in (16, 26, 36):
        d.arc([cx - r * u.s, cy - r * u.s, cx + r * u.s, cy + r * u.s], 200, 340, fill=RED, width=2)
    # AWACS aircraft
    d.polygon([u.p(58, 16), u.p(96, 16), u.p(100, 23), u.p(58, 23)], fill=SLATE)
    d.polygon([u.p(84, 16), u.p(91, 3), u.p(96, 4), u.p(92, 16)], fill=SLATE)
    d.polygon([u.p(72, 16), u.p(66, 6), u.p(61, 7), u.p(66, 16)], fill=SLATE)
    d.ellipse(u.r(68, 2, 24, 8), fill="#8492A0")
    d.line(u.line([(58, 20), (52, 20)], 0, 0), fill=SLATE, width=2)


def pic_libya(d, b):
    u = Box(b)
    d.rectangle(b, fill="#DAE7E3")
    d.rectangle(u.r(0, 62, 100, 38), fill="#7FB3AD")
    d.rectangle(u.r(0, 82, 100, 18), fill=TEAL)
    for wx in range(4, 96, 14):
        d.line(u.line([(wx, 72), (wx + 7, 72)], 0, 0), fill=CREAM, width=3)
    # listing corvette
    d.polygon([u.p(8, 54), u.p(74, 38), u.p(81, 56), u.p(15, 72)], fill=SLATE)
    d.polygon([u.p(28, 48), u.p(46, 41), u.p(49, 52), u.p(31, 59)], fill="#6E7C89")
    d.line(u.line([(38, 42), (38, 22)], 0, 0), fill=INK, width=3)
    d.line(u.line([(38, 22), (52, 26)], 0, 0), fill=INK, width=3)
    for sx, sy, r in [(45, 16, 7), (58, 9, 9), (70, 6, 6)]:
        d.ellipse(u.r(sx - r, sy - r, 2 * r, 2 * r), fill="#AEB6BD")
    # drone overhead
    d.rectangle(u.r(64, 26, 12, 6), fill=INK)
    d.line(u.line([(62, 28), (52, 21)], 0, 0), fill=INK, width=2)
    d.line(u.line([(78, 28), (86, 20)], 0, 0), fill=INK, width=2)
    d.ellipse(u.r(48, 17, 7, 6), fill=INK)
    d.ellipse(u.r(83, 15, 7, 6), fill=INK)
    d.line(u.line([(70, 32), (66, 42)], 0, 0), fill=RED, width=2)
    d.polygon([u.p(2, 80), u.p(12, 60), u.p(21, 82)], fill=CREAM)


def pic_us(d, b):
    u = Box(b)
    d.rectangle(b, fill="#EFE6D3")
    d.line(u.line([(86, 88), (86, 18)], 0, 0), fill=RED, width=8)
    d.polygon([u.p(86, 4), u.p(76, 22), u.p(96, 22)], fill=RED)
    cx, cy, s = u.p(40, 52), None, 24
    cxx, cyy = cx
    d.rectangle([cxx - s * u.s, cyy - s * u.s, cxx + s * u.s, cyy + s * u.s], fill=SLATE)
    d.rectangle([cxx - (s - 6) * u.s, cyy - (s - 6) * u.s,
                 cxx + (s - 6) * u.s, cyy + (s - 6) * u.s], fill=TEAL)
    d.rectangle([cxx - 9 * u.s, cyy - 9 * u.s, cxx + 9 * u.s, cyy + 9 * u.s], fill="#0D2827")
    for i in range(3):
        off = -14 + i * 14
        d.rectangle([cxx + (off - 3) * u.s, cyy - (s + 7) * u.s,
                     cxx + (off + 3) * u.s, cyy - s * u.s], fill=OCHRE)
        d.rectangle([cxx + (off - 3) * u.s, cyy + s * u.s,
                     cxx + (off + 3) * u.s, cyy + (s + 7) * u.s], fill=OCHRE)
        d.rectangle([cxx - (s + 7) * u.s, cyy + (off - 3) * u.s,
                     cxx - s * u.s, cyy + (off + 3) * u.s], fill=OCHRE)
        d.rectangle([cxx + s * u.s, cyy + (off - 3) * u.s,
                     cxx + (s + 7) * u.s, cyy + (off + 3) * u.s], fill=OCHRE)
    d.line(u.line([(2, 34), (14, 34)], 0, 0), fill=TEAL, width=3)
    d.line(u.line([(2, 72), (14, 72)], 0, 0), fill=TEAL, width=3)


def pic_mideast(d, b):
    u = Box(b)
    d.rectangle(b, fill="#F0E3D0")
    d.rectangle(u.r(0, 86, 100, 14), fill=SLATE)
    # closed door
    d.rectangle(u.r(56, 6, 36, 80), fill=SLATE)
    d.rectangle(u.r(62, 12, 24, 68), fill="#59666F")
    d.ellipse(u.r(82, 62, 5, 5), fill=OCHRE)
    # plank nailed across the door
    d.polygon([u.p(52, 48), u.p(96, 32), u.p(96, 42), u.p(52, 58)], fill=RED)
    d.rectangle(u.r(70, 42, 5, 8), fill=INK)
    # empty chair
    d.rectangle(u.r(10, 58, 22, 6), fill=OCHRE)
    d.rectangle(u.r(10, 38, 5, 24), fill=OCHRE)
    d.line(u.line([(14, 64), (14, 86)], 0, 0), fill=INK, width=3)
    d.line(u.line([(29, 64), (29, 86)], 0, 0), fill=INK, width=3)


def pic_asia(d, b):
    u = Box(b)
    d.rectangle(b, fill="#E4E9F0")
    d.line(u.line([(18, 92), (18, 4)], 0, 0), fill=SLATE, width=4)
    for gy in range(8, 88, 11):
        d.line(u.line([(18, gy), (31, gy + 6)], 0, 0), fill=SLATE, width=2)
    # rocket
    d.polygon([u.p(36, 20), u.p(44, 2), u.p(52, 20)], fill=RED)
    d.rectangle(u.r(36, 20, 16, 54), fill=CREAM, outline=SLATE, width=2)
    d.rectangle(u.r(36, 40, 16, 8), fill=RED)
    d.polygon([u.p(36, 62), u.p(26, 80), u.p(36, 80)], fill=SLATE)
    d.polygon([u.p(52, 62), u.p(62, 80), u.p(52, 80)], fill=SLATE)
    d.polygon([u.p(40, 74), u.p(48, 74), u.p(44, 94)], fill=OCHRE)
    # space station
    d.rectangle(u.r(64, 10, 20, 11), fill=CREAM, outline=SLATE, width=2)
    d.rectangle(u.r(52, 13, 12, 5), fill=TEAL)
    d.rectangle(u.r(84, 13, 9, 5), fill=TEAL)
    d.rectangle(u.r(68, 3, 11, 7), fill=TEAL)
    # pakistan flag
    d.rectangle(u.r(58, 56, 34, 22), fill="#0B5A33")
    d.rectangle(u.r(58, 56, 6, 22), fill=CREAM)
    d.ellipse(u.r(66, 60, 15, 13), fill=CREAM)
    d.ellipse(u.r(71, 61, 14, 12), fill="#0B5A33")
    star5(d, (u.p(78, 65))[0], (u.p(78, 65))[1], 4 * u.s, CREAM)


STORIES = [
    ("UKRAINE", "RUSSIAN STRIKE KILLS TWO", "48 wounded, four children", pic_ukraine),
    ("NATO", "AWACS JETS SENT TO POLAND", "Three Kh-101s fell in Poland", pic_nato),
    ("LIBYA", "WARSHIP SUNK AT BENGHAZI", "Kyiv drone hits a corvette", pic_libya),
    ("UNITED STATES", "NVIDIA REINSTATES FOUNDER", "Huang back; shares up 31%", pic_us),
    ("MIDDLE EAST", "IRAN SHUTS DOOR ON TALKS", "Seven conditions for talks", pic_mideast),
    ("ASIA", "SHENZHOU-24 CREW NAMED", "First foreign visitor aboard", pic_asia),
]


def draw_masthead(d):
    d.rectangle([0, 0, W, 8], fill=RED)
    ft = F(SANS_B, 26)
    d.text((24, 14), "TUESDAY", font=ft, fill=RED)
    tw = d.textlength("TUESDAY", font=ft)
    d.line([(24 + tw + 18, 32), (540, 32)], fill=RED, width=2)
    d.text((560, 16), "WORLD NEWS IN ONE IMAGE", font=F(SANS_B, 23), fill=SLATE)
    gx, gy, gr = 976, 30, 22
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=TEAL, width=3)
    d.ellipse([gx - gr + 8, gy - gr, gx + gr - 8, gy + gr], outline=TEAL, width=2)
    d.line([(gx - gr, gy), (gx + gr, gy)], fill=TEAL, width=2)
    d.arc([gx - gr, gy - 11, gx + gr, gy + 11], 0, 180, fill=TEAL, width=2)
    fdate = fit_one(d, "24 NOVEMBER 2026", SERIF_B, 94, 78, 980)
    d.text((18, 46), "24 NOVEMBER 2026", font=fdate, fill=INK)
    d.rectangle([0, 164, W, 171], fill=INK)
    return fdate


def draw_panel(d, box, kicker, headline, detail, picture_fn):
    """Draw one story panel: kicker, wrapped headline, picture, one caption.

    box is (left, top, width, height). Headline and caption are measured and
    shrunk so they never leave the panel.
    """
    px, py, pw, ph = box
    d.text((px, py), kicker, font=F(SANS_B, 25), fill=RED)
    fh, lines = wrap_fit(d, headline, SERIF_B, 42, 34, pw, 2)
    ty = py + 24
    for ln in lines:
        d.text((px, ty), ln, font=fh, fill=INK)
        ty += int(fh.size * 1.02)
    pic = (px, py + 110, px + 98, py + 110 + 96)
    picture_fn(d, pic)
    d.rectangle([pic[0] - 1, pic[1] - 1, pic[2] + 1, pic[3] + 1], outline=INK, width=2)
    fd = fit_one(d, detail, SANS, 26, 24, pw - 108)
    d.text((px + 108, py + 146), detail, font=fd, fill=SLATE)
    return fh.size, fd.size


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    draw_masthead(d)

    cols, rows, PW, PH = [22, 526], [176, 392, 608], 476, 208
    for i, (kick, head, det, fn) in enumerate(STORIES):
        px, py = cols[i % 2], rows[i // 2]
        hs, ds = draw_panel(d, (px, py, PW, PH), kick, head, det, fn)
        print("panel", i, kick, "head", hs, "detail", ds)

    d.line([(22, 386), (1002, 386)], fill=HAIR, width=2)
    d.line([(22, 602), (1002, 602)], fill=HAIR, width=2)
    d.line([(512, 176), (512, 816)], fill=HAIR, width=2)

    # also today
    d.line([(22, 826), (1002, 826)], fill=RED, width=3)
    d.text((22, 832), "ALSO TODAY", font=F(SANS_B, 25), fill=RED)
    items = [
        "EU seeks changes to UN climate talks after COP31 failed",
        "Hanoi hot pot restaurant blast kills six",
        "Bangladesh: Hasina says she will return on 16 December",
        "Record quasar found 630m years after the Big Bang",
    ]
    for j, item in enumerate(items):
        oy = 848 + j * 22
        d.rectangle([22, oy + 8, 30, oy + 16], fill=RED)
        d.text((40, oy), item, font=fit_one(d, item, SANS, 25, 24, 950), fill=INK)

    ff = F(SANS, 24)
    fy = 946
    for line in [
        "Wire compiled 15:50 UTC, Tuesday 24 November 2026 - events of",
        "24 November, any time zone.",
        "Built by an AI agent for make.fun. Sources: Reuters, AP, AFP, FT, WPXI.",
    ]:
        d.text((22, fy), line, font=ff, fill=SLATE)
        fy += 24

    return img


def main():
    img = render()
    assert img.size == (1024, 1024) and img.mode == "RGB"
    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size, img.mode)


if __name__ == "__main__":
    main()
