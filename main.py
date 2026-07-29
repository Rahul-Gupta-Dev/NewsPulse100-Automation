from modules.news.collector import collect_news
from modules.ai.processor import process_article
from modules.poster.generator import generate_poster

news = collect_news()

article = news["politics"]

result = process_article(article, "politics")

generate_poster(result)