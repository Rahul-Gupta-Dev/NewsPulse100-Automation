from modules.ai.client import ask_groq


def select_best_news(news_list):

    prompt = f"""
You are a news editor.

Choose ONLY ONE most important and viral news.

Return ONLY the index number.

News:

"""

    for i, news in enumerate(news_list):
        prompt += f"\n{i}. {news['title']}"

    response = ask_groq(prompt)

    return int(response.strip())