# prompt-vault

A structured prompt memory vault for storing, tagging, remixing, and surfacing high-signal prompts and creative ideas.

This repo is designed to be useful in two ways:

1. Humans can browse prompts, read why they work, and remix them.
2. Clients can clone the repo and consume the JSON files directly.

## Why this repo exists

Most prompt repos are just text dumps. This one is opinionated:

- every prompt gets structure
- every prompt keeps the original raw wording
- every prompt gets cleaned and tagged
- strong prompts surface reusable patterns, not just one-off text

## Repo layout

```text
prompt-vault/
  data/
    catalog.json
    prompt-memory-db.json
  docs/
    INTEGRATION.md
  examples/
    javascript/load-prompts.mjs
    python/load_prompts.py
  prompts/
    image/
      insectoid-human-retro-futurist-portrait.json
      post-rain-summer-cyclist-seaside-village.json
  schemas/
    prompt-entry.schema.json
  scripts/
    build_catalog.py
    validate_prompts.py
  surfaced/
    ideas.md
  CONTRIBUTING.md
  CONTENT_LICENSE.md
  LICENSE
```

## Data model

Each prompt entry follows a stable JSON shape with fields such as:

- `id`
- `slug`
- `title`
- `category`
- `status`
- `raw_prompt`
- `cleaned_prompt`
- `tags`
- `style_tokens`
- `reuse_patterns`
- `variations`
- `why_it_works`
- `failure_modes`
- `best_for`

The schema lives at [schemas/prompt-entry.schema.json](/Users/hema/Desktop/prompt-vault/schemas/prompt-entry.schema.json).

## Quick start

Clone the repo:

```bash
git clone https://github.com/Arnie016/prompt-vault.git
cd prompt-vault
```

Browse the lightweight summary:

```bash
cat data/catalog.json
```

Load the full prompt database:

```bash
cat data/prompt-memory-db.json
```

Validate prompt files:

```bash
python3 scripts/validate_prompts.py
```

Rebuild generated data:

```bash
python3 scripts/build_catalog.py
```

## Integration strategy

The simplest way for other clients to integrate is:

1. Clone the repo.
2. Read `data/catalog.json` to discover prompts.
3. Read `data/prompt-memory-db.json` or individual files in `prompts/`.
4. Filter by `category`, `tags`, `status`, or `best_for`.

Use [docs/INTEGRATION.md](/Users/hema/Desktop/prompt-vault/docs/INTEGRATION.md) for concrete examples.

## Curation rules

- Preserve the original prompt text, even if it is partial or messy.
- Add a cleaned version rather than overwriting the original.
- Prefer small numbers of strong prompts over large numbers of weak prompts.
- Record why a prompt works and how to remix it.

## Contribution model

See [CONTRIBUTING.md](/Users/hema/Desktop/prompt-vault/CONTRIBUTING.md) for the expected entry shape and review standard.

## Licensing

- Code, schema, and scripts: MIT via [LICENSE](/Users/hema/Desktop/prompt-vault/LICENSE)
- Prompt content and data: CC0 via [CONTENT_LICENSE.md](/Users/hema/Desktop/prompt-vault/CONTENT_LICENSE.md)
