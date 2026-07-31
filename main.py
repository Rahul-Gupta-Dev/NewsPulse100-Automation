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
from modules.news.smart_category import smart_category
from modules.news.deduplicate import is_duplicate
from modules.utils.retry import retry
from modules.utils.error_handler import handle_error

try:

    # Create Output Folder
    output_folder = create_output_folder()
    print("Output Folder:", output_folder)
    
    # Output Paths
    image_path = output_folder / "news_image.jpg"
    poster_path = output_folder / "poster.png"
    video_path = output_folder / "shorts.mp4"
    
    # Collect News
    all_news = collect_news()
    
    
    
    category = smart_category(all_news)
    
    news_list = all_news[category]
    
    best_index = select_best_news(news_list)
    
    best_news = news_list[best_index]
    if is_duplicate(best_news["title"]):
        print("⚠️ Duplicate news skipped.")
        raise SystemExit
    
    # AI Processing
    result = process_article(best_news, category)
    
    # Generate Image
    image_path = retry(
        generate_image,
        prompt=result["poster_headline"],
        output_path=str(image_path)
    )
    if image_path is None:
        raise Exception("Image generation failed after retries.")
    
    # Generate Poster
    poster_path = generate_poster(
        headline=result["poster_headline"],
        summary=result["summary_hindi"],
        category=category,
        image_path=str(image_path),
        output_path=str(poster_path)
    )
    
    # Generate Shorts
    generate_shorts(
        image=str(poster_path),
        output=str(video_path)
    )
    
    # Generate SEO
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
    
    save_json(article, output_folder / "article.json")
    save_json(seo, output_folder / "seo.json")
    
    print("Image :", image_path)
    print("Poster:", poster_path)
    print("Video :", video_path)
    print("SEO   :", seo)
    
    write_log(output_folder / "log.txt", "Project completed successfully.")

except Exception as e:
    handle_error(e)