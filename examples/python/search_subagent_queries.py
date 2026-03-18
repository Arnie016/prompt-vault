from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / "data" / "subagent-query-catalog.json"


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text())
    matches = [
        entry for entry in catalog["entries"]
        if entry["domain"] == "security" and entry["mode"] == "harden"
    ]

    for entry in matches[:5]:
        print(f'{entry["id"]}: {entry["title"]}')


if __name__ == "__main__":
    main()
