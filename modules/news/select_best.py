import json
import re

from modules.ai.client import ask_groq


# -------------------------------------------------
# CONFIG
# -------------------------------------------------

BATCH_SIZE = 20
TOP_PER_BATCH = 3


# -------------------------------------------------
# ASK AI TO SELECT FROM SMALL BATCH
# -------------------------------------------------

def select_batch(news_list, limit=TOP_PER_BATCH):

    if not news_list:
        return []

    prompt = """
You are a senior Indian news editor.

From the following news candidates, select the most important
and nationally relevant news stories for an Indian audience.

Selection priority:

1. Major national importance
2. Large public impact
3. Government / policy decisions
4. Major accidents / disasters
5. Economy / business impact
6. Major sports news
7. Education / jobs with large impact
8. Important international news affecting India
9. Breaking or developing news
10. Avoid celebrity gossip and trivial stories

IMPORTANT:
- Do NOT select duplicate or nearly identical stories.
- Prefer factual and significant news.
- Select at most {limit} stories.

Return ONLY a JSON array of INDEX NUMBERS.

Example:
[0, 4, 7]

NEWS:
""".format(limit=limit)

    for i, news in enumerate(news_list):

        title = str(news.get("title", "")).strip()
        source = str(news.get("source", "")).strip()

        prompt += f"\n{i}. {title}"

        if source:
            prompt += f" | Source: {source}"


    response = ask_groq(prompt)

    response = response.strip()


    # -------------------------------------------------
    # CLEAN AI RESPONSE
    # -------------------------------------------------

    if response.startswith("```"):
        response = re.sub(
            r"```(?:json)?",
            "",
            response,
            flags=re.IGNORECASE
        )

        response = response.replace("```", "").strip()


    # -------------------------------------------------
    # PARSE JSON
    # -------------------------------------------------

    try:

        result = json.loads(response)

        if isinstance(result, list):

            indexes = []

            for value in result:

                try:
                    index = int(value)

                    if (
                        0 <= index < len(news_list)
                        and index not in indexes
                    ):
                        indexes.append(index)

                except Exception:
                    continue

            return indexes[:limit]

    except Exception:
        pass


    # -------------------------------------------------
    # FALLBACK: FIND NUMBERS
    # -------------------------------------------------

    numbers = re.findall(
        r"\b\d+\b",
        response
    )

    indexes = []

    for number in numbers:

        index = int(number)

        if (
            0 <= index < len(news_list)
            and index not in indexes
        ):
            indexes.append(index)

    return indexes[:limit]


# -------------------------------------------------
# TOP 10 NEWS
# -------------------------------------------------

def select_top_news(news_list, limit=10):

    if not news_list:
        return []


    print("\n🤖 Selecting India's Top News...")


    # -------------------------------------------------
    # SMALL NUMBER OF NEWS
    # -------------------------------------------------

    if len(news_list) <= BATCH_SIZE:

        selected = select_batch(
            news_list,
            limit=limit
        )

        print(
            f"✅ AI selected {len(selected)} news."
        )

        return selected


    # -------------------------------------------------
    # STEP 1
    # DIVIDE NEWS INTO SMALL BATCHES
    # -------------------------------------------------

    candidates = []


    for start in range(
        0,
        len(news_list),
        BATCH_SIZE
    ):

        batch = news_list[
            start:start + BATCH_SIZE
        ]

        print(
            f"🔎 Evaluating news "
            f"{start + 1}-{start + len(batch)} "
            f"of {len(news_list)}"
        )


        selected_indexes = select_batch(
            batch,
            limit=TOP_PER_BATCH
        )


        for index in selected_indexes:

            if 0 <= index < len(batch):

                candidates.append(
                    batch[index]
                )


    print(
        f"\n📌 Intermediate candidates: "
        f"{len(candidates)}"
    )


    # -------------------------------------------------
    # REMOVE DUPLICATES AGAIN
    # -------------------------------------------------

    unique_candidates = []

    seen = set()


    for news in candidates:

        title = (
            str(news.get("title", ""))
            .strip()
            .lower()
        )

        if not title:
            continue

        if title in seen:
            continue

        seen.add(title)

        unique_candidates.append(news)


    print(
        f"📌 Final candidates for ranking: "
        f"{len(unique_candidates)}"
    )


    # -------------------------------------------------
    # STEP 2
    # FINAL TOP 10 SELECTION
    # -------------------------------------------------

    final_indexes = select_batch(
        unique_candidates,
        limit=limit
    )


    # -------------------------------------------------
    # SAFETY FALLBACK
    # -------------------------------------------------

    if len(final_indexes) < limit:

        for i in range(
            len(unique_candidates)
        ):

            if i not in final_indexes:

                final_indexes.append(i)

            if len(final_indexes) >= limit:
                break


    # -------------------------------------------------
    # PRINT FINAL TOP NEWS
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("🇮🇳 INDIA TOP NEWS")
    print("=" * 60)


    for rank, index in enumerate(
        final_indexes[:limit],
        start=1
    ):

        if 0 <= index < len(unique_candidates):

            print(
                f"{rank}. "
                f"{unique_candidates[index].get('title', '')}"
            )


    # -------------------------------------------------
    # IMPORTANT
    # RETURN ORIGINAL NEWS INDEXES
    # -------------------------------------------------

    selected_news = [
        unique_candidates[i]
        for i in final_indexes[:limit]
        if 0 <= i < len(unique_candidates)
    ]


    original_indexes = []


    for selected in selected_news:

        try:

            original_index = news_list.index(
                selected
            )

            original_indexes.append(
                original_index
            )

        except ValueError:
            continue


    return original_indexes[:limit]


# -------------------------------------------------
# OLD FUNCTION
# -------------------------------------------------
# Keeps compatibility with older code.
# -------------------------------------------------

def select_best_news(news_list):

    selected = select_top_news(
        news_list,
        limit=1
    )

    if selected:
        return selected[0]

    return 0