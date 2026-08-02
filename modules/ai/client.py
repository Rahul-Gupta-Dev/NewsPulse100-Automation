"""
Groq REST API Client

Author: Rahul Gupta
Project: NewsPulse100 Automation
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL = "llama-3.3-70b-versatile"


def ask_groq(prompt):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1
    }

    response = requests.post(URL, headers=headers, json=body, timeout=60)

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]