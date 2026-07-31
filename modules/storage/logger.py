from datetime import datetime


def write_log(path, message):
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")