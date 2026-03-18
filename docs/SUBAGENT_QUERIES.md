# Codex Subagent Queries

This repo ships a generated pack of 1000 high-signal prompt queries for Codex users who want to get more value from subagents.

## Why this exists

Most people know subagents are useful, but their prompts are too vague:

- "use subagents and improve this repo"
- "analyze this codebase deeply"
- "find bugs"

Those prompts often waste parallelism. This pack makes the split explicit and repeatable.

## Shape of the pack

The dataset is built from:

- 10 domains
- 10 domain-specific scenarios per domain
- 10 execution modes

That yields 1000 total queries.

Each query includes:

- `domain`
- `scenario`
- `mode`
- `difficulty`
- `recommended_subagents`
- `prompt`
- `expected_output`

## Files

- `data/subagent-query-catalog.json`: lightweight discovery
- `data/subagent-queries.json`: full prompt text
- `schemas/subagent-query.schema.json`: machine contract

## How to use it

1. Filter by `domain`.
2. Narrow by `scenario`.
3. Pick the `mode` that matches what you want Codex to do.
4. Paste the generated `prompt` into Codex and adjust any repo-specific details if needed.

## Good starting filters

- `domain=backend` and `mode=fix`
- `domain=security` and `mode=harden`
- `domain=frontend` and `mode=review`
- `domain=release-platform` and `mode=productionize`
- `domain=docs` and `mode=audit`

## Design choices

- The prompts are specific enough to split work well.
- They stay portable by not depending on one repo layout.
- Recommended subagent names are metadata, not hard requirements.
- The generator is deterministic so the pack can evolve cleanly.

## Maintenance

Regenerate and validate with:

```bash
python3 scripts/generate_subagent_queries.py
python3 scripts/validate_subagent_queries.py
```
