import requests
import urllib.parse


def generate_image(prompt, output_file="output/news_image.jpg"):

    prompt = urllib.parse.quote(prompt)

    url = f"https://image.pollinations.ai/prompt/{prompt}"

    response = requests.get(url)

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)

        print("✅ Image Saved:", output_file)
        return output_file

    print("❌ Image Generation Failed")
    return None