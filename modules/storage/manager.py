from pathlib import Path
from datetime import datetime


def create_output_folder():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    folder = Path("output") / timestamp
    folder.mkdir(parents=True, exist_ok=True)

    return folder