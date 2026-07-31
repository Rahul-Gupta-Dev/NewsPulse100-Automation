from collections import Counter


def smart_category(all_news):
    scores = {}

    for category, news_list in all_news.items():
        scores[category] = len(news_list)

    if not scores:
        return None

    return max(scores, key=scores.get)