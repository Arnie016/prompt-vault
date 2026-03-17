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

Required keys are defined in [schemas/prompt-entry.schema.json](/Users/hema/Desktop/prompt-vault/schemas/prompt-entry.schema.json).

## Review bar

Reject prompts that are:

- generic
- redundant
- under-specified
- obviously model-fragile
- impossible to understand without extra context

Prefer prompts that show:

- strong composition
- clear stylistic control
- reusable structure
- interesting constraints
- high remix potential

## Maintenance

After adding or editing prompts:

```bash
python3 scripts/validate_prompts.py
python3 scripts/build_catalog.py
```
