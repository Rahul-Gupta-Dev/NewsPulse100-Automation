from PIL import ImageDraw

from modules.poster.theme import get_theme
from modules.poster.background import prepare_background
from modules.poster.widgets import (
    draw_logo,
    draw_badge,
    draw_footer
)
from modules.poster.typography import (
    draw_headline,
    draw_summary
)

from datetime import datetime


def render_poster(
    image_path,
    headline,
    summary,
    category
):

    theme = get_theme(category)

    canvas = prepare_background(image_path)

    draw = ImageDraw.Draw(canvas)

    draw_logo(draw, theme)

    draw_badge(draw, theme)

    y = draw_headline(
        draw,
        headline,
        theme
    )

    draw_summary(
    draw,
    summary,
    y + 45,
    theme
)

    draw_footer(
        draw,
        theme,
        datetime.now().strftime("%d %b %Y").upper(),
        category
    )

    return canvas