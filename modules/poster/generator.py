import os

from modules.poster.renderer import render_poster


def generate_poster(
    headline,
    summary,
    category,
    image_path="output/news_image.jpg",
    output_path="output/poster.png"
):

    if not os.path.exists(image_path):
        raise FileNotFoundError(image_path)

    poster = render_poster(
        image_path=image_path,
        headline=headline,
        summary=summary,
        category=category
    )

    poster.save(
        output_path,
        quality=100
    )

    print(f"✅ Poster Saved : {output_path}")
    return output_path