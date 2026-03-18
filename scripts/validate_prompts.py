from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = REPO_ROOT / "prompts"
SLUG_PATTERN = re.compile(r"^[a-z0-9-]+$")
ALLOWED_STATUSES = {"seed", "curated", "tested", "experimental"}
REQUIRED_KEYS = {
    "id",
    "slug",
    "title",
    "category",
    "status",
    "source",
    "created_at",
    "raw_prompt",
    "cleaned_prompt",
    "tags",
    "style_tokens",
    "reuse_patterns",
    "variations",
    "why_it_works",
    "failure_modes",
    "best_for",
}


def validate_string_list(path: Path, payload: dict, key: str, *, min_items: int = 1) -> list[str]:
    errors = []
    value = payload.get(key)
    if value is None:
        return errors

    if not isinstance(value, list):
        return [f"{path}: {key} must be an array"]

    if len(value) < min_items:
        errors.append(f"{path}: {key} must contain at least {min_items} item(s)")

    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{path}: {key}[{index}] must be a non-empty string")

    return errors


def validate_entry(path: Path) -> list[str]:
    errors = []
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return [f"{path}: invalid JSON: {exc}"]

    if not isinstance(payload, dict):
        return [f"{path}: root value must be an object"]

    missing = sorted(REQUIRED_KEYS - payload.keys())
    if missing:
        errors.append(f"{path}: missing keys: {', '.join(missing)}")

    for key in ("tags", "style_tokens", "reuse_patterns", "variations", "why_it_works", "best_for"):
        errors.extend(validate_string_list(path, payload, key))

    errors.extend(validate_string_list(path, payload, "failure_modes", min_items=0))

    if "slug" in payload:
        slug = payload["slug"]
        if not isinstance(slug, str) or not SLUG_PATTERN.fullmatch(slug):
            errors.append(f"{path}: slug must match ^[a-z0-9-]+$")

    if "status" in payload and payload["status"] not in ALLOWED_STATUSES:
        errors.append(f"{path}: status must be one of {', '.join(sorted(ALLOWED_STATUSES))}")

    if "created_at" in payload:
        created_at = payload["created_at"]
        if not isinstance(created_at, str):
            errors.append(f"{path}: created_at must be a string in YYYY-MM-DD format")
        else:
            try:
                date.fromisoformat(created_at)
            except ValueError:
                errors.append(f"{path}: created_at must be a valid ISO date (YYYY-MM-DD)")

    if "extensions" in payload and not isinstance(payload["extensions"], dict):
        errors.append(f"{path}: extensions must be an object when present")

    return errors


def main() -> None:
    prompt_files = sorted(PROMPTS_DIR.rglob("*.json"))
    if not prompt_files:
        print("No prompt files found.")
        return

    errors = []
    seen_ids: dict[str, Path] = {}
    seen_slugs: dict[str, Path] = {}
    for path in prompt_files:
        errors.extend(validate_entry(path))
        try:
            payload = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue

        if not isinstance(payload, dict):
            continue

        for key, seen in (("id", seen_ids), ("slug", seen_slugs)):
            value = payload.get(key)
            if not isinstance(value, str) or not value:
                continue
            if value in seen:
                errors.append(f"{path}: duplicate {key} '{value}' already used by {seen[value]}")
            else:
                seen[value] = path

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    print(f"Validated {len(prompt_files)} prompt files.")


if __name__ == "__main__":
    main()
