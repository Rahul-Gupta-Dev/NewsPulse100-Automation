"""
collector.py

Collect one best news article from each category.

Author: Rahul Gupta
Project: NewsPulse100 Automation
"""

from modules.news.rss import fetch_news
from modules.news.cleaner import clean_article


CATEGORIES = {
    "politics": [
        "politics",
        "government",
        "parliament",
        "election"
    ],
    "students": [
        "education",
        "jee",
        "neet",
        "ugc",
        "cbse"
    ],
    "jobs": [
        "government jobs",
        "ssc",
        "upsc",
        "railway recruitment"
    ],
    "business": [
        "business",
        "economy",
        "stock market",
        "startup"
    ],
    "sports": [
        "cricket",
        "football",
        "tennis",
        "olympics",
        "sports"
    ]
}


def collect_news():

    collected = {}

    for category, query in CATEGORIES.items():

        news = fetch_news(query, limit=10)

        if news:
            collected[category] = [clean_article(n) for n in news]

        else:
            collected[category] = []

    return collected