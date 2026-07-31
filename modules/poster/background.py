from PIL import Image, ImageEnhance, ImageFilter, ImageDraw


def prepare_background(image_path):

    img = Image.open(image_path).convert("RGB")

    img = img.resize((1080, 1350), Image.LANCZOS)

    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = ImageEnhance.Color(img).enhance(1.10)
    img = ImageEnhance.Sharpness(img).enhance(1.15)

    img = img.filter(ImageFilter.GaussianBlur(0.3))

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    h = img.height

    for y in range(h):
        alpha = int(max(0, (y - h * 0.30) / (h * 0.55)) * 255)
        draw.line((0, y, img.width, y), fill=(0, 0, 0, alpha))

    img = Image.alpha_composite(
        img.convert("RGBA"),
        overlay
    ).convert("RGB")

    return img