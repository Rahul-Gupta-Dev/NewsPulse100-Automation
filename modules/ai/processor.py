"""
AI Processor

Author: Rahul Gupta
Project: NewsPulse100 Automation
"""

import json
import re

from modules.ai.client import ask_groq
from modules.ai.prompt import build_prompt


def process_article(article, category):

    prompt = build_prompt(
        article["title"],
        article["summary"],
        category
    )

    response = ask_groq(prompt)
    response = response.strip()

    # Remove markdown if present
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    # Keep only JSON
    start = response.find("{")
    end = response.rfind("}") + 1

    if start != -1 and end != -1:
        response = response[start:end]

    try:

        try:
            result = json.loads(response)

        except Exception:
            # ---------- JSON Repair ----------
            response = response.replace("\n", " ")
            response = response.replace("\r", " ")
            response = response.replace("\t", " ")

            response = response.replace(",}", "}")
            response = response.replace(",]", "]")

            response = re.sub(r",\s*}", "}", response)
            response = re.sub(r",\s*]", "]", response)

            result = json.loads(response)

        # ---------- Safe Defaults ----------
        result.setdefault("headline_hindi", "")
        result.setdefault("summary_hindi", "")
        result.setdefault("poster_headline", "")
        result.setdefault("short_script", "")
        result.setdefault("hashtags", [])

        # ---------- Image Prompt ----------
        image_prompts = {
            "politics": "indian parliament politicians press conference high quality",
            "students": "indian students classroom education school university",
            "jobs": "government job recruitment exam students india",
            "business": "stock market business finance office india",
            "sports": "cricket player stadium sports india"
        }

        result["image_prompt"] = image_prompts.get(
            category.lower(),
            article["title"]
        )

        return result

    except Exception as e:
        print("❌ Invalid JSON returned by AI")
        print(response)
        print(e)
        return None