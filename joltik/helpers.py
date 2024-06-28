import json
from pathlib import Path

PROJECT_ROOT = Path.cwd()


def load_json(file_name: str) -> list[str]:
    with open(PROJECT_ROOT / file_name) as file:
        return json.load(file)


SERVICE = load_json("joltik/models/service.json")
