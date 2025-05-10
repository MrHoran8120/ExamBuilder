# ----- exam_builder/json_loader.py -----
import json


def load_questions(json_file: str) -> list:
    """Read and return the list of question dicts from a JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Optionally: validate structure (keys, types)
    return data