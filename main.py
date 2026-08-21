from modules.news.collector import collect_news
from modules.news.select_best import select_top_news
from modules.ai.processor import process_article
from modules.poster.generator_v2 import generate_poster
from modules.video.shorts import generate_shorts
from modules.seo.generator import generate_seo
from modules.storage.manager import create_output_folder
from modules.storage.save_json import save_json
from modules.storage.logger import write_log
from modules.news.deduplicate import is_duplicate
from modules.utils.retry import retry
from modules.utils.error_handler import handle_error
from modules.image.search import search_and_download_image


try:

    print("\n" + "=" * 60)
    print("🇮🇳 NEWSPULSE100 — INDIA TOP 10 NEWS")
    print("=" * 60)

    # -------------------------------------------------
    # STEP 1: COLLECT ALL CANDIDATE NEWS
    # -------------------------------------------------

    all_news = collect_news()

    print(f"\n📰 Total candidate news collected: {len(all_news)}")


    if not all_news:
        print("❌ No news found.")
        raise SystemExit


    # -------------------------------------------------
    # STEP 2: REMOVE DUPLICATES
    # -------------------------------------------------

    unique_news = []
    seen_titles = set()

    for news in all_news:

        title = news.get("title", "").strip().lower()

        if not title:
            continue

        if title in seen_titles:
            continue

        seen_titles.add(title)

        if is_duplicate(news["title"]):
            print("⚠️ Old/duplicate news skipped:")
            print(news["title"])
            continue

        unique_news.append(news)


    print(f"\n✅ Unique news available: {len(unique_news)}")


    if len(unique_news) < 10:
        print("⚠️ Less than 10 unique news available.")
        print("Continuing with available news...")


    # -------------------------------------------------
    # STEP 3: AI SELECT TOP 10 INDIA NEWS
    # -------------------------------------------------

    selected_indexes = select_top_news(
        unique_news,
        limit=10
    )


    if not selected_indexes:
        print("❌ AI could not select Top 10 news.")
        raise SystemExit


    top_news = [
        unique_news[index]
        for index in selected_indexes
        if 0 <= index < len(unique_news)
    ]


    print("\n" + "=" * 60)
    print("🔥 INDIA TOP NEWS SELECTED")
    print("=" * 60)


    for rank, news in enumerate(top_news, start=1):

        print(
            f"{rank}. "
            f"{news.get('title', 'No title')} "
            f"[{news.get('source', 'Unknown')}]"
        )


    # -------------------------------------------------
    # STEP 4: PROCESS EACH TOP NEWS
    # -------------------------------------------------

    for rank, best_news in enumerate(top_news, start=1):

        print("\n" + "=" * 60)
        print(f"📰 PROCESSING NEWS {rank}/10")
        print("=" * 60)

        print("Title:", best_news.get("title"))
        print("Source:", best_news.get("source"))
        print("Category:", best_news.get("category"))


        category = best_news.get(
            "category",
            "national"
        )


        # -------------------------------------------------
        # OUTPUT FOLDER
        # -------------------------------------------------

        output_folder = create_output_folder(
            f"{rank:02d}_{category}"
        )


        image_path = output_folder / "news_image.jpg"
        poster_path = output_folder / "poster.png"
        video_path = output_folder / "shorts.mp4"


        # -------------------------------------------------
        # AI PROCESSING
        # -------------------------------------------------

        result = process_article(
            best_news,
            category
        )


        if result is None:

            print("❌ AI processing failed.")
            continue


        # -------------------------------------------------
        # IMAGE SEARCH
        # -------------------------------------------------

        image_path = retry(
            search_and_download_image,
            query=result["image_prompt"],
            output_path=str(image_path)
        )


        if image_path is None:

            print("❌ Image search failed.")
            continue


        # -------------------------------------------------
        # POSTER
        # -------------------------------------------------

        poster_path = generate_poster(
            headline=result["poster_headline"],
            summary=result["summary_hindi"],
            category=category,
            image_path=str(image_path),
            output_path=str(poster_path)
        )


        # -------------------------------------------------
        # SHORT VIDEO
        # -------------------------------------------------

        generate_shorts(
            image=str(poster_path),
            output=str(video_path)
        )


        # -------------------------------------------------
        # SEO
        # -------------------------------------------------

        seo = generate_seo(
            result["headline_hindi"],
            result["summary_hindi"],
            category
        )


        # -------------------------------------------------
        # ARTICLE JSON
        # -------------------------------------------------

        article = {

            "rank": rank,

            "category": category,

            "headline_hindi":
                result["headline_hindi"],

            "summary_hindi":
                result["summary_hindi"],

            "poster_headline":
                result["poster_headline"],

            "short_script":
                result["short_script"],

            "hashtags":
                result.get("hashtags", [])
        }


        # -------------------------------------------------
        # METADATA
        # -------------------------------------------------

        metadata = {

            "rank": rank,

            "category": category,

            "source":
                best_news.get("source"),

            "published":
                best_news.get("published"),

            "link":
                best_news.get("link"),

            "original_title":
                best_news.get("title")
        }


        # -------------------------------------------------
        # SAVE FILES
        # -------------------------------------------------

        save_json(
            article,
            output_folder / "article.json"
        )


        save_json(
            seo,
            output_folder / "seo.json"
        )


        save_json(
            metadata,
            output_folder / "metadata.json"
        )


        # -------------------------------------------------
        # LOG
        # -------------------------------------------------

        write_log(
            output_folder / "log.txt",
            "Completed successfully."
        )


        print(f"✅ News {rank} completed.")


    # -------------------------------------------------
    # FINISHED
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("🎉 INDIA TOP 10 NEWS PROCESSING COMPLETED")
    print("=" * 60)


except Exception as e:

    print("\n❌ FATAL ERROR")

    handle_error(e)