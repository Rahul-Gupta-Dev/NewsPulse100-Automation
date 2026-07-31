from PIL import Image, ImageDraw


def paste_logo(canvas, logo_path):
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((280, 90))
        canvas.paste(logo, (30, 30), logo)
    except:
        pass


def paste_breaking(canvas, badge_path):
    try:
        badge = Image.open(badge_path).convert("RGBA")
        badge.thumbnail((250, 90))
        x = canvas.width - badge.width - 30
        canvas.paste(badge, (x, 30), badge)
    except:
        pass


def draw_footer(draw, width, height, date, category, font):

    footer_h = 95

    draw.rectangle(
        (0, height-footer_h, width, height),
        fill=(15, 15, 15)
    )

    draw.text(
        (40, height-68),
        "📅 " + date,
        fill="white",
        font=font
    )

    text_width = draw.textlength(category, font=font)

    draw.text(
        (width-text_width-40, height-68),
        category.upper(),
        fill="white",
        font=font
    )


def headline_start_y(image_height):
    return int(image_height * 0.62)


def summary_start_y(image_height):
    return int(image_height * 0.82)