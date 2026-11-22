"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

Fresh code written for make.fun news-image-20261122. All artwork is drawn
with Pillow primitives; all text is set in DejaVu / Noto fonts shipped on
the build machine. No network, no downloaded assets.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 230)
CARD = (255, 255, 255)
INK = (26, 36, 51)
MUTED = (90, 100, 114)
RULE = (26, 36, 51)
CARD_LINE = (216, 210, 192)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, fnt, fill, x0=0, x1=W):
    tw = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - tw) / 2, y), text, font=fnt, fill=fill)


# ---- tiny icons, drawn with primitives, one per story ----

def icon_flame(d, x, y, s, c):
    # outer flame
    d.polygon([(x + s * 0.50, y + s * 0.02), (x + s * 0.86, y + s * 0.42),
               (x + s * 0.78, y + s * 0.82), (x + s * 0.50, y + s * 0.98),
               (x + s * 0.22, y + s * 0.82), (x + s * 0.14, y + s * 0.42)],
              fill=c)
    # inner flame, lighter
    d.polygon([(x + s * 0.50, y + s * 0.30), (x + s * 0.70, y + s * 0.58),
               (x + s * 0.62, y + s * 0.84), (x + s * 0.50, y + s * 0.92),
               (x + s * 0.38, y + s * 0.84), (x + s * 0.30, y + s * 0.58)],
              fill=(255, 214, 120))


def icon_rocket(d, x, y, s, c):
    # diagonal rocket body
    d.polygon([(x + s * 0.55, y + s * 0.05), (x + s * 0.85, y + s * 0.35),
               (x + s * 0.62, y + s * 0.62), (x + s * 0.35, y + s * 0.85),
               (x + s * 0.15, y + s * 0.62), (x + s * 0.38, y + s * 0.38)],
              fill=c)
    # nose window
    d.ellipse([x + s * 0.52, y + s * 0.22, x + s * 0.72, y + s * 0.42],
              fill=(255, 255, 255))
    # fins
    d.polygon([(x + s * 0.35, y + s * 0.85), (x + s * 0.12, y + s * 0.98),
               (x + s * 0.52, y + s * 0.72)], fill=c)
    d.polygon([(x + s * 0.62, y + s * 0.62), (x + s * 0.98, y + s * 0.88),
               (x + s * 0.72, y + s * 0.52)], fill=c)
    # exhaust flame
    d.polygon([(x + s * 0.15, y + s * 0.62), (x + s * 0.02, y + s * 0.78),
               (x + s * 0.28, y + s * 0.92)], fill=(255, 170, 60))


def icon_rings(d, x, y, s, c):
    # two interlocked trade rings
    d.ellipse([x + s * 0.06, y + s * 0.18, x + s * 0.58, y + s * 0.82],
              outline=c, width=7)
    d.ellipse([x + s * 0.42, y + s * 0.18, x + s * 0.94, y + s * 0.82],
              outline=(200, 120, 30), width=7)
    # small handshake dot where they cross
    d.ellipse([x + s * 0.44, y + s * 0.44, x + s * 0.56, y + s * 0.56],
              fill=c)


def icon_globe(d, x, y, s, c):
    d.ellipse([x + s * 0.05, y + s * 0.05, x + s * 0.95, y + s * 0.95],
              outline=c, width=6)
    d.ellipse([x + s * 0.05, y + s * 0.05, x + s * 0.95, y + s * 0.95],
              fill=(190, 225, 200))
    d.ellipse([x + s * 0.05, y + s * 0.05, x + s * 0.95, y + s * 0.95],
              outline=c, width=6)
    # latitude lines
    d.arc([x + s * 0.05, y + s * 0.28, x + s * 0.95, y + s * 0.72],
          start=0, end=360, fill=c, width=3)
    d.arc([x + s * 0.28, y + s * 0.05, x + s * 0.72, y + s * 0.95],
          start=0, end=360, fill=c, width=3)
    # leaf sprout on top
    d.polygon([(x + s * 0.50, y + s * 0.02), (x + s * 0.66, y + s * 0.16),
               (x + s * 0.50, y + s * 0.24), (x + s * 0.34, y + s * 0.16)],
              fill=(70, 140, 70))


def icon_waves(d, x, y, s, c):
    for i, yy in enumerate((0.22, 0.48, 0.74)):
        d.arc([x + s * 0.05, y + s * yy, x + s * 0.95, y + s * (yy + 0.34)],
              start=200, end=340, fill=c, width=7)
    # a small house roof above the water
    d.polygon([(x + s * 0.50, y + s * 0.02), (x + s * 0.78, y + s * 0.20),
               (x + s * 0.22, y + s * 0.20)], fill=(200, 120, 30))


def icon_badge(d, x, y, s, c):
    # five-point star inside a ring: a capture / law-enforcement badge
    cx, cy, r = x + s * 0.5, y + s * 0.52, s * 0.44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=6)
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = s * 0.34 if i % 2 == 0 else s * 0.15
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=c)


# ---- the day's stories: (tag, colour, icon, headline, summary) ----

STORIES = [
    ("MIDDLE EAST", (179, 64, 42), icon_flame,
     "Iran strikes US base in Bahrain",
     "Tehran hits an industrial site near US forces; Bahrain says its air "
     "defences intercepted the attack."),
    ("UKRAINE", (39, 76, 119), icon_rocket,
     "Missile hits Lviv",
     "A Russian strike on the western city kills 2 and injures 10, as the "
     "war reaches far from the front."),
    ("TRADE", (14, 124, 107), icon_rings,
     "EU\u2013Indonesia sign landmark deal",
     "After a decade of talks, the pact scraps 98.5% of tariffs between the "
     "EU and South-East Asia's largest economy."),
    ("CLIMATE", (91, 122, 41), icon_globe,
     "COP31 talks stall in Turkey",
     "The UN climate summit runs into overtime, deadlocked over fossil "
     "fuels and finance for poorer nations."),
    ("GAZA", (108, 74, 176), icon_waves,
     "Floods deepen Gaza's crisis",
     "Australia, Canada, Italy and the UK urge Israel to open aid routes "
     "as flooding adds to the misery."),
    ("MEXICO", (192, 122, 26), icon_badge,
     "Cartel boss \u2018El Chapo Isidro\u2019 captured",
     "Mexican forces seize a top drug lord in the latest of a string of "
     "high-profile arrests."),
]

ALSO = ("Also today:  Eisenkot asked to form Israel's next government  \u00b7  "
        "Hong Kong votes for its Election Committee  \u00b7  Alcaraz faces "
        "Zverev in the ATP Finals  \u00b7  Norway court voids disputed oil "
        "licences")


def draw_card(d, x, y, w, h, tag, color, icon, headline, summary):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_LINE, width=1)
    d.rectangle([x, y, x + w, y + 6], fill=color)
    # icon
    icon(d, x + 16, y + 22, 64, color)
    # tag
    d.text((x + 96, y + 22), tag, font=font(SANS_B, 16), fill=color)
    # headline, up to 2 lines
    hl = font(SERIF_B, 26)
    lines = wrap(d, headline, hl, w - 96 - 16)
    hy = y + 46
    for ln in lines[:2]:
        d.text((x + 96, hy), ln, font=hl, fill=INK)
        hy += 31
    # summary, up to 3 lines, full card width
    sm = font(SANS_R, 19)
    slines = wrap(d, summary, sm, w - 32)
    sy = y + 122
    for ln in slines[:3]:
        d.text((x + 16, sy), ln, font=sm, fill=MUTED)
        sy += 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    center(d, 20, "A ONE-PAGE NEWSPAPER OF THE DAY'S WORLD NEWS",
           font(SANS_B, 15), MUTED)
    center(d, 44, "THE WORLD IN ONE PAGE", font(SERIF_B, 60), INK)
    d.line([(24, 122), (W - 24, 122)], fill=RULE, width=3)
    d.line([(24, 127), (W - 24, 127)], fill=RULE, width=1)
    center(d, 138, "SUNDAY, 22 NOVEMBER 2026", font(SANS_B, 23), (179, 64, 42))
    center(d, 168, "Six stories that defined the day",
           font(SERIF_R, 19), MUTED)

    # story grid: 2 x 3
    gx, gy, gap = 24, 196, 16
    cw = (W - 2 * gx - gap) // 2
    ch = 224
    for i, (tag, color, icon, headline, summary) in enumerate(STORIES):
        cx = gx + (i % 2) * (cw + gap)
        cy = gy + (i // 2) * (ch + gap)
        draw_card(d, cx, cy, cw, ch, tag, color, icon, headline, summary)

    # footer: also-today strip
    fy = gy + 3 * ch + 2 * gap + 14
    d.line([(24, fy), (W - 24, fy)], fill=RULE, width=1)
    d.text((24, fy + 12), "ALSO TODAY", font=font(SANS_B, 16), fill=(179, 64, 42))
    also_font = font(SANS_R, 17)
    lines = wrap(d, ALSO, also_font, W - 48)
    ay = fy + 36
    for ln in lines[:2]:
        d.text((24, ay), ln, font=also_font, fill=INK)
        ay += 23
    center(d, H - 26, "Sources: Reuters  \u00b7  AP  \u00b7  Al Jazeera  \u00b7  BBC",
           font(SANS_R, 13), MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
