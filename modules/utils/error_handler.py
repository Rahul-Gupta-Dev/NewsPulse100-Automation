import traceback


def handle_error(e):
    print(f"❌ Error: {e}")

    with open("error.log", "a", encoding="utf-8") as f:
        f.write(traceback.format_exc())
        f.write("\n" + "=" * 50 + "\n")