from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


def generate_poster(data, output_path="poster.png"):

    WIDTH = 1080
    HEIGHT = 1350

    img = Image.new("RGB", (WIDTH, HEIGHT), "#ffffff")
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("fonts/NotoSansDevanagari-Regular.ttf", 60)
text_font = ImageFont.truetype("fonts/NotoSansDevanagari-Regular.ttf", 38)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Header
    draw.rectangle((0, 0, WIDTH, 120), fill="#d32f2f")
    draw.text((40, 30), "NewsPulse100", fill="white", font=title_font)

    # Date
    today = datetime.now().strftime("%d %b %Y")
    draw.text((40, 150), today, fill="black", font=text_font)

    # Headline
    draw.text(
        (40, 250),
        data["poster_headline"],
        fill="black",
        font=title_font
    )

    # Summary
    draw.text(
        (40, 420),
        data["summary_hindi"],
        fill="#333333",
        font=text_font
    )

    img.save(output_path)

    print("✅ Poster saved:", output_path)