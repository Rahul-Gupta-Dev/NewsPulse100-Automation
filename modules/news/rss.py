"""
rss.py

Purpose:
Fetch latest news from Google News RSS Feed.

Author: Rahul Gupta
Project: NewsPulse100 Automation
"""

import feedparser


BASE_URL = "https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"


def fetch_news(query: str, limit: int = 10):
    """
    Fetch latest news from Google News RSS.

    Args:
        query (str): Search keyword
        limit (int): Number of news articles

    Returns:
        list[dict]
    """

    url = BASE_URL.format(query=query.replace(" ", "+"))

    feed = feedparser.parse(url)

    news_list = []

    for entry in feed.entries[:limit]:

        news_list.append({
            "title": entry.title,
            "summary": entry.get("summary", ""),
            "link": entry.link,
            "published": entry.get("published", ""),
            "source": entry.get("source", {}).get("title", "Unknown")
        })

    return news_list