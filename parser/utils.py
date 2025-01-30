import os
import json
import uuid
from datetime import datetime


def get_current_date():
    """Returns the current date in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")


def file_path(filename, output_folder):
    """Returns the full path of a file inside the given output folder."""
    return os.path.join(output_folder, filename)


def load_json(file_path):
    """Loads a JSON file and returns its content. Returns None if the file does not exist."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_json(data, file_paths):
    """Saves data in JSON format to multiple file paths."""
    for path in file_paths:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


def generate_uuid():
    """Generates and returns a unique UUID string."""
    return str(uuid.uuid4())


def add_date(date, file_path="./data/dates.json"):
    """
    Adds a date to the JSON file if it is not already present.
    Creates the file if it does not exist.
    """
    data = load_json(file_path)
    if not data:
        data = {"data": []}

    if date not in data["data"]:
        data["data"].append(date)
        save_json(data, file_path)
