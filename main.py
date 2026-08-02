from modules.news.collector import collect_news
from modules.news.select_best import select_best_news
from modules.ai.processor import process_article
from modules.image.client import generate_image
from modules.poster.generator_v2 import generate_poster
from modules.video.shorts import generate_shorts
from modules.seo.generator import generate_seo
from modules.storage.manager import create_output_folder
from modules.storage.save_json import save_json
from modules.storage.logger import write_log
from modules.news.deduplicate import is_duplicate
from modules.utils.retry import retry
from modules.utils.error_handler import handle_error
from modules.image.search import search_and_download_image

try:

    all_news = collect_news()

    for category, news_list in all_news.items():

        print(f"\n===== {category.upper()} =====")

        if not news_list:
            print("No news found.")
            continue

        best_index = select_best_news(news_list)

        best_news = news_list[best_index]

        if is_duplicate(best_news["title"]):
            print("Duplicate news. Skipping...")
            continue

        output_folder = create_output_folder(category)

        image_path = output_folder / "news_image.jpg"
        poster_path = output_folder / "poster.png"
        video_path = output_folder / "shorts.mp4"

        result = process_article(best_news, category)
        if result is None:
            continue

        image_path = retry(
    search_and_download_image,
    query=result["image_prompt"],
    output_path=str(image_path)
)

        if image_path is None:
            print("Image generation failed.")
            continue

        poster_path = generate_poster(
            headline=result["poster_headline"],
            summary=result["summary_hindi"],
            category=category,
            image_path=str(image_path),
            output_path=str(poster_path)
        )

        generate_shorts(
            image=str(poster_path),
            output=str(video_path)
        )

        seo = generate_seo(
            result["headline_hindi"],
            result["summary_hindi"],
            category
        )

        article = {
            "category": category,
            "headline_hindi": result["headline_hindi"],
            "summary_hindi": result["summary_hindi"],
            "poster_headline": result["poster_headline"],
            "short_script": result["short_script"]
        }

        metadata = {
            "category": category,
            "source": best_news.get("source"),
            "published": best_news.get("published"),
            "link": best_news.get("link")
        }

        save_json(article, output_folder / "article.json")
        save_json(seo, output_folder / "seo.json")
        save_json(metadata, output_folder / "metadata.json")

        write_log(
            output_folder / "log.txt",
            "Completed successfully."
        )

        print("Done:", category)

except Exception as e:
    handle_error(e)