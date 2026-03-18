# Contributing

The value of this repo is curation, not volume.

## Submission standard

Every new prompt should:

1. Keep the original wording in `raw_prompt`.
2. Add a cleaned version in `cleaned_prompt`.
3. Include useful tags and style tokens.
4. Explain why the prompt works.
5. Suggest at least one meaningful variation.

## File placement

Store each prompt as one JSON file under the relevant category folder:

- `prompts/image/`
- `prompts/writing/`
- `prompts/workflow/`
- `prompts/system/`

If a category does not exist yet, add it deliberately rather than inventing overlapping names.

## Required fields

Required keys are defined in [`schemas/prompt-entry.schema.json`](./schemas/prompt-entry.schema.json).

## Review bar

Reject prompts that are:

- generic
- redundant
- under-specified
- obviously model-fragile
- impossible to understand without extra context
- only a vibe with no reusable structure

Prefer prompts that show:

- strong composition
- clear stylistic control
- reusable structure
- interesting constraints
- high remix potential

## Minimum acceptable entry

Before opening a PR, make sure the prompt:

- has a clear subject, scene, or task anchor
- contains at least one reusable pattern, not just a one-off aesthetic
- includes at least one meaningful variation that a future contributor could actually build on
- explains failure modes honestly, not as filler

## Review checklist

- Does the entry add a new reusable pattern or meaningfully deepen an existing one?
- Is the cleaned prompt faithful to the raw prompt instead of replacing it?
- Would another client know when to use this entry from `tags`, `best_for`, and `why_it_works` alone?
- Is the prompt strong enough that it raises the average quality of the library?

## Maintenance

After adding or editing prompts:

```bash
python3 scripts/validate_prompts.py
python3 scripts/build_catalog.py
```

## Generated subagent query pack

The files below are generated and should not be edited by hand:

- `data/subagent-queries.json`
- `data/subagent-query-catalog.json`

To change the Codex subagent query pack, edit the source logic in `scripts/generate_subagent_queries.py`, then run:

```bash
python3 scripts/generate_subagent_queries.py
python3 scripts/validate_subagent_queries.py
```
