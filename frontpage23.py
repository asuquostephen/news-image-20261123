#!/usr/bin/env python3
"""frontpage23.py -- draw the 23 November 2026 front page.

A fresh single-file renderer written for this edition. It measures
every block with the real fonts before drawing anything, flows the
briefs into three ruled columns with a greedy balanced fill, and
steps the brief type down (then sheds the lowest-priority briefs)
until the sheet fits inside 1024x1024. Brief headlines are kept
short on purpose (about one column line each) so that 50 sourced
stories fit on one sheet. The story count printed in the strap
line is always the number of stories actually on the page.

Run:  python3 frontpage23.py [out.png]     (needs Pillow)
"""

import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 22
GUTTER = 14
PAPER = (248, 244, 233)
INK = (25, 23, 19)
GREY = (110, 104, 90)
RULE = (185, 178, 160)
RED = (158, 27, 27)
NAVY = (20, 33, 61)
GOLD = (176, 141, 58)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

# Confidence: "full" = confirmed by a named source, "half" = one
# side's claim or a single source, "open" = unconfirmed.
LEAD = {
    "kicker": "THE LEAD  --  MIDDLE EAST",
    "head": "Trump: US will resume Iran strikes after the New Year if no deal",
    "deck": ("President Trump says Iranian vessels testing the US naval blockade "
             "\"will all be at the bottom of the sea\". Tehran vows to use "
             "\"all available means\" to break the blockade, and says the Strait "
             "of Hormuz could reopen within hours if Washington meets its terms."),
    "src": "Fox News via Gulf News; The Express Tribune  --  23 Nov",
    "conf": "full",
}

SECOND = [
    {
        "kicker": "MARKETS  --  THE COMEBACK",
        "head": "Nvidia soars 33% as Huang returns",
        "deck": ("S&P 500 +5%, Nasdaq +7%, Dow +1,344 as the chipmaker reinstates "
                 "Jensen Huang as chief executive, 11 days after he resigned."),
        "src": "The Business Times; Reuters; AP  --  23 Nov",
        "conf": "full",
    },
    {
        "kicker": "EUROPE  --  WAR AT SEA",
        "head": "Ukraine: sea drones sank a Russian warship off Libya",
        "deck": ("Zelenskyy says seven naval drones sank the corvette Merkury at "
                 "Benghazi and hit the cargo ship Angara. Moscow has not commented."),
        "src": "AP; Dawn  --  23 Nov",
        "conf": "half",
    },
]

# (section, headline, source, confidence) -- priority order: the
# tail of this list is shed first if the page ever overflows.
# Headlines are kept to about one column line (~56 chars) so that
# all 50 stories fit on the sheet.
BRIEFS = [
    ("MIDDLE EAST", "Iran vows 'all means' to counter US blockade", "Gulf News", "full"),
    ("MIDDLE EAST", "US struck Iran oil tanker, analyst says", "Gulf News", "open"),
    ("MIDDLE EAST", "Iran demands $290bn from US in damages", "Gulf News", "full"),
    ("MIDDLE EAST", "Israeli strike kills UNRWA worker in Jabalia", "Reuters", "full"),
    ("MIDDLE EAST", "Netanyahu-Eisenkot talks end with no deal", "AFP", "full"),
    ("MIDDLE EAST", "Israeli army suicides hit 16-year high: 23 dead", "Haaretz", "full"),
    ("MIDDLE EAST", "Yemen strikes kill 5, injure 18, sources say", "Xinhua", "full"),
    ("EUROPE", "Russian strike on Kyiv flats kills 11; 14 missing", "AP", "full"),
    ("EUROPE", "Russian cargo ship ablaze in Baltic after strike", "Dunya News", "full"),
    ("EUROPE", "Rostov refinery halts after 'massive' attack", "AP", "full"),
    ("EUROPE", "Medvedev: Russia may be 'obliged' to use nukes", "Yeni Safak", "full"),
    ("EUROPE", "Germany tests kamikaze drones in Lithuania", "Dunya News", "full"),
    ("EUROPE", "EU proposes 3% digital tax on big tech", "Probes Pakistan", "half"),
    ("EUROPE", "Saudi role 'loomed large' in failed COP31 deal", "Dunya News", "full"),
    ("AMERICAS", "Democrats take 258 House seats, most since 1992", "AP", "full"),
    ("AMERICAS", "Democrats plan 12 debates for 2028 primary", "AP", "full"),
    ("AMERICAS", "ICE detains father, daughter at Seattle airport", "AP", "full"),
    ("AMERICAS", "Delta fault delays 1,000+ Thanksgiving flights", "AP", "full"),
    ("AMERICAS", "US forms team to stop air-traffic outages", "Yeni Safak", "full"),
    ("AMERICAS", "USDA cyber breach in fifth day, farm aid hit", "SecureResearch", "half"),
    ("AMERICAS", "NYT: Alice Huang linked to China spy agency", "NYT", "half"),
    ("AFRICA", "Libya blames Ukraine 'fully' for Benghazi strikes", "Yeni Safak", "full"),
    ("AFRICA", "UN: Libya 'must not become a battleground'", "UNSMIL", "full"),
    ("AFRICA", "Sudan drones kill 4, hit UN building in Khartoum", "Yeni Safak", "full"),
    ("AFRICA", "RSF accused of looting in West Kordofan", "Yeni Safak", "full"),
    ("AFRICA", "Boat of mourners capsizes in Nigeria; 24 dead", "Starlit Daily", "full"),
    ("AFRICA", "Huge fire at fuel station on Lagos edge", "Starlit Daily", "full"),
    ("AFRICA", "Tinubu launches manifesto, targets 6% growth", "Starlit Daily", "full"),
    ("AFRICA", "Kenya, DR Congo restore full diplomatic ties", "Starlit Daily", "full"),
    ("AFRICA", "South Africa: 581 women murdered in 3 months", "BusinessDay", "full"),
    ("AFRICA", "DR Congo Ebola outbreak passes 11,000 cases", "BusinessDay", "full"),
    ("AFRICA", "New coalition to govern Johannesburg", "Daily Plug", "half"),
    ("ASIA-PACIFIC", "Kospi falls 3.3% as chip rout deepens", "Al Jazeera", "full"),
    ("ASIA-PACIFIC", "Indonesia factory blaze kills 24, dozens missing", "Dunya News", "full"),
    ("ASIA-PACIFIC", "S. Korea education chief quits over exam chaos", "Xinhua", "full"),
    ("ASIA-PACIFIC", "Bangladesh vows to arrest Hasina on return", "Reuters", "full"),
    ("ASIA-PACIFIC", "Lahore tops pollution ranking, AQI above 500", "Geo News", "full"),
    ("ASIA-PACIFIC", "Magnitude 4.0 quake hits Pakistan border area", "Times of India", "full"),
    ("ASIA-PACIFIC", "Pakistan seeks bids for 800,000t wheat imports", "Express Tribune", "full"),
    ("ASIA-PACIFIC", "Eleven dead in S. Korea car-plant fire", "Manila Times", "full"),
    ("ASIA-PACIFIC", "Indonesia sacks general in wiretap scandal", "Manila Times", "full"),
    ("ASIA-PACIFIC", "N. Korea's Kim: security, not supremacy, sought", "Economic Times", "half"),
    ("MARKETS & BUSINESS", "Korea chip exports $38.5bn in 20 days, +294%", "Korea Customs", "full"),
    ("SCIENCE & TECH", "GTA VI patch: 603 MB on PS5, 160 GB on Xbox", "Probes Pakistan", "half"),
    ("SPORT", "49ers crush Vikings 35-10 in Mexico City", "Flashscore", "full"),
    ("SPORT", "Cowboys pile up 51-30 win over Titans", "Flashscore", "full"),
    ("SPORT", "NBA: Denver 151-145 Chicago in OT; Miami win", "Flashscore", "full"),
]

TIMELINE = [
    ("00:00", "Seoul: Korea chip exports $38.5bn for 1-20 Nov"),
    ("01:24", "Herzliya: Netanyahu-Eisenkot talks end, no deal"),
    ("06:30", "Seoul: Kospi closes down 3.31% at 4,708.54"),
    ("07:37", "Kyiv: Zelenskyy says sea drones sank Merkury"),
    ("10:16", "Kyiv: AP reports Ukraine's Benghazi claim"),
    ("14:34", "New York: Nasdaq-100 up 6.6%, Nvidia +33%"),
]

MARKETS = ("MARKETS  --  Kospi -3.31%  |  S&P 500 +5%  |  Nasdaq +7%  |  "
           "Dow +1,344  |  Nvidia +33%  |  Brent $92.57  |  WTI $83.98")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def line_h(fnt):
    return int(fnt.size * 1.22)


def draw_conf(draw, x, y, kind, r=4):
    """Confidence dot: filled = confirmed, half = one side's claim,
    open ring = unconfirmed."""
    if kind == "full":
        draw.ellipse([x, y, x + 2 * r, y + 2 * r], fill=INK)
    elif kind == "half":
        draw.ellipse([x, y, x + 2 * r, y + 2 * r], outline=INK, width=1)
        draw.pieslice([x, y, x + 2 * r, y + 2 * r], 90, 270, fill=INK)
    else:
        draw.ellipse([x, y, x + 2 * r, y + 2 * r], outline=RED, width=1)


def draw_gulf_panel(draw, x, y, w, h):
    """Small drawn picture for the lead: a tanker at sea under a
    red arc, all vector shapes -- no photo, no copied art."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    draw.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(28, 52, 92))
    draw.ellipse([x + w - 52, y + 8, x + w - 22, y + 38], fill=GOLD)
    for t in range(0, 101, 4):
        ax = x + int(w * 0.06 + t / 100.0 * w * 0.55)
        ay = y + int(h * 0.55 - 26 * (1 - ((t - 50) / 50.0) ** 2))
        draw.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=RED)
    hy = y + int(h * 0.62)
    draw.polygon([(x + 18, hy), (x + w - 30, hy), (x + w - 52, hy + 18),
                  (x + 34, hy + 18)], fill=(12, 12, 14))
    draw.rectangle([x + 30, hy - 20, x + w - 70, hy], fill=(38, 44, 54))
    for i, cx in enumerate(range(x + 34, x + w - 74, 22)):
        draw.rectangle([cx, hy - 18 + (i % 2) * 4, cx + 18, hy - 4],
                       fill=(200, 70, 60) if i % 3 == 0 else (90, 120, 150))
    for wx in range(x + 6, x + w - 6, 34):
        draw.arc([wx, y + h - 14, wx + 30, y + h - 2], 200, 340,
                 fill=(150, 180, 220), width=2)
    draw.text((x + 8, y + h - 12), "THE GULF, 23 NOV",
              font=font(SANS_B, 8), fill=(220, 220, 210))


def measure_briefs(draw, briefs, head_size):
    """Measure the brief columns; returns (height, columns, col_w)."""
    f_head = font(SERIF_B, head_size)
    col_w = (W - 2 * MARGIN - 2 * GUTTER) // 3
    blocks = []
    cur_sec = None
    for sec, head, src, conf in briefs:
        if sec != cur_sec:
            blocks.append(("head", sec, 19))
            cur_sec = sec
        lines = wrap(draw, head, f_head, col_w - 4)
        h = len(lines) * line_h(f_head) + 12
        blocks.append(("brief", (sec, head, src, conf, lines), h))
    total = sum(b[2] for b in blocks)
    target = total / 3.0
    cols, cur, cur_h, cur_sec = [], [], 0, None
    for kind, payload, h in blocks:
        if kind == "head":
            cur_sec = payload
        if cur and cur_h + h > target + 20 and len(cols) < 2:
            cols.append(cur)
            cur, cur_h = [], 0
            if kind == "brief" and payload[0] != cur_sec:
                pass
            if kind == "brief":
                cur.append(("head", payload[0] + " (cont.)", 19))
                cur_h += 19
        cur.append((kind, payload, h))
        cur_h += h
    cols.append(cur)
    brief_h = max(sum(b[2] for b in c) for c in cols)
    return brief_h, cols, col_w


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))

    briefs = list(BRIEFS)
    head_size = 12
    mast_h, lead_h, second_h, time_h, mkt_h, foot_h = 96, 152, 92, 78, 20, 48
    while True:
        brief_h, cols, col_w = measure_briefs(probe, briefs, head_size)
        gaps = 6 + 8 + 8 + 2 + 2  # matches the gaps actually drawn below
        used = MARGIN + mast_h + lead_h + second_h + brief_h + time_h + mkt_h + foot_h + gaps
        if used <= H - 14 or (head_size <= 10 and not briefs):
            break
        if head_size > 10:
            head_size -= 1
        else:
            briefs.pop()  # shed the lowest-priority brief
    n_stories = 3 + len(briefs)
    all_secs = {"MIDDLE EAST"}
    all_secs.update(s for s, _, _, _ in briefs)
    regions = len(all_secs)

    y = MARGIN
    # ---------- masthead ----------
    f_name = font(SERIF_B, 42)
    name = "THE WORLD IN ONE PAGE"
    nw = draw.textlength(name, font=f_name)
    draw.text(((W - nw) / 2, y), name, font=f_name, fill=INK)
    draw.rectangle([MARGIN, y + 52, W - MARGIN, y + 54], fill=INK)
    f_date = font(SANS_B, 14)
    date = "MONDAY  -  23 NOVEMBER 2026"
    dw = draw.textlength(date, font=f_date)
    draw.text(((W - dw) / 2, y + 58), date, font=f_date, fill=RED)
    f_strap = font(SERIF_I, 13)
    strap = ("%d sourced stories  -  %d regions  -  a UTC timeline  -  a date check"
             % (n_stories, regions))
    sw = draw.textlength(strap, font=f_strap)
    draw.text(((W - sw) / 2, y + 76), strap, font=f_strap, fill=GREY)
    y += mast_h + 6

    # ---------- lead ----------
    draw.rectangle([MARGIN, y, W - MARGIN, y + lead_h], outline=RULE, width=1)
    draw.rectangle([MARGIN, y, W - MARGIN, y + 20], fill=RED)
    draw.text((MARGIN + 10, y + 3), LEAD["kicker"], font=font(SANS_B, 11), fill=(255, 255, 255))
    ly = y + 28
    f_lead = font(SERIF_B, 25)
    for ln in wrap(draw, LEAD["head"], f_lead, W - 2 * MARGIN - 20):
        draw.text((MARGIN + 10, ly), ln, font=f_lead, fill=INK)
        ly += line_h(f_lead)
    deck_w = W - 2 * MARGIN - 20 - 300
    f_deck = font(SERIF, 13)
    dy = ly + 4
    for ln in wrap(draw, LEAD["deck"], f_deck, deck_w):
        draw.text((MARGIN + 10, dy), ln, font=f_deck, fill=INK)
        dy += line_h(f_deck)
    draw_gulf_panel(draw, W - MARGIN - 10 - 290, ly + 2, 290, 74)
    draw_conf(draw, MARGIN + 10, y + lead_h - 15, LEAD["conf"])
    draw.text((MARGIN + 24, y + lead_h - 17), LEAD["src"], font=font(SANS, 10), fill=GREY)
    y += lead_h + 8

    # ---------- secondary row ----------
    sec_w = (W - 2 * MARGIN - GUTTER) // 2
    for i, s in enumerate(SECOND):
        x0 = MARGIN + i * (sec_w + GUTTER)
        draw.rectangle([x0, y, x0 + sec_w, y + second_h], outline=RULE, width=1)
        draw.text((x0 + 8, y + 5), s["kicker"], font=font(SANS_B, 10), fill=RED)
        f_sh = font(SERIF_B, 16)
        sy = y + 22
        for ln in wrap(draw, s["head"], f_sh, sec_w - 16):
            draw.text((x0 + 8, sy), ln, font=f_sh, fill=INK)
            sy += line_h(f_sh)
        f_sd = font(SERIF, 11)
        for ln in wrap(draw, s["deck"], f_sd, sec_w - 16):
            draw.text((x0 + 8, sy), ln, font=f_sd, fill=INK)
            sy += line_h(f_sd)
        draw_conf(draw, x0 + 8, y + second_h - 13, s["conf"], r=3)
        draw.text((x0 + 20, y + second_h - 15), s["src"], font=font(SANS, 9), fill=GREY)
    y += second_h + 8

    # ---------- briefs, three columns ----------
    f_head = font(SERIF_B, head_size)
    f_src = font(SANS, 9)
    col_x = [MARGIN + i * (col_w + GUTTER) for i in range(3)]
    for ci, col in enumerate(cols):
        cy = y
        for kind, payload, h in col:
            if kind == "head":
                draw.text((col_x[ci], cy), payload, font=font(SANS_B, 11), fill=RED)
                draw.rectangle([col_x[ci], cy + 14, col_x[ci] + col_w, cy + 15], fill=RULE)
                cy += 19
            else:
                sec, head, src, conf, lines = payload
                for ln in lines:
                    draw.text((col_x[ci], cy), ln, font=f_head, fill=INK)
                    cy += line_h(f_head)
                draw_conf(draw, col_x[ci], cy + 3, conf, r=3)
                draw.text((col_x[ci] + 12, cy + 1), src, font=f_src, fill=GREY)
                cy += 12
    y += brief_h + 2

    # ---------- UTC timeline ----------
    draw.rectangle([MARGIN, y, W - MARGIN, y + time_h], outline=RULE, width=1)
    draw.text((MARGIN + 8, y + 4), "THE DAY IN UTC", font=font(SANS_B, 11), fill=RED)
    tcol_w = (W - 2 * MARGIN - 16) // 3
    f_tt = font(SANS_B, 11)
    f_tx = font(SERIF, 11)
    for i, (t, txt) in enumerate(TIMELINE):
        tx0 = MARGIN + 8 + (i % 3) * tcol_w
        ty0 = y + 22 + (i // 3) * 28
        draw.text((tx0, ty0), t, font=f_tt, fill=RED)
        for j, ln in enumerate(wrap(draw, txt, f_tx, tcol_w - 52)):
            draw.text((tx0 + 46, ty0 + j * 13), ln, font=f_tx, fill=INK)
    y += time_h + 2

    # ---------- markets strip ----------
    f_mk = font(SANS_B, 11)
    mw = draw.textlength(MARKETS, font=f_mk)
    draw.text(((W - mw) / 2, y), MARKETS, font=f_mk, fill=INK)
    y += mkt_h

    # ---------- date check + footer ----------
    draw.rectangle([MARGIN, y, W - MARGIN, y + foot_h], outline=RED, width=1)
    f_dc = font(SERIF_B, 11)
    dc1 = ("DATE CHECK  --  Monday 23 November 2026 was a Monday. Every story here "
           "is an event of, or first reported on, 23 November 2026.")
    dc2 = "Each story is named to its source on the page.  Confidence:  "
    draw.text((MARGIN + 8, y + 5), dc1, font=f_dc, fill=INK)
    draw.text((MARGIN + 8, y + 23), dc2, font=f_dc, fill=INK)
    lx = MARGIN + 8 + draw.textlength(dc2, font=f_dc)
    draw_conf(draw, lx, y + 27, "full", r=3)
    draw.text((lx + 12, y + 23), "confirmed", font=font(SANS, 10), fill=INK)
    lx += 12 + draw.textlength("confirmed", font=font(SANS, 10)) + 10
    draw_conf(draw, lx, y + 27, "half", r=3)
    draw.text((lx + 12, y + 23), "one side's claim / single source", font=font(SANS, 10), fill=INK)
    lx += 12 + draw.textlength("one side's claim / single source", font=font(SANS, 10)) + 10
    draw_conf(draw, lx, y + 27, "open", r=3)
    draw.text((lx + 12, y + 23), "unconfirmed", font=font(SANS, 10), fill=INK)
    draw.text((MARGIN + 8, y + 35),
              "Compiled from live reporting on 23 November 2026. Weekend stories are those still developing on Monday.",
              font=font(SERIF_I, 10), fill=GREY)
    y += foot_h

    img.save(out_path, "PNG", optimize=True)
    print("stories=%d regions=%d brief_head_size=%d briefs=%d used_y=%d"
          % (n_stories, regions, head_size, len(briefs), y))
    return n_stories, regions


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
