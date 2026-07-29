"""
AI Processor

Author: Rahul Gupta
Project: NewsPulse100 Automation
"""

import json

from modules.ai.client import ask_groq
from modules.ai.prompt import build_prompt


def process_article(article, category):

    prompt = build_prompt(
        article["title"],
        article["summary"],
        category
    )

    response = ask_groq(prompt)

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        print("❌ Invalid JSON returned by AI")
        print(response)
        return None