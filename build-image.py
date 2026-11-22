#!/usr/bin/env python3
"""Render the front page of Saturday 21 November 2026 as one 1024x1024 image.
v4: WARTIME restyle. Aged sepia newsprint with grain, blackletter-style
heavy serif masthead, WAR EDITION banner, WAR BULLETIN band, double rules,
column rules, black + blood-red ink only. Same content as v3 (39 stories,
9 regions, 12 fields, 11 drawn cards, UTC strip, world map, ALSO ON,
VERDICT, DATE CHECK) — only the visual style changed, not the facts.
Deterministic: no network, no clock, seeded randomness only. PIL only.
Run: python3 build-image.py  -> writes entry.png next to this file.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
DEJAVU = "/usr/share/fonts/truetype/dejavu"
LIB = "/usr/share/fonts/truetype/liberation"
NOTO = "/usr/share/fonts/truetype/noto"

# ---- palette: aged wartime newsprint — sepia paper, black ink, blood red ----
PAPER = (229, 209, 171)
CARD = (236, 219, 186)
INK = (24, 20, 15)
RED = (139, 12, 12)
GREY = (96, 84, 66)
RULE = (24, 20, 15)
SEA = (206, 190, 152)
LAND = (168, 146, 104)
SEPIA_DK = (58, 48, 32)
SEPIA_MD = (120, 100, 66)
ORANGE = (178, 110, 32)

W, H = 1024, 1024

def font(path, size):
    return ImageFont.truetype(path, size)

# Wartime type: heavy condensed serif for the nameplate, black display serif
# for headlines, Times-like Liberation Serif for body and card text.
F_MAST = lambda s: font(os.path.join(NOTO, "NotoSerif-CondensedBlack.ttf"), s)
F_HEAD = lambda s: font(os.path.join(NOTO, "NotoSerifDisplay-Black.ttf"), s)
F_SERIF = lambda s: font(os.path.join(LIB, "LiberationSerif-Regular.ttf"), s)
F_SERIF_B = lambda s: font(os.path.join(LIB, "LiberationSerif-Bold.ttf"), s)
F_SERIF_I = lambda s: font(os.path.join(LIB, "LiberationSerif-Italic.ttf"), s)
F_SANS = lambda s: font(os.path.join(DEJAVU, "DejaVuSans.ttf"), s)
F_SANS_B = lambda s: font(os.path.join(DEJAVU, "DejaVuSans-Bold.ttf"), s)

def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, xy, text, fnt, color, width, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y

def hline(draw, x0, x1, y, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)

def double_rule(draw, x0, x1, y, color=INK):
    """Classic newspaper double rule: thick line over a thin one."""
    draw.line([(x0, y), (x1, y)], fill=color, width=4)
    draw.line([(x0, y + 7), (x1, y + 7)], fill=color, width=1)

def flag_bar(draw, x, y, w, h, colors):
    cx = x
    for rgb, share in colors:
        sw = int(w * share)
        draw.rectangle([cx, y, cx + sw, y + h], fill=rgb)
        cx += sw

def mini_chart(draw, x, y, w, h, values, color=RED):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 204, 168), outline=GREY)
    if not values:
        return
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1
    pts = []
    for i, v in enumerate(values):
        px = x + 4 + (w - 8) * i / (len(values) - 1)
        py = y + h - 4 - (h - 8) * (v - lo) / span
        pts.append((px, py))
    draw.line(pts, fill=color, width=2)
    for px, py in pts:
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=color)

def grain(draw, seed=21112026):
    """Aged-paper grain: deterministic speckles + a few faint stains."""
    rng = random.Random(seed)
    # fine dark speckles
    for _ in range(2600):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, H - 1)
        c = rng.choice([(214, 192, 152), (206, 184, 142), (240, 224, 192)])
        draw.point((x, y), fill=c)
    # a few larger faint blotches (stains)
    for _ in range(9):
        cx = rng.randint(60, W - 60)
        cy = rng.randint(60, H - 60)
        rx = rng.randint(28, 90)
        ry = rng.randint(18, 55)
        col = rng.choice([(218, 198, 158), (210, 188, 146)])
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=col, width=1)
    # darker edge vignette: short strokes along the border
    for _ in range(420):
        side = rng.randint(0, 3)
        if side == 0:
            x, y = rng.randint(0, W - 1), rng.randint(0, 7)
        elif side == 1:
            x, y = rng.randint(0, W - 1), rng.randint(H - 8, H - 1)
        elif side == 2:
            x, y = rng.randint(0, 7), rng.randint(0, H - 1)
        else:
            x, y = rng.randint(W - 8, W - 1), rng.randint(0, H - 1)
        draw.point((x, y), fill=(200, 178, 136))

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
grain(d)
M = 28
CW = W - 2 * M

# ================= MASTHEAD — wartime nameplate =================
y = 14
d.text((M, y), "THE WORLD IN ONE PICTURE", font=F_MAST(22), fill=INK)
# WAR EDITION box, top right
we = "WAR EDITION"
we_w = int(d.textlength(we, font=F_SANS_B(13))) + 20
wx = W - M - we_w
d.rectangle([wx, y + 1, wx + we_w, y + 24], fill=INK)
d.text((wx + 10, y + 5), we, font=F_SANS_B(13), fill=(245, 236, 214))
d.text((M, y + 27), "EST. 2026  ·  ONE DAY, ONE PAGE", font=F_SANS(10), fill=GREY)
y += 38
double_rule(d, M, W - M, y)
y += 10
d.text((M, y), "SATURDAY 21 NOVEMBER 2026", font=F_HEAD(44), fill=INK)
y += 46
box_w, box_h = 148, 20
bx, by = W - M - box_w, y
d.rectangle([bx, by, bx + box_w, by + box_h], outline=INK, width=2)
d.text((bx + 8, by + 4), "SATURDAY 21 NOV 2026", font=F_SERIF_B(11), fill=RED)
d.text((M, y + 2), "39 STORIES  ·  9 REGIONS  ·  12 FIELDS  ·  11 DRAWN — EVERY ONE FROM SATURDAY 21 NOVEMBER", font=F_SERIF_B(13), fill=INK)
y += 22
hline(d, M, W - M, y, INK, 2)
y += 5
# WAR BULLETIN band: black bar, white type — the late-news strip
band_h = 24
d.rectangle([M, y, W - M, y + band_h], fill=INK)
d.text((M + 10, y + 5), "★  WAR BULLETIN  ★", font=F_SANS_B(12), fill=(245, 236, 214))
bx2 = M + 10 + int(d.textlength("★  WAR BULLETIN  ★  ", font=F_SANS_B(12)))
d.text((bx2, y + 5), "IRAN HITS US BASES IN BAHRAIN  •  MEXICO SEIZES FBI MOST-WANTED CARTEL BOSS  •  S&P 500 −3.7%",
       font=F_SERIF_B(12), fill=(245, 236, 214))
y += band_h + 4

# ================= STATS ROW =================
stats = [
    ("-3.7%", "S&P 500, into correction"),
    ("11", "killed in Sinaloa raid"),
    ("2", "killed in Kryvyi Rih"),
    ("60", "wounded in Kryvyi Rih"),
    ("109–0", "Denmark backs Greenland"),
    ("25", "nations in youth walkout"),
]
sw = CW // 6
for i, (num, lab) in enumerate(stats):
    x = M + i * sw
    d.text((x + 4, y), num, font=F_HEAD(24), fill=RED if i == 0 else INK)
    d.text((x + 4, y + 30), lab, font=F_SERIF(10), fill=GREY)
    if i:
        d.line([(x, y + 2), (x, y + 38)], fill=GREY, width=1)
y += 38
hline(d, M, W - M, y, INK, 2)
y += 6

# ================= THE DAY BY HOURS — UTC STRIP =================
d.text((M, y), "THE DAY BY HOURS — ALL TIMES UTC", font=F_SERIF_B(13), fill=INK)
y += 16
strip_y = y
strip_h = 30
# UTC scale: 00 - 24 across the content width
d.line([(M, strip_y + 8), (W - M, strip_y + 8)], fill=GREY, width=1)
for hh in (0, 6, 12, 18, 24):
    tx = M + CW * hh // 24
    d.line([(tx, strip_y + 4), (tx, strip_y + 12)], fill=GREY, width=1)
    lab = "%02d" % hh
    d.text((tx - 7, strip_y + 14), lab, font=F_SANS(9), fill=GREY)
beats = [
    ("MORNING", "Mexico: Chapo Isidro captured", 7),
    ("MIDDAY", "Kryvyi Rih: 2 dead, 60 hurt", 12),
    ("AFTERNOON", "Markets: S&P −3.7%, correction", 15),
    ("EVENING", "COP31: past deadline, no deal", 18),
    ("NIGHT", "Iran hits US bases", 21),
]
for hh_label, lab, hour in beats:
    bx = M + CW * hour // 24
    d.ellipse([bx - 5, strip_y + 3, bx + 5, strip_y + 13], fill=RED, outline=(245, 236, 214), width=1)
    d.text((bx - 24, strip_y + 24), hh_label, font=F_SANS_B(8), fill=INK)
y = strip_y + strip_h + 6
hline(d, M, W - M, y, INK, 2)
y += 6

# ================= STORY CARDS =================
def card(draw, x, y, w, h, kicker, title, body, source, art, tag="REPORTED",
         title_size=15, body_size=10, art_h=22):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=1)
    ax, ay, aw = x + 8, y + 8, w - 16
    art(draw, ax, ay, aw, art_h)
    cy = y + 8 + art_h + 6
    draw.rectangle([x + 8, cy, x + 8 + 62, cy + 13], fill=INK)
    draw.text((x + 11, cy + 1), tag, font=F_SANS_B(8), fill=(245, 236, 214))
    draw.text((x + 76, cy + 1), kicker, font=F_SANS_B(8), fill=RED)
    cy += 17
    cy = para(draw, (x + 8, cy), title, F_SERIF_B(title_size), INK, w - 16, leading=title_size + 3)
    cy = para(draw, (x + 8, cy + 2), body, F_SERIF(body_size), INK, w - 16, leading=12)
    draw.text((x + 8, y + h - 15), "Source: " + source, font=F_SERIF_I(8), fill=GREY)
    return y + h

def art_bahrain(draw, x, y, w, h):
    # night sky in black ink, white stars, red tracer arcs, dark rooftops
    draw.rectangle([x, y, x + w, y + h], fill=(18, 16, 12))
    for i in range(12):
        px = x + (i * 37) % w
        py = y + (i * 13) % (h // 2)
        draw.ellipse([px, py, px + 2, py + 2], fill=(245, 236, 214))
    draw.arc([x + 6, y + 4, x + w - 6, y + h + 26], 200, 340, fill=ORANGE, width=3)
    draw.arc([x + 22, y, x + w - 22, y + h + 16], 210, 330, fill=RED, width=2)
    draw.rectangle([x, y + h - 10, x + w, y + h], fill=(10, 9, 7))
    for bx in range(x + 8, x + w - 8, 26):
        draw.rectangle([bx, y + h - 18, bx + 14, y + h - 10], fill=(40, 34, 24))

def art_sinaloa(draw, x, y, w, h):
    # flag rendered in sepia tones, flames in red/orange
    flag_bar(draw, x, y, w, h // 2, [((58, 48, 32), 1 / 3), ((236, 219, 186), 1 / 3), ((139, 12, 12), 1 / 3)])
    draw.rectangle([x, y + h // 2, x + w, y + h], fill=(30, 26, 20))
    for fx in (x + 12, x + w // 2 - 8, x + w - 30):
        draw.polygon([(fx, y + h - 4), (fx + 6, y + h - 16), (fx + 12, y + h - 4)], fill=ORANGE)
        draw.polygon([(fx + 3, y + h - 4), (fx + 6, y + h - 11), (fx + 9, y + h - 4)], fill=(245, 236, 214))

def art_kryvyi(draw, x, y, w, h):
    # ruined rooftops in dark sepia, smoke in grey
    draw.rectangle([x, y, x + w, y + h], fill=(72, 58, 40))
    draw.rectangle([x, y + h - 14, x + w // 2 - 6, y + h], fill=(28, 22, 16))
    draw.polygon([(x + w // 2, y + h - 14), (x + w - 10, y + h - 24), (x + w, y + h - 14), (x + w, y + h), (x + w // 2, y + h)], fill=(44, 36, 24))
    for sx, sy, r in [(w // 2 + 14, 7, 6), (w // 2 + 26, 2, 8), (w // 2 + 40, 9, 5)]:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=(150, 140, 120))

def art_markets(draw, x, y, w, h):
    mini_chart(draw, x, y, w, h, [96, 92, 94, 88, 80, 74, 66, 58], color=RED)

def art_cop(draw, x, y, w, h):
    # globe in black ink on sepia, white meridians
    draw.rectangle([x, y, x + w, y + h], fill=INK)
    draw.ellipse([x + w // 2 - 13, y + 4, x + w // 2 + 13, y + 30], outline=(245, 236, 214), width=2)
    draw.line([(x + w // 2 - 13, y + 17), (x + w // 2 + 13, y + 17)], fill=(245, 236, 214), width=1)
    draw.line([(x + w // 2, y + 4), (x + w // 2, y + 30)], fill=(245, 236, 214), width=1)

def art_shenzhen(draw, x, y, w, h):
    # three powers in black, paper and blood red
    flag_bar(draw, x, y, w, h, [((139, 12, 12), 1 / 3), ((236, 219, 186), 1 / 3), ((24, 20, 15), 1 / 3)])
    draw.text((x + 6, y + h - 14), "USA · CHINA · RUSSIA", font=F_SANS_B(9), fill=(245, 236, 214))

def art_dengue(draw, x, y, w, h):
    # mosquito in black ink on pale sepia
    draw.rectangle([x, y, x + w, y + h], fill=(226, 210, 176))
    draw.ellipse([x + w // 2 - 10, y + 6, x + w // 2 + 10, y + 26], outline=INK, width=3)
    for dx, dy in [(-14, -8), (14, -8), (-14, 10), (14, 10)]:
        draw.line([(x + w // 2, y + 16), (x + w // 2 + dx, y + 16 + dy)], fill=INK, width=2)

def art_cancer(draw, x, y, w, h):
    # pill in blood red on pale sepia
    draw.rectangle([x, y, x + w, y + h], fill=(226, 210, 176))
    draw.ellipse([x + w // 2 - 11, y + 5, x + w // 2 + 11, y + 27], fill=RED)
    draw.ellipse([x + w // 2 - 5, y + 11, x + w // 2 + 5, y + 21], fill=(245, 236, 214))
    draw.text((x + w // 2 - 3, y + 12), "1", font=F_SANS_B(8), fill=RED)

def art_youth(draw, x, y, w, h):
    # marching figures in sepia brown on pale paper
    draw.rectangle([x, y, x + w, y + h], fill=(238, 224, 192))
    for i in range(5):
        px = x + 10 + i * (w - 20) // 4
        draw.ellipse([px - 4, y + 8, px + 4, y + 16], fill=SEPIA_MD)
        draw.rectangle([px - 2, y + 16, px + 2, y + 28], fill=SEPIA_MD)
    draw.line([(x + 6, y + 28), (x + w - 6, y + 28)], fill=SEPIA_MD, width=2)

def art_denmark(draw, x, y, w, h):
    # Danish cross: blood red field, paper cross (unchanged — already wartime)
    draw.rectangle([x, y, x + w, y + h], fill=(139, 12, 12))
    draw.rectangle([x + w // 4, y, x + w // 4 + 8, y + h], fill=(245, 236, 214))
    draw.rectangle([x, y + h // 2 - 4, x + w, y + h // 2 + 4], fill=(245, 236, 214))

def art_nvidia(draw, x, y, w, h):
    mini_chart(draw, x, y, w, h, [90, 88, 84, 78, 70, 62, 55, 48], color=INK)

# --- top row: 3 big cards ---
big = [
    ("BAHRAIN · CONFLICT", "Iran strikes US bases in Bahrain",
     "The Revolutionary Guards say they hit US positions at al-Riffa and Awali. Bahrain says the strike hit a civilian industrial site and started a fire; air defences intercepted other attacks. No injuries reported.",
     "Reuters", art_bahrain),
    ("SINALOA · JUSTICE", "Mexico seizes FBI most-wanted cartel boss",
     "Special forces captured Fausto Isidro Meza Flores, “Chapo Isidro”, in Guasave. The raid set off gun battles, burning roadblocks and 11 deaths: 4 soldiers and 7 gunmen.",
     "Reuters", art_sinaloa),
    ("KRYVYI RIH · CONFLICT", "Missile hits Zelensky’s hometown",
     "A Russian ballistic strike on central Kryvyi Rih killed 2 — a 7-year-old boy and a 20-year-old paramedic — and wounded 60. A missile also came down in Poland; NATO called it a grave violation.",
     "AP", art_kryvyi),
]
bw = (CW - 2 * 12) // 3
bh = 152
for i, (kick, title, body, src, art) in enumerate(big):
    card(d, M + i * (bw + 12), y, bw, bh, kick, title, body, src, art, art_h=22)
y += bh + 3

# --- second row: 4 small cards ---
small1 = [
    ("NEW YORK · MARKETS", "AI sell-off drags world markets down",
     "The S&P 500 fell 3.7% into correction as the AI-stock rout deepened. Nasdaq −5.3%; Nikkei −5.1%.",
     "AP", art_markets),
    ("ANTALYA · COP31", "Climate talks run past deadline",
     "The UN summit went into overtime with no deal. A second draft dropped all mention of fossil fuels.",
     "Carbon Brief", art_cop),
    ("SHENZHEN · POLITICS", "Trump defends Putin ties",
     "After a three-way summit with Xi in Shenzhen, Trump defended his ties to Putin. Zelensky called Putin “a killer”.",
     "OneTurn", art_shenzhen),
    ("BRAZIL · HEALTH", "Dengue breakthrough in Brazil",
     "Researchers report bacteria-carrying mosquitoes cut dengue cases among children in Brazil.",
     "OneTurn", art_dengue),
]
sw2 = (CW - 3 * 12) // 4
sh = 136
for i, (kick, title, body, src, art) in enumerate(small1):
    card(d, M + i * (sw2 + 12), y, sw2, sh, kick, title, body, src, art, title_size=14, art_h=22)
y += sh + 3

# --- third row: 4 small cards ---
small2 = [
    ("WORLD · HEALTH", "Cancer pill breakthrough",
     "Daraxonrasib: tumours became undetectable in 1 of 12 patients in early results.",
     "24h summary", art_cancer),
    ("EUROPE · SOCIETY", "Gen Z Youth Day of Action",
     "School and university walkouts swept 25 European countries in a coordinated day of action.",
     "24h summary", art_youth),
    ("DENMARK · POLITICS", "Denmark backs US-Greenland deal 109–0",
     "Copenhagen approved a new US security deal for Greenland, allowing two new American bases.",
     "24h summary", art_denmark),
    ("CHINA · TECH", "Nvidia halts H200 chip exports",
     "Nvidia stopped exports of its H200 AI chips to China, deepening the tech split.",
     "Standard Topic", art_nvidia),
]
for i, (kick, title, body, src, art) in enumerate(small2):
    card(d, M + i * (sw2 + 12), y, sw2, sh, kick, title, body, src, art, title_size=14, art_h=22)
y += sh + 3

# ================= WHERE IT HAPPENED — bigger world map =================
map_h = 66
d.rectangle([M, y, W - M, y + map_h], fill=SEA, outline=INK, width=1)
d.text((M + 8, y + 4), "WHERE IT HAPPENED — WORLD MAP", font=F_SERIF_B(11), fill=INK)
def lonlat(lon, lat):
    # Crop the map to the inhabited latitudes (75N to 55S) so the land
    # fills the strip instead of sitting in a thin band.
    return (M + 10 + (lon + 180) / 360 * (CW - 20),
            y + 20 + (75 - lat) / 130 * (map_h - 34))
# Simplified but recognisable continent outlines (Natural Earth style).
continents = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 73), (-105, 70), (-95, 80), (-85, 80), (-80, 73), (-75, 68), (-65, 62), (-55, 52), (-60, 46), (-70, 42), (-75, 35), (-80, 31), (-81, 26), (-88, 21), (-95, 18), (-100, 16), (-105, 20), (-112, 24), (-117, 33), (-124, 42), (-124, 49), (-135, 58), (-150, 60), (-162, 58), (-168, 66)],
    # South America
    [(-80, 10), (-77, 4), (-72, -3), (-70, -12), (-70, -20), (-68, -30), (-65, -40), (-68, -50), (-66, -55), (-70, -52), (-68, -45), (-62, -38), (-55, -34), (-48, -28), (-40, -20), (-35, -8), (-38, -3), (-45, 0), (-52, 5), (-60, 8), (-70, 11), (-80, 10)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (4, 53), (8, 57), (10, 59), (6, 61), (12, 56), (18, 56), (21, 55), (24, 59), (28, 61), (30, 63), (32, 70), (40, 68), (45, 66), (42, 62), (38, 58), (34, 54), (30, 50), (28, 45), (30, 42), (24, 40), (20, 40), (15, 44), (10, 44), (8, 39), (3, 38), (-2, 37), (-10, 36)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (12, 34), (20, 32), (30, 31), (35, 28), (38, 22), (42, 15), (48, 11), (51, 10), (46, 5), (42, 0), (40, -10), (38, -18), (35, -25), (32, -29), (28, -33), (20, -35), (16, -30), (12, -18), (9, -5), (9, 4), (0, 5), (-8, 5), (-13, 8), (-16, 12), (-17, 15), (-16, 20), (-15, 25), (-10, 30), (-6, 35)],
    # Asia
    [(30, 36), (36, 36), (40, 38), (44, 40), (48, 42), (52, 44), (56, 46), (60, 50), (65, 54), (68, 58), (72, 62), (75, 68), (80, 73), (88, 75), (96, 76), (104, 77), (112, 74), (120, 73), (128, 72), (136, 72), (144, 70), (152, 68), (160, 66), (170, 66), (178, 65), (172, 62), (165, 60), (158, 53), (152, 59), (145, 58), (142, 52), (140, 44), (136, 38), (130, 33), (127, 35), (122, 31), (120, 25), (115, 22), (110, 20), (108, 13), (105, 9), (100, 7), (97, 10), (94, 17), (91, 22), (88, 22), (85, 19), (80, 13), (77, 8), (75, 14), (72, 20), (69, 22), (66, 25), (62, 25), (58, 26), (55, 27), (52, 28), (50, 30), (48, 30), (44, 29), (40, 31), (35, 32), (30, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (135, -12), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)],
]
for poly in continents:
    pts = [lonlat(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=LAND)
pins = [
    # (number, lon, lat, dx, dy): dx/dy nudge the numbered circle off the true
    # spot (a thin leader line links it back) so clustered pins stay readable.
    ("1", 51, 26, 10, 8), ("2", -107, 25, 0, 0), ("3", 33, 48, 10, -8),
    ("4", -74, 41, 0, 0), ("5", 30, 37, -10, 8), ("6", 114, 22, 0, 0),
    ("7", -52, -10, 0, 0), ("8", 10, 56, 0, -8), ("9", 104, 35, 0, 0),
    ("10", -5, 50, -10, -6), ("11", -30, 30, 0, 0),
]
for num, lon, lat, dx, dy in pins:
    px, py = lonlat(lon, lat)
    if dx or dy:
        d.line([(px, py), (px + dx, py + dy)], fill=RED, width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        px, py = px + dx, py + dy
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(245, 236, 214), width=1)
    d.text((px - 3, py - 6), num, font=F_SANS_B(8), fill=(245, 236, 214))
d.text((M + 8, y + map_h - 14), "1 Bahrain  2 Sinaloa  3 Kryvyi Rih  4 New York  5 Antalya  6 Shenzhen  7 Brazil  8 Denmark  9 China  10 Europe  11 World",
       font=F_SERIF(9), fill=INK)
y += map_h + 4

# ================= ALSO ON + VERDICT =================
col_w = (CW - 12) // 2
ax = M
d.text((ax, y), "ALSO ON SATURDAY 21 NOVEMBER", font=F_SERIF_B(12), fill=INK)
ay = y + 17
also = [
    (12, "RIYADH", "Saudi downed 3 Houthi missiles."),
    (13, "YONGBYON", "N. Korea expanded enrichment."),
    (14, "HORMUZ", "Tanker attacks cut shipping 15%."),
    (15, "NEW YORK", "Anthropic slid, closed $88.91."),
    (16, "DELHI", "Modi opened SCO dialogue."),
    (17, "GULF OF FINLAND", "Sparta II on fire."),
    (18, "GAZA", "Seven hurt by Israeli fire."),
    (19, "BASRA", "Energy facility fire, 4 killed."),
    (20, "KHASAB", "Two more tankers hit near Oman."),
    (21, "COPENHAGEN", "Russia murder plot alleged."),
    (22, "OTTAWA", "Unaware of Hegseth memo."),
    (23, "WASHINGTON", "Vance rejects nuke claim."),
    (24, "KYIV", "Crimea Bridge hits called justified."),
    (25, "SHENZHEN", "Trump and Xi hold APEC talks."),
    (26, "QESHM", "IRGC claims downing US drone."),
    (27, "WASHINGTON", "Trump eyes AI-centre tax."),
    (28, "TOKYO", "Sila signs Panasonic anode deal."),
    (29, "CHINA", "Leapmotor passes 2 million EVs."),
    (30, "SINGAPORE", "Mistral AI picks Singapore hub."),
    (31, "ANTHROPIC", "Riemann proof claim in Lean."),
    (32, "POLAND", "Russian missiles enter SE Poland."),
    (33, "KRYVYI RIH", "Triple-tap kills boy, 7."),
    (34, "ANTALYA", "COP31 nears final deal Saturday."),
    (35, "SINALOA", "11 dead; fans flee gunfire."),
    (36, "BRAZIL", "Dengue cut ~69% in child study."),
    (37, "HARARE", "Zimbabwe taxes lithium exports."),
    (38, "COOK ISLANDS", "Cyclone Xavier weakens, Cat 5."),
    (39, "LONDON", "Leeds stun Chelsea 4-1."),
]
# two columns: 14 left, 14 right; one line per item, numbered on from the 11 cards
n_left = 14
for col in range(2):
    cx = ax + col * (col_w // 2)
    items = also[:n_left] if col == 0 else also[n_left:]
    for row, (num, city, line) in enumerate(items):
        ly = ay + row * 10
        num_s = "%d." % num
        d.text((cx, ly), num_s, font=F_SERIF_B(9), fill=RED)
        d.text((cx + d.textlength(num_s, font=F_SERIF_B(9)) + 3, ly),
               "%s — %s" % (city, line), font=F_SERIF(9), fill=INK)
    # wartime column rule between the two ALSO ON columns
    if col == 0:
        d.line([(ax + col_w // 2 - 6, ay - 2), (ax + col_w // 2 - 6, ay + 14 * 10)],
               fill=GREY, width=1)
ay += 14 * 10 + 4
vx = M + col_w + 12
d.text((vx, y), "THE VERDICT", font=F_SERIF_B(12), fill=RED)
vy = para(d, (vx, y + 17),
          "Two wars heating up at once — Iran hit US forces in the Gulf, Russia hit Zelensky’s hometown — and the AI rout turned a wobble into a correction.",
          F_SERIF(10), INK, col_w, leading=13)
vy += 4
d.text((vx, vy), "HOW SURE ARE WE?  ", font=F_SERIF_B(10), fill=INK)
vy += 14
for lab, desc in [("REPORTED", "confirmed by a named source"),
                  ("CLAIM", "one side’s claim, unverified"),
                  ("FORECAST", "expected, not what happened")]:
    d.rectangle([vx, vy + 1, vx + 58, vy + 12], fill=RED if lab == "REPORTED" else INK)
    d.text((vx + 4, vy + 2), lab, font=F_SANS_B(8), fill=(245, 236, 214))
    d.text((vx + 64, vy + 2), desc, font=F_SERIF(9), fill=INK)
    vy += 14
y = max(ay, vy) + 2
hline(d, M, W - M, y, INK, 1)
y += 4

# ================= DATE CHECK =================
d.text((M, y), "DATE CHECK — LOUD IN THE HEADLINES, BUT NOT 21 NOVEMBER NEWS", font=F_SERIF_B(11), fill=INK)
y += 12
dc = [
    "✕  Shenzhen Trump–Xi–Putin summit itself: 20 Nov.",
    "✕  World Court: Myanmar genocide ruling: 20 Nov.",
    "✕  Anthropic IPO priced at $83: 19 Nov.",
    "✕  UK–EU reset deal signed: 20 Nov.",
]
for col in range(2):
    for row in range(2):
        d.text((M + col * (CW // 2), y + row * 10), dc[col * 2 + row], font=F_SERIF(10), fill=GREY)
y += 2 * 10 + 4
double_rule(d, M, W - M, y)
y += 10

# ================= FOOTER =================
y = para(d, (M, y),
         "Every story here happened, or was first reported, on Saturday 21 November 2026. Sources: Reuters, AP, BBC, Xinhua, WSJ, CNN, Carbon Brief, Standard Topic, OneTurn, IntelChron, Majik, UKMTO, The Verge, InsightEx, Jerusalem Post, Radarr Africa, LiveScore.",
         F_SERIF_I(10), GREY, CW, leading=12)

print("final y =", y, "canvas H =", H)
assert y <= H - 14, "layout overflow: final y %d > %d" % (y, H - 14)
img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes", img.size)
