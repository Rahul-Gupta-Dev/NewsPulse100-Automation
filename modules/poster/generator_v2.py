from PIL import (
    Image,
    ImageDraw,
    ImageFont,
    ImageEnhance
)

import os

from datetime import datetime

from modules.poster.effects import (
    add_bottom_gradient
)

from modules.poster.text import (
    wrap_text,
    draw_stroke_text,
    get_hindi_font,
    get_english_font
)


# -----------------------------
# CONFIG
# -----------------------------

WIDTH = 1080
HEIGHT = 1350

LEFT = 60
RIGHT = 60

HEADER_Y = 35

FOOTER_HEIGHT = 95

LOGO_PATH = "assets/logo.png"
BREAKING_PATH = "assets/breaking.png"

WHITE = (255,255,255)
YELLOW = (255,210,0)
BLACK = (0,0,0)
RED = (225,0,0)
LIGHT = (235,235,235)


# -----------------------------
# IMAGE COVER
# -----------------------------

def cover_resize(img):

    iw, ih = img.size

    scale = max(
        WIDTH / iw,
        HEIGHT / ih
    )

    nw = int(iw * scale)
    nh = int(ih * scale)

    img = img.resize(
        (nw, nh),
        Image.LANCZOS
    )

    left = (nw - WIDTH) // 2
    top = (nh - HEIGHT) // 2

    return img.crop(
        (
            left,
            top,
            left + WIDTH,
            top + HEIGHT
        )
    )


# -----------------------------
# IMAGE LOOK
# -----------------------------

def enhance(img):

    img = ImageEnhance.Contrast(
        img
    ).enhance(1.18)

    img = ImageEnhance.Color(
        img
    ).enhance(1.08)

    img = ImageEnhance.Sharpness(
        img
    ).enhance(1.12)

    return img


# -----------------------------
# HEADER
# -----------------------------

def draw_header(canvas):

    if os.path.exists(LOGO_PATH):

        logo = Image.open(LOGO_PATH)

        logo = logo.convert("RGBA")

        logo.thumbnail((190,190))

        canvas.paste(
            logo,
            (20,20),
            logo
        )

    else:

        draw = ImageDraw.Draw(canvas)

        font = ImageFont.truetype(
    "fonts/DejaVuSans-Bold.ttf",
    34
)

        draw.rounded_rectangle(
            (
                30,
                30,
                320,
                90
            ),
            radius=8,
            fill=RED
        )

        draw.text(
            (
                48,
                42
            ),
            "NewsPulse100",
            font=font,
            fill=WHITE
        )

    if os.path.exists(BREAKING_PATH):

        badge = Image.open(
            BREAKING_PATH
        ).convert("RGBA")

        badge.thumbnail((240,90))

        x = WIDTH - badge.width - 35

        canvas.paste(
            badge,
            (x,25),
            badge
        )


# -----------------------------
# FOOTER
# -----------------------------

def draw_footer(
    canvas,
    category
):

    draw = ImageDraw.Draw(canvas)

    y = HEIGHT - FOOTER_HEIGHT

    draw.rectangle(
        (
            0,
            y,
            WIDTH,
            HEIGHT
        ),
        fill=(12,12,12)
    )

    font = ImageFont.truetype(
    "fonts/DejaVuSans-Bold.ttf",
    34
)

    date = datetime.now().strftime(
        "%d %b %Y"
    ).upper()

    draw.text(
        (
            40,
            y+30
        ),
        date,
        font=font,
        fill=WHITE
    )

    tw = draw.textlength(
        category.upper(),
        font=font
    )

    draw.text(
        (
            WIDTH-tw-40,
            y+30
        ),
        category.upper(),
        font=font,
        fill=WHITE
    )

    draw.line(
        (
            WIDTH//2,
            y+18,
            WIDTH//2,
            HEIGHT-18
        ),
        fill=(70,70,70),
        width=2
    )


# -----------------------------
# BACKGROUND
# -----------------------------

def prepare_background(
    image_path
):

    img = Image.open(
        image_path
    ).convert("RGB")

    img = cover_resize(img)

    img = enhance(img)

    img = add_bottom_gradient(img)

    return img

import re

# -----------------------------
# MIXED TEXT
# -----------------------------

def draw_mixed_text(draw, position, text, hindi_font, english_font,
                    fill, stroke_fill=None, stroke=0):

    x, y = position

    parts = re.findall(r"[A-Za-z0-9#@._+-]+|[^A-Za-z0-9#@._+-]+", text)

    for part in parts:

        font = english_font if re.search(r"[A-Za-z0-9]", part) else hindi_font

        if stroke > 0:
            for dx in range(-stroke, stroke + 1):
                for dy in range(-stroke, stroke + 1):
                    if dx == 0 and dy == 0:
                        continue
                    draw.text(
                        (x + dx, y + dy),
                        part,
                        font=font,
                        fill=stroke_fill
                    )

        draw.text(
            (x, y),
            part,
            font=font,
            fill=fill
        )

        x += draw.textlength(part, font=font)

      

# -----------------------------
# HEADLINE
# -----------------------------

def draw_headline(canvas, headline):

    draw = ImageDraw.Draw(canvas)

    parts = wrap_text(
    headline,
    get_hindi_font(82, True),
    WIDTH - 120,
    draw
)

    if len(parts) == 1:
        white_lines = parts
        yellow_lines = []
    else:
        white_lines = parts[:-1]
        yellow_lines = [parts[-1]]

    y = 770

    white_font = get_hindi_font(82, True)
    yellow_font = get_hindi_font(88, True)
    

    for line in white_lines:

        w = draw.textlength(
            line,
            font=white_font
        )

        x = (WIDTH - w) / 2

        draw_mixed_text(
            draw,
            (x, y),
            line,
            get_hindi_font(82, True),
            get_english_font(82, True),
            fill=WHITE,
            stroke_fill=BLACK,
            stroke=4
        )

        y += 90

    for line in yellow_lines:

        w = draw.textlength(
            line,
            font=yellow_font
        )

        x = (WIDTH - w) / 2

        draw_mixed_text(
    draw,
    (x, y),
    line,
    get_hindi_font(88, True),
    get_english_font(88, True),
    fill=YELLOW,
    stroke_fill=BLACK,
    stroke=4
        )

        y += 100

    draw.rounded_rectangle(
        (
            120,
            y + 10,
            WIDTH - 120,
            y + 16
        ),
        radius=5,
        fill=RED
    )

    return y + 40


# -----------------------------
# SUMMARY
# -----------------------------

def draw_summary(
    canvas,
    summary,
    start_y
):

    draw = ImageDraw.Draw(canvas)

    font = get_hindi_font(36)

    lines = wrap_text(
        summary,
        font,
        WIDTH - 140,
        draw
    )[:3]

    y = start_y

    for line in lines:

        w = draw.textlength(
            line,
            font=font
        )

        x = (WIDTH - w) / 2

        draw_mixed_text(
    draw,
    (x, y),
    line,
    get_hindi_font(36),
    get_english_font(36),
    fill=LIGHT,
    stroke_fill=BLACK,
    stroke=2
)

        y += 46


# -----------------------------
# GENERATE
# -----------------------------

def generate_poster(
    headline,
    summary,
    category,
    image_path="output/news_image.jpg",
    output_path="output/poster.png"
):

    bg = prepare_background(
        image_path
    )

    draw_header(bg)

    y = draw_headline(
        bg,
        headline
    )

    draw_summary(
        bg,
        summary,
        y + 20
    )

    draw_footer(
        bg,
        category
    )

    bg.save(
        output_path,
        quality=95
    )

    print(
        "✅ Poster Saved:",
        output_path
    )
    return output_path