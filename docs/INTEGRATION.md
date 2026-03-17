# Integration

This repo is meant to be easy to consume from any client.

## Recommended options

### Option 1: clone and read JSON locally

Best when your app can vendor or periodically sync the repo.

- use `data/catalog.json` for discovery
- use `data/prompt-memory-db.json` for the full dataset
- use `prompts/` when you want one-file-per-entry workflows

### Option 2: fetch raw files directly from GitHub

Useful for prototypes or server-side tools that do not want a full clone.

Typical targets:

- `data/catalog.json`
- `data/prompt-memory-db.json`
- files under `prompts/`

### Option 3: fork and extend

Best when you want your own private prompt layer while keeping compatibility with the public schema.

## Stability contract

Clients should treat these as the stable interfaces:

- `schemas/prompt-entry.schema.json`
- `data/catalog.json`
- `data/prompt-memory-db.json`

Markdown files are useful for humans but should not be considered the machine contract.

## Consumption pattern

1. Read `data/catalog.json`.
2. Filter by `category`, `tags`, `status`, or `best_for`.
3. Read the matching prompt entries from the full DB or individual prompt files.
4. Surface `cleaned_prompt` by default.
5. Use `raw_prompt` for provenance and remix history.

## Compatibility advice

- prefer additive schema changes over breaking ones
- keep old keys when possible
- do not depend on Markdown parsing for core behavior
- cache the generated data files if your client needs fast startup
