from PIL import ImageDraw, ImageFont
import textwrap


def get_font(size, bold=False):
    if bold:
        return ImageFont.truetype(
            "fonts/NotoSansDevanagari-Bold.ttf",
            size
        )

    return ImageFont.truetype(
        "fonts/NotoSansDevanagari-Regular.ttf",
        size
    )


def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = current + (" " if current else "") + word

        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_stroke_text(draw, pos, text, font,
                     fill, stroke_fill, stroke=3):

    x, y = pos

    for dx in range(-stroke, stroke + 1):
        for dy in range(-stroke, stroke + 1):
            if dx == 0 and dy == 0:
                continue

            draw.text(
                (x + dx, y + dy),
                text,
                font=font,
                fill=stroke_fill
            )

    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill
    )


def fit_font(text, draw, max_width,
             start_size=90,
             min_size=40):

    size = start_size

    while size >= min_size:

        font = get_font(size, True)

        if draw.textlength(text, font=font) <= max_width:
            return font

        size -= 2

    return get_font(min_size, True)