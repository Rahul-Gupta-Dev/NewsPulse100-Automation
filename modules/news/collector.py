"""
collector.py

Collect one best news article from each category.

Author: Rahul Gupta
Project: NewsPulse100 Automation
"""

from modules.news.rss import fetch_news
from modules.news.cleaner import clean_article


CATEGORIES = {
    "politics": "politics government parliament election",
    "students": "student education school college jee neet ugc cbse",
    "jobs": "government jobs vacancy recruitment ssc upsc railway",
    "business": "business economy stock market gold silver",
    "agriculture": "farmer agriculture crop monsoon weather"
}


def collect_news():

    collected = {}

    for category, query in CATEGORIES.items():

        news = fetch_news(query, limit=1)

        if news:
            collected[category] = clean_article(news[0])

        else:
            collected[category] = {
                "title": "No news found",
                "summary": "",
                "link": "",
                "published": "",
                "source": ""
            }

    return collected