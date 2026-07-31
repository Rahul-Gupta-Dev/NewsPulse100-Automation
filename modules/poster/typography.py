from PIL import ImageDraw
from modules.poster.text import get_font, wrap_text, draw_stroke_text


def draw_headline(draw, headline, theme):

    font = get_font(78, True)

    lines = wrap_text(
        headline,
        font,
        900,
        draw
    )

    y = 930

    for i, line in enumerate(lines):

        color = theme["headline"]

        if i == len(lines) - 1:
            color = theme["secondary"]

        w = draw.textlength(line, font=font)
        x = (1080 - w) / 2

        draw_stroke_text(
            draw,
            (x, y),
            line,
            font,
            fill=color,
            stroke_fill="black",
            stroke=4
        )

        y += 90

    draw.rounded_rectangle(
        (180, y+10, 900, y+16),
        radius=3,
        fill=theme["primary"]
    )

    return y + 35


def draw_summary(draw, summary, start_y, theme):

    font = get_font(36)

    lines = wrap_text(
        summary,
        font,
        920,
        draw
    )[:3]

    y = start_y

    for line in lines:

        w = draw.textlength(line, font=font)
        x = (1080 - w) / 2

        draw.text(
            (x, y),
            line,
            font=font,
            fill=theme["summary"]
        )

        y += 45