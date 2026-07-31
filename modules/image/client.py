import requests
import urllib.parse


def generate_image(prompt, output_path="output/news_image.jpg"):
    prompt = urllib.parse.quote(prompt)

    url = f"https://image.pollinations.ai/prompt/{prompt}"

    response = requests.get(url)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)

        print("✅ Image Saved:", output_path)
        return output_path

    print("❌ Image Generation Failed")
    return None