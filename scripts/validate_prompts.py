from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = REPO_ROOT / "prompts"
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


def validate_entry(path: Path) -> list[str]:
    errors = []
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        return [f"{path}: invalid JSON: {exc}"]

    missing = sorted(REQUIRED_KEYS - payload.keys())
    if missing:
        errors.append(f"{path}: missing keys: {', '.join(missing)}")

    for key in ("tags", "style_tokens", "reuse_patterns", "variations", "why_it_works", "best_for"):
        if key in payload and not isinstance(payload[key], list):
            errors.append(f"{path}: {key} must be an array")

    if "slug" in payload and (not isinstance(payload["slug"], str) or payload["slug"] != payload["slug"].lower()):
        errors.append(f"{path}: slug must be lowercase")

    return errors


def main() -> None:
    prompt_files = sorted(PROMPTS_DIR.rglob("*.json"))
    if not prompt_files:
        print("No prompt files found.")
        return

    errors = []
    for path in prompt_files:
        errors.extend(validate_entry(path))

    if errors:
        print("\n".join(errors))
        sys.exit(1)

    print(f"Validated {len(prompt_files)} prompt files.")


if __name__ == "__main__":
    main()
