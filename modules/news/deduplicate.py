import hashlib
import json
from pathlib import Path


DB = Path("news_history.json")


def is_duplicate(title):
    key = hashlib.md5(title.lower().encode()).hexdigest()

    if DB.exists():
        history = json.loads(DB.read_text())
    else:
        history = []

    if key in history:
        return True

    history.append(key)
    DB.write_text(json.dumps(history, indent=4))

    return False