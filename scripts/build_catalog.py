from __future__ import annotations

import json
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = REPO_ROOT / "prompts"
DATA_DIR = REPO_ROOT / "data"


def assert_unique(entries: list[dict]) -> None:
    for key in ("id", "slug"):
        seen: dict[str, str] = {}
        for entry in entries:
            value = entry.get(key)
            path = entry.get("_path", "<unknown>")
            if value in seen:
                raise ValueError(f"Duplicate {key} '{value}' in {path} and {seen[value]}")
            seen[value] = path


def load_prompt_files() -> list[dict]:
    entries = []
    for path in sorted(PROMPTS_DIR.rglob("*.json")):
        entry = json.loads(path.read_text())
        entry["_path"] = path.relative_to(REPO_ROOT).as_posix()
        entries.append(entry)
    entries.sort(key=lambda item: (item["category"], item["slug"], item["id"]))
    assert_unique(entries)
    return entries


def build_catalog(entries: list[dict]) -> dict:
    categories = sorted({entry["category"] for entry in entries})
    catalog_entries = []

    for entry in entries:
        catalog_entries.append(
            {
                "id": entry["id"],
                "slug": entry["slug"],
                "title": entry["title"],
                "category": entry["category"],
                "status": entry["status"],
                "tags": entry["tags"],
                "best_for": entry["best_for"],
                "path": entry["_path"],
            }
        )

    return {
        "version": 1,
        "updated_on": max(entry["created_at"] for entry in entries) if entries else None,
        "prompt_count": len(entries),
        "categories": categories,
        "entries": catalog_entries,
    }


def build_db(entries: list[dict]) -> dict:
    normalized_entries = []
    for entry in entries:
        item = dict(entry)
        item.pop("_path", None)
        normalized_entries.append(item)

    latest = max((entry["created_at"] for entry in normalized_entries), default=None)
    return {
        "version": 1,
        "updated_on": latest,
        "prompt_count": len(normalized_entries),
        "entries": normalized_entries,
    }


def write_json(path: Path, payload: dict) -> None:
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False) as handle:
        handle.write(json.dumps(payload, indent=2) + "\n")
        temp_path = Path(handle.name)
    temp_path.replace(path)


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    entries = load_prompt_files()
    write_json(DATA_DIR / "catalog.json", build_catalog(entries))
    write_json(DATA_DIR / "prompt-memory-db.json", build_db(entries))


if __name__ == "__main__":
    main()
