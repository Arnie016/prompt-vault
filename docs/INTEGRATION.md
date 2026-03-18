# Integration

This repo is meant to be easy to consume from any client.

## Machine contract vs human docs

Treat these files as the supported machine contract:

- `schemas/prompt-entry.schema.json`
- `schemas/subagent-query.schema.json`
- `data/catalog.json`
- `data/prompt-memory-db.json`
- `data/subagent-query-catalog.json`
- `data/subagent-queries.json`
- JSON files under `prompts/`

Treat Markdown docs as implementation guidance for humans, not a contract your client should parse.

## Recommended options

### Option 1: clone and read JSON locally

Best when your app can vendor or periodically sync the repo.

- use `data/catalog.json` for discovery
- use `data/prompt-memory-db.json` for the full dataset
- use `data/subagent-query-catalog.json` for Codex subagent query discovery
- use `data/subagent-queries.json` for the full subagent query pack
- use `prompts/` when you want one-file-per-entry workflows

### Option 2: fetch raw files directly from GitHub

Useful for prototypes or server-side tools that do not want a full clone.

Typical targets:

- `data/catalog.json`
- `data/prompt-memory-db.json`
- `data/subagent-query-catalog.json`
- `data/subagent-queries.json`
- files under `prompts/`

### Option 3: fork and extend

Best when you want your own private prompt layer while keeping compatibility with the public schema.

If you need client-specific metadata, prefer the optional `extensions` object inside a prompt entry rather than changing the core required keys.

## Stability contract

Clients should treat these as the stable interfaces:

- `schemas/prompt-entry.schema.json`
- `schemas/subagent-query.schema.json`
- `data/catalog.json`
- `data/prompt-memory-db.json`
- `data/subagent-query-catalog.json`
- `data/subagent-queries.json`

Markdown files are useful for humans but should not be considered the machine contract.

## Consumption pattern

1. Read `data/catalog.json` for prompt-vault discovery and `data/subagent-query-catalog.json` for subagent-query discovery.
2. Filter by `category`, `tags`, `status`, `best_for`, `domain`, `scenario`, or `mode`.
3. Read the matching prompt entries from the full DB or individual prompt files.
4. Surface `cleaned_prompt` by default for prompt-vault entries.
5. Surface `prompt` by default for subagent query entries.
6. Use `raw_prompt` for provenance and remix history on prompt-vault entries.

## Recommended read order

- Start with `data/catalog.json` for cheap discovery.
- Start with `data/subagent-query-catalog.json` for cheap subagent-query discovery.
- Use `data/prompt-memory-db.json` when you want one fetch for the full library.
- Use `data/subagent-queries.json` when you want one fetch for the full Codex subagent prompt pack.
- Use `prompts/` when you prefer one-file-per-entry workflows or incremental sync.

## Compatibility advice

- prefer additive schema changes over breaking ones
- keep old keys when possible
- do not depend on Markdown parsing for core behavior
- cache the generated data files if your client needs fast startup
- tolerate optional additive fields such as `extensions`
