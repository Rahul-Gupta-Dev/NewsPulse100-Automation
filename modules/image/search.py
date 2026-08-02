import os
import requests

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_and_download_image(query, output_path):
    url = "https://google.serper.dev/images"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query + " -watermark -logo",
        "num": 5
    }

    r = requests.post(url, headers=headers, json=payload, timeout=30)
    print(r.status_code)

    data = r.json()

    if "images" not in data or len(data["images"]) == 0:
        raise Exception(data)

    for item in data["images"]:
        try:
            print(item["imageUrl"])
            image_url = item["imageUrl"]
            bad_sources =["youtube","ytimg","instagram","lookaside","fbsbx","facebook"]
            if any(src in image_url.lower() for src in bad_sources):
                continue

          
            if ("instagram" in image_url.lower() or "lookaside" in image_url.lower() or "fbsbx" in image_url.lower()):
                continue
            img = requests.get(image_url, timeout=30)

            if not img.headers.get("Content-Type", "").startswith("image/"):
                continue

            with open(output_path, "wb") as f:
                f.write(img.content)

            print("✅ Image Saved:", output_path)
            return output_path

        except:
            continue

    raise Exception("No valid image found")