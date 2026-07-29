"""
AI Prompt

Author: Rahul Gupta
Project: NewsPulse100 Automation
"""


def build_prompt(title, summary, category):

    return f"""
You are an experienced Hindi news editor.

Convert the following English news into clean Hindi.

Rules:

1. Return ONLY valid JSON.
2. Do not use markdown.
3. Do not add extra facts.
4. Use simple Hindi.
5. Poster headline must be catchy.
6. Summary should be 40-60 words.
7. Shorts script should be around 25 seconds.
8. Hashtags should contain only 5 hashtags.
9. Category must remain same.

English Title:
{title}

English Summary:
{summary}

Category:
{category}

Return JSON in exactly this format:

{{
    "headline_hindi": "",
    "summary_hindi": "",
    "poster_headline": "",
    "short_script": "",
    "hashtags": [
        "",
        "",
        "",
        "",
        ""
    ]
}}
"""