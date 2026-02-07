# Copilot Instructions for txt2ged Project

## Overview
This repository contains a small Python script that converts a plain‑text family tree into a GEDCOM file using an AI‑powered prompt.  The script is intentionally minimal to serve as a playground for testing Copilot Agents and local LLMs.

## How to run the script
```bash
# Activate the virtual environment
source venv/bin/activate

# Run the conversion
python txt2ged.py <input.txt> <output.ged>
```

The script expects the input file to follow the format described in the README:
- Each line contains a name, a birth year, and optionally a death year separated by a dash (e.g. `John Doe (1837-1901)`).
- Hierarchy is indicated by leading tabs.
- Spouses are separated by the word `ép`.

## Prompting the AI
Open the most recent prompt file (e.g. `prompt 260206.1448.txt`) and paste it into the Copilot chat.  The prompt instructs the AI to generate the Python script.  The AI will then produce a `txt2ged.py` file.

## Testing the output
The generated GEDCOM file can be visualised with the Topola viewer:
https://pewu.github.io/topola-viewer/

## Common pitfalls
- **Missing death year handling** – The original script only parsed the first year in parentheses.  The prompt now explicitly asks the AI to handle both birth and death years.
- **Incorrect hierarchy** – Ensure tabs are preserved in the input file; otherwise the tree structure will be lost.

## Development workflow
1. **Create a new prompt** – Write a detailed prompt in a new `.txt` file.
2. **Ask Copilot** – Paste the prompt into the chat and let the AI generate `txt2ged.py`.
3. **Run & test** – Execute the script and verify the GEDCOM output with Topola.
4. **Iterate** – Refine the prompt if the output is incomplete.

## Conventions
- The project uses a lightweight virtual environment located in `venv/`.
- No external dependencies are required; the script is pure Python.
- All code is written in French, matching the README and prompt language.

---

Feel free to modify the prompt or the script to experiment with different LLMs or prompt engineering techniques.