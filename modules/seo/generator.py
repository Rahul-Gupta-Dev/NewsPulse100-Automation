from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
import json
import requests
import os


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def generate_seo(headline, summary, category):

    prompt = f"""
Generate SEO content for this news.

Headline: {headline}
Summary: {summary}
Category: {category}

Return ONLY raw JSON.

Do NOT use markdown.
Do NOT wrap the response in ```json.
Do NOT add any explanation.
Return 10 hashtags.
5 hashtags must be in English.
5 hashtags must be in Hindi.

{{
"title":"",
"description":"",
"hashtags":[]
}}
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )
    text = response.json()["choices"][0]["message"]["content"]
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    return json.loads(text)