from pathlib import Path
from datetime import datetime


def create_output_folder(category=None):

    date_folder = datetime.now().strftime("%Y-%m-%d")

    folder = Path("output") / date_folder

    if category:
        folder = folder / category.capitalize()

    folder.mkdir(parents=True, exist_ok=True)

    return folder