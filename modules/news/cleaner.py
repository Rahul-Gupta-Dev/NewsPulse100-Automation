"""
Clean RSS News Data

Author: Rahul Gupta
Project: NewsPulse100 Automation
"""

import re


def clean_title(title: str):

    title = re.sub(r"\s*-\s*[^-]+$", "", title)

    title = title.replace("’", "'")

    title = title.strip()

    return title


def clean_article(article):

    article["title"] = clean_title(article["title"])

    return article