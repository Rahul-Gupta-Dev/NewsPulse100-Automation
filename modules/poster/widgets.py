from PIL import ImageFont
from PIL import ImageDraw
from modules.poster.text import get_font


def draw_logo(draw, theme):

    from PIL import ImageFont
    font = ImageFont.truetype(
    "fonts/DejaVuSans-Bold.ttf",
    34
)

    draw.rounded_rectangle(
        (30, 30, 340, 90),
        radius=12,
        fill=theme["primary"]
    )

    draw.text(
        (50, 45),
        "NEWSPULSE100",
        font=font,
        fill="white"
    )


def draw_badge(draw, theme):

    font = ImageFont.truetype(
    "fonts/DejaVuSans-Bold.ttf",
    28
)

    draw.rounded_rectangle(
        (760, 30, 1050, 90),
        radius=12,
        fill=theme["primary"]
    )

    draw.text(
        (790, 45),
        "BREAKING NEWS",
        font=font,
        fill="white"
    )


def draw_footer(draw, theme, date, category):

    font = ImageFont.truetype(
    "fonts/DejaVuSans-Bold.ttf",
    28
)

    draw.rectangle(
        (0, 1260, 1080, 1350),
        fill=theme["footer"]
    )

    draw.text(
        (40, 1295),
        date,
        font=font,
        fill="white"
    )

    w = draw.textlength(
        category.upper(),
        font=font
    )

    draw.text(
        (1080-w-40, 1295),
        category.upper(),
        font=font,
        fill="white"
    )