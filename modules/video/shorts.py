import subprocess


def generate_shorts(
    image="output/poster.png",
    music="assets/music/news_bg.mp3",
    output="output/shorts.mp4",
    duration=10
):

    filter_complex = (
        # Background (same image blurred)
        "[0:v]"
        "scale=1080:1920:force_original_aspect_ratio=increase,"
        "crop=1080:1920,"
        "gblur=sigma=20[bg];"

        # Foreground (original image)
        "[0:v]"
        "scale=950:1689:force_original_aspect_ratio=decrease,"
        "pad=950:1689:(ow-iw)/2:(oh-ih)/2:0x00000000,"
        "zoompan="
        "z='min(zoom+0.0005,1.06)':"
        "d=300:"
        "x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)':"
        "s=1050x1867"
        "[fg];"

        # Overlay foreground on background
        "[bg][fg]"
        "overlay=(W-w)/2:(H-h)/2,"
        "fps=30,"
        "fade=t=in:st=0:d=1,"
        f"fade=t=out:st={duration-1}:d=1"
        "[v]"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", image,
        "-stream_loop", "-1",
        "-i", music,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-t", str(duration),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output
    ]

    subprocess.run(cmd, check=True)
  
    print("✅ Shorts Saved:", output)

    return output