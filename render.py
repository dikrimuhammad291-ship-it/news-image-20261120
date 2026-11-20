#!/usr/bin/env python3
"""Draw the Friday 20 November 2026 world-news front page, 1024x1024 PNG.

Run from the repository root:  python3 render.py
Writes entry.png next to this file. Every illustration is original vector
art drawn with PIL primitives; no photographs or copied artwork.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 26

PAPER = (250, 246, 238)     # newsprint off-white
CARD = (255, 253, 248)      # card fill
INK = (24, 24, 24)          # near-black ink
GREY = (110, 106, 96)       # muted grey
RULE = (196, 188, 168)      # hairline rule
RED = (176, 32, 32)         # accent red
NAVY = (30, 58, 95)         # accent navy
GOLD = (184, 138, 44)       # accent gold
NIGHT = (18, 28, 52)        # night sky
NIGHT2 = (28, 42, 74)       # night sky, lower band
FLAME = (244, 130, 32)      # explosion orange
EMBER = (232, 72, 32)       # explosion red-orange

FD = "/usr/share/fonts/truetype/dejavu"


def serif_bold(size):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSerif-Bold.ttf"), size)


def serif(size):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSerif.ttf"), size)


def sans_bold(size):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSans-Bold.ttf"), size)


def sans(size):
    return ImageFont.truetype(os.path.join(FD, "DejaVuSans.ttf"), size)


def fit_lines(d, text, font, width):
    """Wrap text to lines that fit width, measured with the font."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def put_lines(d, x, y, lines, font, fill, gap=5):
    """Draw stacked lines; return y just below the last one."""
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += font.size + gap
    return y


def frame(d, x0, y0, x1, y1, fill=CARD, outline=RULE, width=2):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=width)


def tag(d, x, y, text, color=RED, size=16):
    """Small caps kicker line; returns y below it."""
    d.text((x, y), text, font=sans_bold(size), fill=color)
    return y + size + 7


def starburst(d, cx, cy, r, color):
    """Explosion burst: radiating triangles around a core."""
    import math
    for i in range(10):
        a = math.radians(i * 36)
        a2 = math.radians(i * 36 + 18)
        x1 = cx + int(r * math.cos(a))
        y1 = cy + int(r * math.sin(a))
        x2 = cx + int(r * 0.45 * math.cos(a2))
        y2 = cy + int(r * 0.45 * math.sin(a2))
        x3 = cx + int(r * math.cos(math.radians(i * 36 + 36)))
        y3 = cy + int(r * math.sin(math.radians(i * 36 + 36)))
        d.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=color)
    d.ellipse([cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32],
              fill=(255, 214, 120))


def draw_kyiv(d, x0, y0, x1, y1):
    """Night attack over Kyiv: skyline, broken bridge, missile trails."""
    d.rectangle([x0, y0, x1, y1], fill=NIGHT)
    d.rectangle([x0, y0 + (y1 - y0) // 2, x1, y1], fill=NIGHT2)
    # stars
    for sx, sy in ((x0 + 22, y0 + 16), (x0 + 90, y0 + 30), (x0 + 150, y0 + 12),
                   (x0 + 210, y0 + 26), (x0 + 260, y0 + 14), (x0 + 300, y0 + 34),
                   (x0 + 55, y0 + 48), (x0 + 180, y0 + 52)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(220, 226, 240))
    # missile trails arcing down
    for (mx0, my0, mx1, my1) in ((x0 + 40, y0 + 8, x0 + 120, y0 + 84),
                                (x0 + 170, y0 + 4, x0 + 240, y0 + 78),
                                (x0 + 285, y0 + 10, x0 + 310, y0 + 70)):
        d.line([mx0, my0, mx1, my1], fill=(255, 200, 110), width=3)
        d.ellipse([mx1 - 4, my1 - 4, mx1 + 4, my1 + 4], fill=(255, 240, 200))
    # city skyline
    base = y0 + int((y1 - y0) * 0.66)
    heights = [46, 70, 54, 88, 62, 78, 50, 66, 58]
    bw = (x1 - x0) // len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + i * bw + 3
        d.rectangle([bx, base - hh, bx + bw - 6, base], fill=(10, 16, 32))
        for wy in range(base - hh + 8, base - 6, 14):
            d.rectangle([bx + 5, wy, bx + 9, wy + 5], fill=(255, 214, 120))
    # river
    d.rectangle([x0, base, x1, y1], fill=(16, 44, 78))
    # bridge with a broken middle span
    deck = base - 6
    mid = (x0 + x1) // 2
    d.rectangle([x0 + 10, deck - 8, mid - 30, deck], fill=(120, 122, 128))
    d.rectangle([mid + 30, deck - 8, x1 - 10, deck], fill=(120, 122, 128))
    for px in (x0 + 46, x1 - 58):
        d.rectangle([px, deck - 34, px + 12, deck], fill=(120, 122, 128))
    # fallen span tilting into the water
    d.polygon([(mid - 34, deck + 8), (mid + 26, deck + 26),
               (mid + 18, deck + 38), (mid - 40, deck + 20)],
              fill=(120, 122, 128))
    # bursts at the break and on the skyline
    starburst(d, mid, deck - 18, 20, FLAME)
    starburst(d, x0 + 120, base - 92, 14, EMBER)
    d.rectangle([x0, y0, x1, y1], outline=RULE, width=2)


def draw_chart(d, x0, y0, x1, y1):
    """Falling market chart with a red plunge line."""
    d.rectangle([x0, y0, x1, y1], fill=(242, 240, 234))
    # grid lines
    for gy in range(y0 + 18, y1 - 8, 22):
        d.line([x0 + 10, gy, x1 - 10, gy], fill=(222, 216, 200), width=1)
    pts = []
    n = 9
    vals = [0.16, 0.24, 0.20, 0.36, 0.44, 0.58, 0.52, 0.72, 0.86]
    for i, v in enumerate(vals):
        px = x0 + 16 + int(i * (x1 - x0 - 32) / (n - 1))
        py = y0 + 14 + int(v * (y1 - y0 - 34))
        pts.append((px, py))
    d.line(pts, fill=RED, width=5, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    # down arrow at the end
    ex, ey = pts[-1]
    d.polygon([(ex, ey + 14), (ex - 9, ey + 2), (ex + 9, ey + 2)], fill=RED)
    d.rectangle([x0, y0, x1, y1], outline=RULE, width=2)


def draw_tower(d, x0, y0, x1, y1):
    """Riyadh tower struck, with a tanker burning below. All art is kept
    inside the box by scaling every height to the box height."""
    h = y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(238, 226, 205))
    horizon = y0 + int(h * 0.62)
    # low skyline, heights as fractions of the box so nothing pokes out
    for bx, bw, bf in ((12, 34, 0.28), (52, 26, 0.38), (84, 30, 0.22),
                       (210, 30, 0.32), (246, 26, 0.26), (278, 34, 0.36)):
        bh = int(h * bf)
        d.rectangle([x0 + bx, horizon - bh, x0 + bx + bw, horizon],
                    fill=(150, 138, 110))
    # tall tower with a twist top
    tx = x0 + 128
    top = y0 + int(h * 0.12)
    d.rectangle([tx, top, tx + 66, horizon], fill=(96, 88, 72))
    d.polygon([(tx, top), (tx + 66, top), (tx + 48, y0 + 2),
               (tx + 18, y0 + 2)], fill=(96, 88, 72))
    wy = top + 6
    while wy < horizon - 4:
        d.line([tx + 6, wy, tx + 60, wy], fill=(238, 226, 205), width=2)
        wy += 10
    starburst(d, tx + 62, top + int(h * 0.18), 14, FLAME)
    # sea and tanker
    d.rectangle([x0, horizon, x1, y1], fill=(38, 92, 140))
    d.rectangle([x0 + 30, horizon + 8, x0 + 210, horizon + 20],
                fill=(40, 40, 40))
    d.rectangle([x0 + 170, horizon + 1, x0 + 204, horizon + 8],
                fill=(200, 200, 200))
    starburst(d, x0 + 90, horizon + 6, 12, EMBER)
    d.rectangle([x0, y0, x1, y1], outline=RULE, width=2)


def draw_stars(d, x0, y0, x1, y1):
    """Circle of gold stars on navy — a Europe motif."""
    d.rectangle([x0, y0, x1, y1], fill=NAVY)
    import math
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 14
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + int(r * math.cos(a)), cy + int(r * math.sin(a))
        starburst(d, sx, sy, 7, GOLD)
    d.rectangle([x0, y0, x1, y1], outline=RULE, width=2)


def draw_ball(d, x0, y0, x1, y1):
    """A baseball on a green diamond — a sports motif."""
    d.rectangle([x0, y0, x1, y1], fill=(64, 120, 72))
    d.polygon([( (x0 + x1) // 2, y1 - 12), (x1 - 14, (y0 + y1) // 2),
               ((x0 + x1) // 2, y0 + 12), (x0 + 14, (y0 + y1) // 2)],
              outline=(240, 236, 220), width=3)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(250, 248, 240),
              outline=RED, width=2)
    d.arc([cx - 20, cy - 26, cx + 6, cy + 26], 300, 60, fill=RED, width=2)
    d.arc([cx - 6, cy - 26, cx + 20, cy + 26], 120, 240, fill=RED, width=2)
    d.rectangle([x0, y0, x1, y1], outline=RULE, width=2)


def draw_forest(d, x0, y0, x1, y1):
    """Amazon canopy under sun — a Brazil motif. Tree heights are scaled
    to the box so no canopy pokes above the panel."""
    h = y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(206, 226, 196))
    d.ellipse([x1 - 40, y0 + 6, x1 - 14, y0 + 32], fill=(255, 214, 120))
    base = y1 - 6
    for tx, tf in ((14, 0.55), (44, 0.78), (76, 0.62),
                   (108, 0.85), (140, 0.58), (170, 0.75),
                   (200, 0.60), (230, 0.80)):
        th = int(h * tf)
        d.rectangle([x0 + tx + 8, base - th // 3, x0 + tx + 14, base],
                    fill=(120, 84, 48))
        d.ellipse([x0 + tx - 6, base - th, x0 + tx + 28,
                   base - th // 3 + 6], fill=(46, 110, 58))
    d.rectangle([x0, y0, x1, y1], outline=RULE, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    title = "THE WORLD TODAY"
    tf = serif_bold(62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 18), title, font=tf, fill=INK)
    d.line([MARGIN, 96, W - MARGIN, 96], fill=INK, width=3)
    d.line([MARGIN, 101, W - MARGIN, 101], fill=INK, width=1)
    date = "FRIDAY, 20 NOVEMBER 2026"
    d.text((MARGIN, 110), date, font=sans_bold(20), fill=RED)
    right = "ONE DAY  \u2022  ONE PAGE  \u2022  THE WORLD'S NEWS"
    rw = d.textlength(right, font=sans(16))
    d.text((W - MARGIN - rw, 112), right, font=sans(16), fill=GREY)
    d.line([MARGIN, 140, W - MARGIN, 140], fill=RULE, width=1)

    # ---- Lead story: Ukraine ----
    lx0, ly0, lx1, ly1 = MARGIN, 152, W - MARGIN, 420
    frame(d, lx0, ly0, lx1, ly1)
    ax0, ay0, ax1, ay1 = lx1 - 348, ly0 + 14, lx1 - 14, ly0 + 196
    draw_kyiv(d, ax0, ay0, ax1, ay1)
    tx = lx0 + 16
    y = tag(d, tx, ly0 + 14, "WAR IN UKRAINE  \u2022  KYIV")
    head = "Russia's biggest strike in months hits Kyiv"
    hf = serif_bold(37)
    y = put_lines(d, tx, y, fit_lines(d, head, hf, ax0 - tx - 16), hf, INK, gap=2)
    deck = ("More than 100 missiles and 400 drones rain down overnight, hours "
            "after the Shenzhen summit \u2014 killing 8, wounding 28, smashing "
            "three bridges and cutting power across Ukraine.")
    df = sans(17)
    y = put_lines(d, tx, y + 6, fit_lines(d, deck, df, ax0 - tx - 16), df, INK)
    # stat strip under the art + text, two lines so nothing collides
    sy = ly1 - 48
    d.line([lx0 + 16, sy - 8, lx1 - 16, sy - 8], fill=RULE, width=1)
    stats = "100+ MISSILES  \u2022  400 DRONES  \u2022  3 BRIDGES HIT  \u2022  8 KILLED, 28 HURT"
    d.text((lx0 + 16, sy), stats, font=sans_bold(16), fill=NAVY)
    note = "UK pledges 1,000+ drones in a \u00a3260m package  \u2022  Poland lifts air-threat warning"
    d.text((lx0 + 16, sy + 22), note, font=sans(14), fill=GREY)

    # ---- Row 2: two half panels ----
    ry0, ry1 = 432, 652
    mid = (W - 12) // 2
    # Markets
    frame(d, MARGIN, ry0, mid, ry1)
    y = tag(d, MARGIN + 14, ry0 + 12, "MARKETS  \u2022  ASIA")
    y = put_lines(d, MARGIN + 14, y,
                  fit_lines(d, "Asian markets plunge on AI-bubble fears",
                            serif_bold(24), mid - MARGIN - 28),
                  serif_bold(24), INK, gap=1)
    draw_chart(d, MARGIN + 14, y + 6, mid - 14, y + 66)
    body = ("Nikkei \u22124.8%, Kospi \u22125.7%, Taiwan \u22126.8%: shares head "
            "for their worst week since 2020 as Anthropic's record IPO fails "
            "to calm the AI trade.")
    put_lines(d, MARGIN + 14, y + 74,
              fit_lines(d, body, sans(14), mid - MARGIN - 28), sans(14), INK)
    # Middle East
    frame(d, mid + 12, ry0, W - MARGIN, ry1)
    y = tag(d, mid + 26, ry0 + 12, "MIDDLE EAST  \u2022  RIYADH / HORMUZ")
    y = put_lines(d, mid + 26, y,
                  fit_lines(d, "Houthi missiles hit Riyadh tower; tanker burns",
                            serif_bold(24), W - MARGIN - mid - 40),
                  serif_bold(24), INK, gap=1)
    draw_tower(d, mid + 26, y + 6, W - MARGIN - 14, y + 66)
    body = ("Missiles damage the sovereign wealth fund tower in Riyadh; a "
            "tanker catches fire after hitting a mine near the Strait of "
            "Hormuz. Pentagon puts the US\u2013Iran war cost at $48.3bn.")
    put_lines(d, mid + 26, y + 74,
              fit_lines(d, body, sans(14), W - MARGIN - mid - 40), sans(14), INK)

    # ---- Row 3: three cards ----
    cy0, cy1 = 664, 852
    cw = (W - 2 * MARGIN - 24) // 3
    cards = [
        ("EUROPE  \u2022  LONDON", "UK and EU set to agree youth mobility scheme",
         "A deal is expected at Friday's summit \u2014 as young Europeans "
         "protest in 25+ countries over living costs.", draw_stars),
        ("UNITED STATES", "Trump pardons baseball legend Pete Rose",
         "A posthumous pardon for the late star, banned from the game for "
         "betting.", draw_ball),
        ("BRAZIL  \u2022  MATO GROSSO", "Brazil recognises Raoni's ancestral land",
         "President Lula visits the 94-year-old Kayapo leader and recognises "
         "Kayapo and Yudja ancestral lands.", draw_forest),
    ]
    for i, (kick, head, body, art) in enumerate(cards):
        cx0 = MARGIN + i * (cw + 12)
        cx1 = cx0 + cw
        frame(d, cx0, cy0, cx1, cy1)
        y = tag(d, cx0 + 12, cy0 + 10, kick, size=14)
        y = put_lines(d, cx0 + 12, y,
                      fit_lines(d, head, serif_bold(20), cw - 24),
                      serif_bold(20), INK, gap=1)
        art(d, cx0 + 12, y + 4, cx1 - 12, y + 50)
        put_lines(d, cx0 + 12, y + 58,
                  fit_lines(d, body, sans(14), cw - 24), sans(14), INK)

    # ---- In brief ----
    by0, by1 = 864, 962
    frame(d, MARGIN, by0, W - MARGIN, by1)
    d.text((MARGIN + 14, by0 + 10), "IN BRIEF", font=sans_bold(16), fill=RED)
    briefs = [
        "COP31: Africa seeks tripled climate finance.",
        "Senegal: boat capsizing kills four.",
        "Georgia: six dead in a gas explosion.",
        "Italy: Genoa airport halts flights after drones.",
        "Zimbabwe: 250,000 landmines destroyed.",
        "US sanctions Comancheros and 'Ndrangheta.",
    ]
    col_w = (W - 2 * MARGIN - 28 - 24) // 2
    for i, item in enumerate(briefs):
        col = i // 3
        row = i % 3
        bx = MARGIN + 14 + col * (col_w + 24)
        by = by0 + 36 + row * 20
        d.text((bx, by), "\u2022  " + item, font=sans(14), fill=INK)

    # ---- Footer ----
    foot = ("Sources: CNN \u2022 Reuters \u2022 BBC \u2022 Al Jazeera \u2022 Le Monde \u2022 AP  "
            "|  Compiled Friday 20 November 2026")
    fw = d.textlength(foot, font=sans(13))
    d.text(((W - fw) / 2, 972), foot, font=sans(13), fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
