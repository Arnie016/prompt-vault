from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "subagent-queries.json"
CATALOG_PATH = REPO_ROOT / "data" / "subagent-query-catalog.json"
REQUIRED_KEYS = {
    "id",
    "slug",
    "title",
    "domain",
    "scenario",
    "mode",
    "difficulty",
    "recommended_subagents",
    "prompt",
    "expected_output",
    "tags",
}


def main() -> None:
    if not DATA_PATH.exists():
        print(f"Missing generated file: {DATA_PATH}")
        sys.exit(1)
    if not CATALOG_PATH.exists():
        print(f"Missing generated file: {CATALOG_PATH}")
        sys.exit(1)

    payload = json.loads(DATA_PATH.read_text())
    catalog = json.loads(CATALOG_PATH.read_text())
    entries = payload.get("entries", [])

    errors: list[str] = []
    if payload.get("query_count") != 1000:
        errors.append(f"Expected query_count=1000, found {payload.get('query_count')}")
    if len(entries) != 1000:
        errors.append(f"Expected 1000 entries, found {len(entries)}")
    if catalog.get("query_count") != 1000:
        errors.append(f"Expected catalog query_count=1000, found {catalog.get('query_count')}")

    ids = set()
    slugs = set()
    for entry in entries:
        missing = REQUIRED_KEYS - entry.keys()
        if missing:
            errors.append(f"{entry.get('id', '<missing id>')}: missing keys: {', '.join(sorted(missing))}")
        if entry.get("id") in ids:
            errors.append(f"Duplicate id: {entry.get('id')}")
        if entry.get("slug") in slugs:
            errors.append(f"Duplicate slug: {entry.get('slug')}")
        ids.add(entry.get("id"))
        slugs.add(entry.get("slug"))

        for key in ("recommended_subagents", "expected_output", "tags"):
            if key in entry and not isinstance(entry[key], list):
                errors.append(f"{entry.get('id')}: {key} must be a list")

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    print(f"Validated {len(entries)} subagent query entries.")


if __name__ == "__main__":
    main()
