from PIL import Image, ImageDraw, ImageFilter


def add_bottom_gradient(img, height_ratio=0.50):

    w, h = img.size

    fade_height = int(h * height_ratio)

    gradient = Image.new("L", (1, fade_height))

    for y in range(fade_height):

        alpha = int(255 * (y / fade_height))

        gradient.putpixel((0, y), alpha)

    gradient = gradient.resize((w, fade_height))

    black = Image.new("RGBA", (w, fade_height), (0, 0, 0, 255))

    black.putalpha(gradient)

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    overlay.paste(black, (0, h - fade_height))

    return Image.alpha_composite(
        img.convert("RGBA"),
        overlay
    ).convert("RGB")


def add_shadow(draw, position, text, font):

    x, y = position

    for dx in range(-3, 4):
        for dy in range(-3, 4):

            draw.text(
                (x + dx, y + dy),
                text,
                fill=(0, 0, 0),
                font=font
            )


def blur_background(img):

    return img.filter(
        ImageFilter.GaussianBlur(radius=1)
    )