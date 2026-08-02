import feedparser
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta

BASE_URL = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"


def fetch_news(queries, limit=10):

    if isinstance(queries, str):
        queries = [queries]

    news_list = []

    now = datetime.now(timezone.utc)
    last_48_hours = now - timedelta(hours=48)

    for query in queries:

        url = BASE_URL.format(query=query.replace(" ", "+"))

        feed = feedparser.parse(url)

        for entry in feed.entries:

            try:
                published = parsedate_to_datetime(entry.published)

                if published < last_48_hours:
                    continue

            except Exception:
                continue

            news_list.append({
                "title": entry.title,
                "summary": entry.get("summary", ""),
                "link": entry.link,
                "published": entry.get("published", ""),
                "source": entry.get("source", {}).get("title", "Unknown")
            })

            if len(news_list) >= limit:
                return news_list

    return news_list