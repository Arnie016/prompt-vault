from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / "data" / "catalog.json"


def filter_entries(entries: list[dict], *, category: str | None = None, exclude_statuses: set[str] | None = None) -> list[dict]:
    excluded = exclude_statuses or set()
    return [
        entry for entry in entries
        if (category is None or entry["category"] == category)
        and entry["status"] not in excluded
    ]


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text())
    curated = filter_entries(
        catalog["entries"],
        category="image",
        exclude_statuses={"seed"},
    )

    for entry in curated:
        print(f'{entry["id"]}: {entry["title"]} [{entry["status"]}] -> {entry["path"]}')


if __name__ == "__main__":
    main()
