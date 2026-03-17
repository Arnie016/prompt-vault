from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / "data" / "catalog.json"


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text())
    curated = [
        entry for entry in catalog["entries"]
        if entry["category"] == "image" and entry["status"] != "seed"
    ]

    for entry in curated:
        print(f'{entry["id"]}: {entry["title"]}')


if __name__ == "__main__":
    main()
