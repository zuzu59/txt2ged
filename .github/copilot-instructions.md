# Project Guidelines

## Code Style
- Prefer Python 3 standard library only unless a dependency is explicitly requested.
- Keep generated and edited Python files UTF-8 compatible.
- Keep parsing logic explicit and simple; this project favors readability over abstractions.

## Architecture
- This repository is an AI-benchmark workflow, not a packaged app.
- Main flow: text genealogy in `input.txt` -> converter script `txt2ged.py` -> GEDCOM output `test.ged`.
- Prompt assets (`prompt.md`, `init.prompt.md`) define generation behavior.


## Build and Test
- Run converter: `python3 txt2ged.py input.txt test.ged`
- For repeatable benchmark runs, start clean: `rm test.ged txt2ged.py`
- Validation is manual:
  - Visual structure check with Topola viewer.
  - GEDCOM syntax check with Ged-Inline.

## Conventions
- Input hierarchy is indentation-based and assumes 4 spaces per generation level.
- Spouses are separated by the literal token `ep` or `ép` in source text.
- Do not infer or assign gender from names.
- Preserve parent-child links strictly from indentation hierarchy.
- Emit GEDCOM 5.5.1-compatible structure with proper INDI/FAM cross-links.
- Keep benchmark integrity: avoid reading old outputs as templates for new generation logic unless explicitly asked to compare against them.
