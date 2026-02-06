# Copilot Agent Instructions for txt2ged

## 1. Project Overview
- **Purpose**: Convert a plain‑text family tree into a GEDCOM file.
- **Core script**: `txt2ged.py` – parses the input, builds a tree of `Node` objects, assigns GEDCOM IDs, and writes the output.
- **Input format**: Each line represents a person. Leading tabs indicate depth. Names and dates are in parentheses. Spouses are separated by the word `ép`.
- **Output**: A valid GEDCOM file that can be opened in tools such as Topola.

## 2. Key Files & Patterns
| File | What it contains | Notable pattern |
|------|------------------|-----------------|
| `txt2ged.py` | Main logic | Recursive tree building (`build_tree`), ID assignment (`assign_ids`), and GEDCOM writing (`write_gedcom`). |
| `README.md` | Usage, tests, prompt guidance | Shows how to run the script and how to craft prompts for Copilot Agent. |
| `prompt *.txt` | Sample prompts for Copilot Agent | Demonstrates how to ask the agent to generate or modify the script. |

### 2.1 Parsing Lines
```python
depth = len(line) - len(line.lstrip("\t"))
content = line.lstrip("\t").strip()
parts = [p.strip() for p in re.split(r"\s*\bép\b\s*", content)]
```
- Tabs → depth.
- `ép` splits person and spouse.
- `PERSON_RE` extracts name and optional death year.

### 2.2 Building the Tree
```python
while stack and stack[-1][0] >= depth:
    stack.pop()
```
- Maintains a stack of `(depth, node)` to attach children correctly.

### 2.3 ID Assignment
```python
node.individual_id = f"@I{indiv_counter}@"
node.family_id = f"@F{fam_counter}@"
```
- Sequential IDs ensure uniqueness.

### 2.4 Writing GEDCOM
- Families are written first, then individuals.
- Each `Node` writes its spouse as a separate `INDI` record.
- Parent–child links use `CHIL`, `FAMC`, and `FAMS` tags.

## 3. Developer Workflows
1. **Run the script**
   ```bash
   python3 txt2ged.py toto.txt toto.ged
   ```
2. **Verify output** – open `toto.ged` in Topola: <https://pewu.github.io/topola-viewer/>.
3. **Add a new prompt** – create a file like `prompt 260300.0000.txt` and ask Copilot Agent to generate a new feature.
4. **Testing** – no automated tests yet; use the Topola viewer for visual validation.

## 4. Copilot Agent Tips
- **Ask for a specific function**: e.g., *“Add a function to export only the family tree without individuals.”*
- **Use the existing prompt**: copy the content of `prompt 260126.1450.txt` and paste it into the Copilot chat.
- **Explain the input format**: remind the agent that tabs denote depth and `ép` separates spouses.
- **Show the current code**: provide the snippet of `parse_line` to help the agent understand the regex.

## 5. Conventions & Gotchas
- **Tabs vs spaces**: the parser relies on tabs; spaces will break depth detection.
- **Date format**: only four‑digit years are supported; the regex will fail otherwise.
- **Spouse handling**: if a spouse is missing, the script still writes a `HUSB` tag with the individual's ID.
- **No external dependencies**: pure Python 3.8+.

---

Feel free to suggest improvements or report missing documentation.
