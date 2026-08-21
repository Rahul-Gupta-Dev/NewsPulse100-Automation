"""
News Collector
NewsPulse100 Automation
"""

from modules.news.rss import fetch_news
from modules.news.cleaner import clean_article


CATEGORIES = {
    "politics": [
        "India politics government parliament",
        "India government latest news",
        "India parliament latest",
    ],

    "students": [
        "India education students latest",
        "India school college university latest",
        "JEE NEET UGC CBSE latest",
    ],

    "jobs": [
        "India government jobs latest",
        "India recruitment vacancy latest",
        "SSC UPSC railway jobs latest",
    ],

    "business": [
        "India business economy latest",
        "India stock market economy latest",
        "India companies corporate latest",
    ],

    "sports": [
        "India cricket latest",
        "India sports latest",
        "Indian cricket team latest",
    ],

    "national": [
        "India latest news",
        "India breaking news",
        "India major news today",
    ],

    "weather": [
        "India weather flood rain latest",
        "India flood latest",
        "India monsoon latest",
    ],

    "science": [
        "India science technology latest",
        "ISRO India latest",
        "India research technology latest",
    ]
}


def collect_news():

    collected = []

    for category, queries in CATEGORIES.items():

        for query in queries:

            try:
                news = fetch_news(query, limit=10)

                for article in news:

                    article = clean_article(article)

                    article["category"] = category

                    collected.append(article)

            except Exception as e:
                print(f"⚠️ Failed query: {query}")
                print(e)

    return collected