"""
Image Prompt Builder

Author: Rahul Gupta
Project: NewsPulse100 Automation
"""


def build_image_prompt(title, summary, category):

    if category.lower() == "sports":
        extra = "Sports stadium, athlete, cricket ground, medal ceremony, action sports photography."

    elif category.lower() == "politics":
        extra = "Parliament, government building, leaders, flags, press conference."

    elif category.lower() == "business":
        extra = "Office, stock exchange, finance, charts, business meeting."

    elif category.lower() == "jobs":
        extra = "Students, examination hall, recruitment office, documents."

    elif category.lower() == "students":
        extra = "Classroom, books, students studying, school, college."

    else:
        extra = ""

    return f"""Create a realistic, cinematic news background.

Category: {category}

Headline:
{title}

Summary:
{summary}

Specific scene:
{extra}

Rules:
- Use only real news photography.
- Never generate attractive female model.
- Never generate glamour portrait.
- If people are not required, do not show people.
- Prefer objects, places, logos, buildings and events.
- Background must directly represent the news.
- Hyper realistic photojournalism.
- News topic must be clearly visible.
- No anime.
- No cartoon.
- No 3D character.
- No AI doll.
- No beautiful girl unless the news itself is about that person.
- No glamour.
- No romantic scene.
- No sexy pose.
- No revealing clothes.
- No blurred faces.
- No distorted hands.
- No extra fingers.
- No text.
- No watermark.
- No logo.
- Match the exact news topic.

Examples:
WhatsApp → WhatsApp logo on phone screen.
Israel war → soldiers, tanks, smoke, border.
SSC/UPSC → students giving exam.
Government jobs → candidates, office, documents.
Cricket → cricket stadium or player.
Business → stock market, office, charts.

Professional news photography.
Ultra realistic.
High quality.
"""