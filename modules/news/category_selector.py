def select_category(all_news):
    for category, news in all_news.items():
        if news:
            return category
    return None