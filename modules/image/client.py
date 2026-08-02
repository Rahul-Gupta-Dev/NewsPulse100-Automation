import os
import requests

FAL_KEY = os.getenv("FAL_KEY")

URL = "https://fal.run/fal-ai/flux/dev"


def generate_image(prompt, output_path):

    headers = {
        "Authorization": f"Key {FAL_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "image_size": "portrait_4_3",
        "num_images": 1,
        "enable_safety_checker": True
    }

    print("Generating image...")

    r = requests.post(URL, headers=headers, json=payload, timeout=300)

    if r.status_code != 200:
        print(r.text)
        raise Exception("Image generation failed")

    result = r.json()

    image_url = result["images"][0]["url"]

    img = requests.get(image_url)

    with open(output_path, "wb") as f:
        f.write(img.content)

    print("✅ Image Saved:", output_path)

    return output_path