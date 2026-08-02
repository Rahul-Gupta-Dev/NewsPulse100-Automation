from dotenv import load_dotenv
import os
import json
import requests
import re

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def generate_seo(headline, summary, category):

    prompt = f"""
Generate SEO content for this news.

Headline: {headline}
Summary: {summary}
Category: {category}

Return ONLY valid JSON.

Rules:
1. Do not use markdown.
2. Do not wrap the response in ```json.
3. Return only JSON.
4. Description should be 30-50 words.
5. Return exactly 10 hashtags.
6. First 5 hashtags in English.
7. Last 5 hashtags in Hindi.

Format:

{{
    "title": "",
    "description": "",
    "hashtags": []
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
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        timeout=60
    )

    response.raise_for_status()

    text = response.json()["choices"][0]["message"]["content"]

    # Clean response
    text = (
        text.replace("```json", "")
            .replace("```", "")
            .replace("\r", " ")
            .replace("\t", " ")
            .strip()
    )

    # Extract JSON only
    start = text.find("{")
    end = text.rfind("}") + 1

    if start != -1 and end != -1:
        text = text[start:end]

    # Repair common JSON issues
    text = re.sub(r",\s*}", "}", text)
    text = re.sub(r",\s*]", "]", text)

    try:
        seo = json.loads(text)

        seo.setdefault("title", headline)
        seo.setdefault("description", summary)
        seo.setdefault("hashtags", [])

        return seo

    except Exception as e:
        print("❌ SEO JSON Error")
        print(text)
        print(e)

        return {
            "title": headline,
            "description": summary,
            "hashtags": []
        }