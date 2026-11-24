#!/usr/bin/env python3
"""The World in One Day — Tuesday 24 November 2026.

A broadsheet front page drawn from scratch with Pillow: a big masthead,
one dominant lead story with a schematic Nvidia share-price chart, six
story panels and an In Brief strip. Everything is fixed geometry and
fixed fonts, so the output is deterministic — no network, no clock,
no randomness.

Run:  python3 draw.py        # writes entry.png next to this file
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette

PAPER = (247, 243, 234)   # newsprint cream
INK = (26, 25, 22)        # near-black body ink
FAINT = (96, 91, 80)      # datelines, captions
RED = (139, 26, 26)       # kickers, chart line
HAIR = (178, 170, 152)    # thin panel dividers
CHART_GRID = (205, 198, 182)

PAGE = 1024
MARGIN = 40
RIGHT = PAGE - MARGIN

# ---------------------------------------------------------------- typefaces

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def typeface(path, size):
    """Load a TTF once; fall back to Pillow's built-in bitmap font."""
    key = (path, size)
    if key not in _cache:
        try:
            _cache[key] = ImageFont.truetype(path, size)
        except OSError:
            _cache[key] = ImageFont.load_default(size)
    return _cache[key]


def fit_lines(canvas, text, font, width):
    """Greedy word wrap; returns the list of lines that fit `width`."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if not current or canvas.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_paragraph(canvas, x, y, width, text, font, leading, color=INK):
    """Draw a wrapped paragraph; returns the y below its last line."""
    for line in fit_lines(canvas, text, font, width):
        canvas.text((x, y), line, font=font, fill=color)
        y += leading
    return y


def rule(canvas, y, weight, x0=MARGIN, x1=RIGHT, color=INK):
    canvas.rectangle([x0, y, x1, y + weight - 1], fill=color)


# ---------------------------------------------------------------- masthead

def paint_masthead(canvas):
    dateline = typeface(SANS_BOLD, 12)
    canvas.text((MARGIN, 30), "TUESDAY, 24 NOVEMBER 2026", font=dateline, fill=INK)
    tag = "No. 329  ·  FREE"
    canvas.text((RIGHT - canvas.textlength(tag, font=dateline), 30), tag,
                font=dateline, fill=FAINT)

    title = typeface(SERIF_BOLD, 56)
    name = "THE WORLD IN ONE DAY"
    canvas.text(((PAGE - canvas.textlength(name, font=title)) / 2, 46),
                name, font=title, fill=INK)

    rule(canvas, 104, 4)
    rule(canvas, 112, 1)


# ---------------------------------------------------------------- lead story

LEAD_BODY = [
    "Nvidia's board voted unanimously on Monday to reinstate co-founder "
    "Jensen Huang as president and chief executive — 11 days after he "
    "resigned over reports of extramarital affairs, including one with "
    "Alice Huang, a former Megaspeed executive whom US officials suspect "
    "of ties to Chinese intelligence. The board had ruled out his return "
    "on 18 November, then reversed itself.",
    "Shares jumped about 33% in Monday trading, closing near $165.57, up "
    "from Friday's $125.53 — adding roughly $1 trillion in market value "
    "— while the Nasdaq rose about 7%. President Trump told CNBC on "
    "Monday: \"I spoke to them... And I convinced them. I made the deal.\"",
    "Senate Banking Committee chair Tim Scott said Huang will testify "
    "publicly on 3 December about export controls. Nvidia's own "
    "investigation continues, and the company is appointing a Chief "
    "Compliance Officer. On Tuesday, SK hynix's US-traded shares rose 20%.",
]


def paint_share_chart(canvas, x0, y0, x1, y1):
    """Schematic Nvidia close: 29 Oct $213.66, 20 Nov $125.53, 23 Nov $165.57."""
    heading = typeface(SANS_BOLD, 12)
    caption = typeface(SERIF_ITALIC, 12)
    axis = typeface(SANS, 10)
    value = typeface(SANS_BOLD, 11)

    title = "NVIDIA SHARES — THE BOUNCE"
    canvas.text(((x0 + x1 - canvas.textlength(title, font=heading)) / 2, y0),
                title, font=heading, fill=INK)
    sub = "+33% ON MONDAY  ·  ABOUT +$1 TRILLION IN VALUE"
    canvas.text(((x0 + x1 - canvas.textlength(sub, font=axis)) / 2, y0 + 18),
                sub, font=axis, fill=RED)

    plot_x0, plot_x1 = x0 + 34, x1 - 8
    plot_y0, plot_y1 = y0 + 44, y1 - 34
    low, high = 100.0, 220.0

    def to_xy(px, price):
        return (px, plot_y1 - (price - low) / (high - low) * (plot_y1 - plot_y0))

    for level in (100, 140, 180, 220):
        gy = to_xy(0, level)[1]
        canvas.line([(plot_x0, gy), (plot_x1, gy)], fill=CHART_GRID, width=1)
        tag = f"${level}"
        canvas.text((plot_x0 - canvas.textlength(tag, font=axis) - 6, gy - 6),
                    tag, font=axis, fill=FAINT)

    points = [("29 Oct", 213.66), ("20 Nov", 125.53), ("23 Nov", 165.57)]
    xs = [plot_x0 + i * (plot_x1 - plot_x0) / 2 for i in range(3)]
    dots = [to_xy(x, price) for x, (_, price) in zip(xs, points)]
    canvas.line(dots, fill=RED, width=3, joint="curve")
    for idx, ((label, price), (dx, dy)) in enumerate(zip(points, dots)):
        canvas.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=RED)
        tag = f"${price:.2f}"
        # Value sits below the dot, except the last point where it goes above.
        label_y = dy - 24 if idx == len(points) - 1 else dy + 10
        canvas.text((dx - canvas.textlength(tag, font=value) / 2, label_y),
                    tag, font=value, fill=RED)
        canvas.text((dx - canvas.textlength(label, font=axis) / 2, plot_y1 + 6),
                    label, font=axis, fill=FAINT)

    canvas.text((dots[2][0] - 160, dots[2][1] - 30), "+31.5% on the day",
                font=value, fill=RED)
    canvas.text((x0, y1 - 16),
                "Shares had closed at $213.66 on 29 Oct, before the scandal broke.",
                font=caption, fill=FAINT)


def paint_lead(canvas):
    kicker = typeface(SANS_BOLD, 12)
    canvas.text((MARGIN, 122), "LEAD STORY  ·  ANNOUNCED MONDAY",
                font=kicker, fill=RED)

    headline = typeface(SERIF_BOLD, 58)
    canvas.text((MARGIN, 138), "HUANG IS BACK", font=headline, fill=INK)

    deck = typeface(SERIF_ITALIC, 20)
    canvas.text((MARGIN, 202),
                "Shares jump about 33% as the board reverses course — "
                "and Trump says: \"I made the deal.\"",
                font=deck, fill=INK)
    rule(canvas, 230, 1, color=HAIR)

    body = typeface(SERIF, 14)
    y = 242
    for paragraph in LEAD_BODY:
        y = paint_paragraph(canvas, MARGIN, y, 600, paragraph, body, 18)
        y += 8

    paint_share_chart(canvas, 664, 242, RIGHT, 442)
    rule(canvas, 452, 4)


# ---------------------------------------------------------------- story panels

PANELS = [
    (
        "LIBYA — CONFIRMED MONDAY",
        "Kyiv says it sank Russian warship",
        "Zelenskyy confirmed on Monday that seven Ukrainian naval drones "
        "sank the Russian corvette Merkury off Benghazi on Sunday. A Ka-27 "
        "helicopter aboard was destroyed and the cargo ship MV Angara was "
        "hit. The UN called for an independent investigation.",
    ),
    (
        "EUROPE — PROPOSED MONDAY",
        "EU proposes 22nd sanctions package",
        "Ursula von der Leyen presented the proposed 22nd package on "
        "Monday: about 60 Russian banks cut from SWIFT, a crypto crackdown "
        "and a new task force, 70+ more shadow-fleet ships listed, and a "
        "ban on the Russian flag at EU sports events. All 27 states must agree.",
    ),
    (
        "INDIA–NEPAL — ANNOUNCED MONDAY",
        "$1.62bn lifeline for flood-hit Nepal",
        "India announced on Monday a $1.62bn package for flood-hit Nepal — "
        "a $377m grant for reconstruction and a $1.24bn credit line for "
        "energy — after talks between PM Narendra Modi and Nepali PM "
        "Balendra Shah. The 26 Aug floods killed about 1,500 people; "
        "5,200 are missing.",
    ),
    (
        "GAZA — TUESDAY",
        "Strike kills 3 in Khan Younis",
        "An Israeli airstrike killed at least three Palestinians on Tuesday "
        "near a police outpost in Khan Younis, medics said; five were "
        "wounded. At least 1,600 Palestinians and five Israeli soldiers "
        "have died since the October 2025 ceasefire. Four nations urged aid "
        "access to flooded Gaza.",
    ),
    (
        "SPORT — TUESDAY",
        "2031 Women's World Cup to US & Mexico",
        "FIFA confirmed the 2031 Women's World Cup will be hosted by the "
        "United States, Mexico, Costa Rica and Jamaica; the 2035 edition "
        "goes to the United Kingdom.",
    ),
    (
        "GULF — TUESDAY",
        "Iran claims US drone downed; US sanctions widen",
        "Iran's army said on Tuesday it shot down a US drone — reported as "
        "a \"Lucas\" drone — over the Gulf. The US Treasury sanctioned more "
        "than two dozen Iranian exchange houses and front firms under "
        "\"Operation Economic Outcast\".",
    ),
]


def paint_panel(canvas, x, y, width, kicker, headline, body):
    kick = typeface(SANS_BOLD, 11)
    head = typeface(SERIF_BOLD, 18)
    text = typeface(SERIF, 13)

    canvas.text((x, y), kicker, font=kick, fill=RED)
    y += 18
    head_lines = fit_lines(canvas, headline, head, width)
    for line in head_lines:
        canvas.text((x, y), line, font=head, fill=INK)
        y += 21
    y += 5
    paint_paragraph(canvas, x, y, width, body, text, 16)


def paint_panels(canvas):
    col_w = 304
    xs = [MARGIN, 360, 680]
    ys = [464, 648]
    for row, y in enumerate(ys):
        for col, x in enumerate(xs):
            paint_panel(canvas, x, y, col_w, *PANELS[row * 3 + col])
    for divider_x in (348, 668):
        canvas.line([(divider_x, 464), (divider_x, 824)], fill=HAIR, width=1)
    canvas.line([(MARGIN, 640), (RIGHT, 640)], fill=HAIR, width=1)
    rule(canvas, 836, 4)


# ---------------------------------------------------------------- In Brief

BRIEF = [
    ("UKRAINE", "Fresh Russian drone and missile strikes hit the Kyiv region on Tuesday."),
    ("SOUTH SUDAN", "24 people, including seven children, killed in a strike."),
    ("UNITED NATIONS", "Talks on lethal autonomous weapons ended with no pact."),
    ("MYANMAR", "The ICJ ruled on Thursday that Myanmar committed genocide against the Rohingya (9–6), the first such finding against a state."),
    ("CRICKET", "India v New Zealand first Test at Wellington ended in a draw."),
    ("BALTIC", "Crew of the Russian cargo ship Sparta II evacuated after a drone hit."),
    ("HORMUZ", "Three oil tankers hit sea mines and caught fire in the Strait of Hormuz, Iran's Revolutionary Guard says."),
    ("CYPRUS", "Two Russian diplomats had to leave the island."),
    ("KOREA", "Suspected North Korean aircraft violated South Korean airspace."),
    ("IOWA", "Trump ordered the Army not to detonate bomb chemicals without court approval."),
]


def paint_brief(canvas):
    heading = typeface(SANS_BOLD, 15)
    canvas.text((MARGIN, 846), "IN BRIEF", font=heading, fill=INK)
    rule(canvas, 870, 1, color=HAIR)

    label_font = typeface(SERIF_BOLD, 12)
    item_font = typeface(SERIF, 12)
    for col, x in enumerate((MARGIN, 524)):
        y = 878
        for label, text in BRIEF[col * 5:(col + 1) * 5]:
            full = f"{label} — {text}"
            for line in fit_lines(canvas, full, item_font, 460):
                canvas.text((x, y), line, font=item_font, fill=INK)
                y += 15
            y += 6


# ---------------------------------------------------------------- assemble

def build_page():
    page = Image.new("RGB", (PAGE, PAGE), PAPER)
    canvas = ImageDraw.Draw(page)
    canvas.rectangle([16, 16, PAGE - 17, PAGE - 17], outline=INK, width=2)
    paint_masthead(canvas)
    paint_lead(canvas)
    paint_panels(canvas)
    paint_brief(canvas)
    return page


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    build_page().save(os.path.join(here, "entry.png"), format="PNG")
    print("entry.png written")
