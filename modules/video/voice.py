from gtts import gTTS


def generate_voice(text, output="output/news.mp3"):

    tts = gTTS(
        text=text,
        lang="hi",
        slow=False
    )

    tts.save(output)

    print("✅ Voice Saved:", output)