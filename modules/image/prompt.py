"""
Image Prompt Builder

Author: Rahul Gupta
Project: NewsPulse100 Automation
"""


def build_image_prompt(title, summary, category):

    return f"""
Create a realistic editorial news image.

Category: {category}

Headline:
{title}

Summary:
{summary}

Rules:
- Photorealistic
- High quality
- 4K
- No text
- No watermark
- No logo
- Cinematic lighting
- Professional news photography
- Suitable for newspaper and television news
"""