from modules.news.collector import collect_news
from modules.news.select_best import select_best_news
from modules.ai.processor import process_article
from modules.image.client import generate_image
from modules.poster.generator_v2 import generate_poster
from modules.video.shorts import generate_shorts
from modules.seo.generator import generate_seo

all_news = collect_news()

category = "politics"

news_list = all_news[category]

best_index = select_best_news(news_list)

best_news = news_list[best_index]

result = process_article(best_news, category)

image_path = generate_image(result["poster_headline"])
poster_path = generate_poster(
    headline=result["poster_headline"],
    summary=result["summary_hindi"],
    category=category,
    image_path=image_path
)
video_path = generate_shorts(
    image=poster_path
)

seo = generate_seo(
    result["headline_hindi"],
    result["summary_hindi"],
    category
)

print(video_path)
print(seo)
print(poster_path)
print(result)
print(image_path)