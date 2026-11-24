#!/usr/bin/env python3
"""The World in One Day - Tuesday 24 November 2026.

Broadsheet front page, drawn from scratch with Pillow.
Deterministic: no random, no clock, no network.
Output: entry.png, 1024x1024 RGB, < 1 MiB.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (178, 34, 24)
GREEN = (31, 120, 60)
BLUE = (31, 78, 121)
GREY = (90, 90, 90)
RULE = (60, 60, 60)
CHART_BG = (255, 255, 255)
GRID = (210, 210, 210)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured width. Returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw a wrapped paragraph. Returns y after last line."""
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, x1, y, width=1, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 28                      # side margin
    RX = W - MX                  # right edge
    CW = RX - MX                 # content width

    # ---------- top dateline strip ----------
    f_date = font(SERIF_B, 30)
    f_small = font(SANS_B, 13)
    d.text((MX, 12), "No. 328", font=f_small, fill=INK)
    d.text((RX - d.textlength("PRICE: FREE", font=f_small), 12),
           "PRICE: FREE", font=f_small, fill=INK)
    date_txt = "TUESDAY 24 NOVEMBER 2026"
    d.text(((W - d.textlength(date_txt, font=f_date)) / 2, 8),
           date_txt, font=f_date, fill=RED)
    rule(d, MX, RX, 46, 2)
    rule(d, MX, RX, 50, 1)

    # ---------- masthead ----------
    f_mast = font(SERIF_B, 60)
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 56),
           mast, font=f_mast, fill=INK)
    f_tag = font(SERIF_I, 17)
    tag = "Every story that mattered, on a single page"
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, 120),
           tag, font=f_tag, fill=GREY)
    rule(d, MX, RX, 146, 3)
    rule(d, MX, RX, 150, 1)

    # ---------- lead headline ----------
    y = 156
    f_lead = font(SERIF_B, 68)
    lead = "HUANG IS BACK"
    d.text(((W - d.textlength(lead, font=f_lead)) / 2, y),
           lead, font=f_lead, fill=INK)
    y += 78
    f_deck = font(SERIF_B, 20)
    deck = ("Huang returns as Nvidia CEO \u2014 shares jump 33% as Trump "
            "says: \u201cI made the deal\u201d")
    for ln in wrap(d, deck, f_deck, CW):
        d.text(((W - d.textlength(ln, font=f_deck)) / 2, y),
               ln, font=f_deck, fill=INK)
        y += 25
    y += 4
    rule(d, MX, RX, y, 1)
    y += 10

    # ---------- lead body (left) + share-price chart (right) ----------
    lead_top = y
    chart_w = 372
    chart_x = RX - chart_w
    body_w = chart_x - 18 - MX
    f_body = font(SERIF, 16)
    f_kick = font(SANS_B, 13)
    f_quote = font(SERIF_I, 16)

    d.text((MX, lead_top), "SANTA CLARA, CALIFORNIA \u2014 ANNOUNCED MONDAY",
           font=f_kick, fill=RED)
    by = lead_top + 20
    by = para(d, MX, by,
              "Nvidia\u2019s board voted unanimously on Monday to reinstate "
              "co-founder Jensen Huang as president and chief executive, "
              "effective immediately \u2014 11 days after he resigned over "
              "revelations of extramarital affairs, including one with a woman "
              "US officials suspect of spying for China.",
              f_body, body_w, 19)
    by += 6
    by = para(d, MX, by,
              "Shares jumped about 33% on Monday, adding roughly $1 trillion "
              "in market value, and the Nasdaq rose 7%. The board said it was "
              "satisfied with Huang\u2019s candour and, after input from senior "
              "US officials, saw no national security risk.",
              f_body, body_w, 19)
    by += 6
    by = para(d, MX, by,
              "\u201cI spoke to them\u2026 And I convinced them. I made the "
              "deal,\u201d President Donald Trump told CNBC on Monday.",
              f_quote, body_w, 19)
    by += 6
    by = para(d, MX, by,
              "The questions have not gone away: Huang is due to testify "
              "publicly before the Senate Banking Committee on 3 December "
              "about export controls, after closed-door House interviews on "
              "1 December. Nvidia\u2019s own investigation continues.",
              f_body, body_w, 19)

    # chart box
    d.rectangle([chart_x, lead_top, RX, lead_top + 232], outline=INK, width=2)
    d.text((chart_x + 10, lead_top + 8), "NVIDIA SHARES, $ \u2014 THE 33% BOUNCE",
           font=font(SANS_B, 16), fill=RED)
    d.text((chart_x + 10, lead_top + 30),
           "Nvidia share price, $ \u2014 closing prices",
           font=font(SANS, 12), fill=GREY)
    # chart area: 29 Oct $213.66 -> 20 Nov $125.53 -> 23 Nov $165.57
    cx0, cy0 = chart_x + 42, lead_top + 52
    cw, ch = chart_w - 62, 104
    d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=CHART_BG,
                outline=INK, width=1)
    p_lo, p_hi = 100.0, 230.0

    def py_of(price):
        return cy0 + ch - (price - p_lo) / (p_hi - p_lo) * ch

    for gv in (100, 150, 200):
        gy = py_of(gv)
        d.line([(cx0, gy), (cx0 + cw, gy)], fill=GRID, width=1)
        lab = str(gv)
        d.text((cx0 - 34, gy - 6), lab, font=font(SANS, 11), fill=GREY)
    pts = [(cx0 + 26, py_of(213.66), "29 Oct", "$213.66", True),
           (cx0 + cw // 2, py_of(125.53), "20 Nov", "$125.53", False),
           (cx0 + cw - 26, py_of(165.57), "23 Nov", "$165.57", True)]
    d.line([pts[0][:2], pts[1][:2]], fill=RED, width=3)
    d.line([pts[1][:2], pts[2][:2]], fill=GREEN, width=3)
    for (px, py_, dl, vl, above) in pts:
        d.ellipse([px - 4, py_ - 4, px + 4, py_ + 4], fill=INK, outline=INK)
        f_v = font(SANS_B, 12)
        d.text((px - d.textlength(vl, font=f_v) / 2,
                py_ - 18 if above else py_ + 8), vl, font=f_v, fill=INK)
        f_d = font(SANS, 11)
        d.text((px - d.textlength(dl, font=f_d) / 2, cy0 + ch + 4),
               dl, font=f_d, fill=GREY)
    d.text((cx0 + cw - 62, py_of(165.57) - 34), "+33% Mon",
           font=font(SANS_B, 12), fill=GREEN)
    cap_y = lead_top + 178
    cap_y = para(d, chart_x + 10, cap_y,
                 "Shares fell more than 40% after the scandal broke in late "
                 "October. Chip stocks rallied too: SK hynix\u2019s US-traded "
                 "shares rose 20% on Tuesday.",
                 font(SERIF, 13), chart_w - 20, 15)
    lead_bottom = max(by, lead_top + 232) + 8
    rule(d, MX, RX, lead_bottom, 2)

    # ---------- six story panels, 3 x 2 ----------
    py = lead_bottom + 8
    panels = [
        ("LIBYA", "Kyiv says it sank Russian warship",
         "President Zelenskyy confirmed on Monday that seven Ukrainian "
         "naval drones sank the Russian corvette Merkury off Benghazi on "
         "Sunday; a Ka-27 helicopter was destroyed and the cargo ship "
         "MV Angara hit."),
        ("EUROPE", "EU unveils 22nd sanctions package",
         "The European Commission proposed on Monday to cut about 60 "
         "Russian banks from SWIFT, list 70+ more shadow-fleet ships and "
         "crack down on crypto \u2014 and ban the Russian flag at EU "
         "sports events. All 27 states must agree."),
        ("INDIA\u2013NEPAL", "$1.62bn lifeline for flood-hit Nepal",
         "India announced on Monday a $1.62bn package \u2014 a $377m grant "
         "and a $1.24bn credit line \u2014 after talks with PM Balendra "
         "Shah. August floods killed about 1,500 people; 5,200 are "
         "missing."),
        ("GAZA", "Strike kills 3 in Khan Younis",
         "An Israeli airstrike killed at least three Palestinians on "
         "Tuesday near a police outpost in Khan Younis, medics said; "
         "five were wounded. Australia, Canada, Italy and the UK urged "
         "aid access to flooded Gaza."),
        ("SPORT", "2031 Women\u2019s World Cup to US & Mexico",
         "FIFA confirmed the 2031 Women\u2019s World Cup will be hosted by "
         "the US, Mexico, Costa Rica and Jamaica; the 2035 edition goes "
         "to the United Kingdom."),
        ("GULF", "Iran claims US drone downed",
         "Iran\u2019s army said on Tuesday it shot down a US drone over "
         "the Gulf. The US Treasury sanctioned more than two dozen "
         "Iranian exchange houses and front firms under \u201cOperation "
         "Economic Outcast\u201d."),
    ]
    gap = 12
    pw = (CW - 2 * gap) // 3
    ph = 162
    f_pk = font(SANS_B, 13)
    f_ph = font(SERIF_B, 19)
    f_pb = font(SERIF, 14)
    for i, (kick, head, body) in enumerate(panels):
        col, row = i % 3, i // 3
        x = MX + col * (pw + gap)
        yy = py + row * (ph + gap)
        d.rectangle([x, yy, x + pw, yy + ph], outline=INK, width=1)
        d.text((x + 10, yy + 8), kick, font=f_pk, fill=RED)
        hy = yy + 28
        for ln in wrap(d, head, f_ph, pw - 20):
            d.text((x + 10, hy), ln, font=f_ph, fill=INK)
            hy += 22
        hy += 2
        byy2 = para(d, x + 10, hy, body, f_pb, pw - 20, 17)
        assert byy2 <= yy + ph - 4, f"panel {kick} overflows: {byy2} > {yy + ph}"
    panels_bottom = py + 2 * ph + gap

    # ---------- In Brief strip ----------
    iy = panels_bottom + 10
    rule(d, MX, RX, iy, 2)
    iy += 6
    d.text((MX, iy), "IN BRIEF", font=font(SANS_B, 15), fill=RED)
    iy += 20
    brief = [
        ("UKRAINE", "Fresh Russian strikes reported in the Kyiv region."),
        ("SOUTH SUDAN", "24 killed, including seven children, in a strike."),
        ("UNITED NATIONS", "Talks on lethal AI weapons end without a pact."),
        ("MYANMAR", "ICJ ruled Thursday: Myanmar committed genocide."),
        ("CRICKET", "India\u2013New Zealand Wellington Test ends in a draw."),
        ("BALTIC", "Crew of Russian ship Sparta II evacuated after drone hit."),
        ("HORMUZ", "Three tankers hit sea mines and caught fire, Iran says."),
        ("CYPRUS", "Two Russian diplomats told to leave the island."),
        ("KOREA", "Seoul says North Korean aircraft violated its airspace."),
        ("IOWA", "Trump halts Army plan to detonate bomb chemicals."),
    ]
    f_bb = font(SANS, 12)
    col_w = (CW - 20) // 2
    left_items = brief[:5]
    right_items = brief[5:]
    byy3 = iy
    for col_items, cx in ((left_items, MX), (right_items, MX + col_w + 20)):
        cy = iy
        for kick, txt in col_items:
            line = kick + ": " + txt
            for ln in wrap(d, line, f_bb, col_w):
                d.text((cx, cy), ln, font=f_bb, fill=INK)
                cy += 13
            cy += 1
        byy3 = max(byy3, cy)
    assert byy3 <= H - 14, f"in-brief overflows: {byy3}"
    rule(d, MX, RX, H - 12, 1)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
