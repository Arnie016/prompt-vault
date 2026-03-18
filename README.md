# prompt-vault

A curated, machine-readable prompt library for storing, tagging, remixing, and surfacing high-signal prompts and creative ideas, plus a machine-readable library of Codex subagent prompt queries.

This repo is designed to be useful in two ways:

1. Humans can browse prompts, read why they work, and remix them.
2. Clients can clone the repo and consume the JSON files directly.

## What this repo is

- a small, curated library of reusable prompt entries
- a stable JSON contract that clients can integrate directly
- a place to capture why a prompt works, not just the prompt text itself

## What this repo is not

- a prompt dump
- a Markdown-only collection with no machine contract
- a closed system that requires one model, one app, or one provider

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
    subagent-query-catalog.json
    subagent-queries.json
  docs/
    INTEGRATION.md
    SUBAGENT_QUERIES.md
  examples/
    javascript/load-prompts.mjs
    javascript/search-subagent-queries.mjs
    python/load_prompts.py
    python/search_subagent_queries.py
  prompts/
    image/
      insectoid-human-retro-futurist-portrait.json
      post-rain-summer-cyclist-seaside-village.json
  schemas/
    prompt-entry.schema.json
    subagent-query.schema.json
  scripts/
    build_catalog.py
    generate_subagent_queries.py
    validate_prompts.py
    validate_subagent_queries.py
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

The schema lives at [`schemas/prompt-entry.schema.json`](./schemas/prompt-entry.schema.json).
Clients should treat the schema plus the generated files under `data/` as the machine contract.
Human-facing Markdown docs are guidance, not the API.

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

Build and validate the Codex subagent query pack:

```bash
python3 scripts/generate_subagent_queries.py
python3 scripts/validate_subagent_queries.py
```

## 1000 Codex subagent queries

This repo includes a generated collection of 1000 high-signal prompt queries for Codex users who want to use subagents more effectively without inventing prompts from scratch.

The pack lives in:

- `data/subagent-queries.json` for full prompt text
- `data/subagent-query-catalog.json` for lightweight discovery

Each query is organized by:

- `domain`
- `scenario`
- `mode`
- `difficulty`
- `recommended_subagents`

Use [`docs/SUBAGENT_QUERIES.md`](./docs/SUBAGENT_QUERIES.md) for usage guidance.

## Integration strategy

The simplest way for other clients to integrate is:

1. Clone the repo.
2. Read `data/catalog.json` to discover prompts.
3. Read `data/prompt-memory-db.json` or individual files in `prompts/`.
4. Read `data/subagent-query-catalog.json` to discover Codex subagent prompt queries.
5. Filter by `category`, `tags`, `status`, `best_for`, `domain`, `scenario`, or `mode`.

Use [`docs/INTEGRATION.md`](./docs/INTEGRATION.md) for concrete examples.

## Stable interfaces

If you are integrating this repo programmatically, treat these as the supported surfaces:

- `schemas/prompt-entry.schema.json`
- `schemas/subagent-query.schema.json`
- `data/catalog.json`
- `data/prompt-memory-db.json`
- `data/subagent-query-catalog.json`
- `data/subagent-queries.json`
- one-file-per-entry JSON under `prompts/`

Future evolution should stay additive. The core entry shape remains strict, and optional client-specific metadata belongs under `extensions`.

## Curation rules

- Preserve the original prompt text, even if it is partial or messy.
- Add a cleaned version rather than overwriting the original.
- Prefer small numbers of strong prompts over large numbers of weak prompts.
- Record why a prompt works and how to remix it.
- Keep generated subagent query packs reproducible from source scripts rather than editing generated JSON by hand.

## Contribution model

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the expected entry shape and review standard.

## Licensing

- Code, schema, and scripts: MIT via [`LICENSE`](./LICENSE)
- Prompt content and data: CC0 via [`CONTENT_LICENSE.md`](./CONTENT_LICENSE.md)
