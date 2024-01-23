import json
from pathlib import Path


REPO_ROOT_DIR = Path(__file__).parent.parent


def write_to_json(object, filename):
    filepath = REPO_ROOT_DIR / filename

    with open(filepath, "w") as write_file:
        json.dump(object, write_file)