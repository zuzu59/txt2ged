# Copilot Instructions for txt2ged

## 1. Overview
`txt2ged` is a tiny command‑line tool that converts a **tab‑indented** genealogical
text file into a **GEDCOM** file.  The repository contains only one Python
script (`txt2ged-v1.py`) and a handful of example files (`toto.txt`, `toto.ged`).

### Key concepts
* **Indentation** – each leading tab represents a parent‑child level.
* **Spouse separator** – the word `ép` (French for *married to*) splits a
  person and their spouse.
* **IDs** – individuals are given `@I1@`, `@I2@`, … and families `@F1@`, ….
* **Name format** – `First Last` → `First /Last/` in GEDCOM.

## 2. Usage
```bash
python txt2ged-v1.py input.txt output.ged
```
The script prints a confirmation message on success.  It uses only the
standard library (`re`, `sys`, `pathlib`).

## 3. Input format (see `toto.txt`)
```
Pierre ZUFFEREY (1837) ép Marie DUPONT (1840)
	Jean ZUFFEREY (1865) ép Sophie LEROY (1867)
		Luc ZUFFEREY (1890)
```
* Each line is a person; tabs before the line denote the depth.
* Birth years are in parentheses; a range like `1859-1931` is truncated to
  the first year.

## 4. Output format
The script writes a valid GEDCOM file (`toto.ged`).  Open it with the
Topola viewer (link in `README.md`) to verify the tree.

## 5. Core functions
* `parse_person_part(part)` – extracts name and birth year.
* `format_name(name)` – converts to GEDCOM name syntax.
* `main(argv)` – orchestrates parsing, ID assignment, stack‑based parent
  resolution, and file writing.

## 6. Developer workflow
* **Run**: `python txt2ged-v1.py toto.txt toto.ged`.
* **Test**: Open `toto.ged` in Topola (see `README.md`).
* **Debug**: Add `print` statements or run the script in a debugger.
* **Add features**: Edit `txt2ged-v1.py`; no build step is required.

## 7. Conventions & patterns
* No external dependencies – keep the script lightweight.
* Simple ID counters (`indiv_counter`, `fam_counter`).
* Stack (`stack`) tracks the current parent at each indentation level.
* Error handling is minimal: the script exits with a usage message if
  arguments are missing.

## 8. Extending the tool
* To support more GEDCOM tags, add them in the `write GEDCOM` section.
* For richer input (e.g., dates, places), extend `parse_person_part`.
* If you need a CLI wrapper, consider adding a `setup.py` or `pyproject.toml`.

## 9. Sample data
* `toto.txt` – example input.
* `toto.ged` – generated output.
* `prompt 260126.1450.txt` – a prompt used by the author for AI experiments.

## 10. Feedback
Please let me know if any section is unclear or if you need additional
examples for a specific workflow.
