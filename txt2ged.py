#!/usr/bin/env python3
"""
txt2ged.py

Script to convert a simple tab-indented genealogical text file into a GEDCOM file.

The input format is a plain text file where each line represents a person.
Each line contains:
    - a name
    - a birth year in parentheses, optionally followed by a death year separated by a dash
    - spouses separated by the word "ép"

Indentation (tabs) indicates parent-child relationships.  The first line is the root ancestor.

Example input (toto.txt):

    Pierre ZUFFEREY (1837) ép Marguerite ROSSIER (1850)
        Louis ZUFFEREY (1835) ép Madeleine PONT (1824)
            Georges Louis ZUFFEREY (1859-1931) ép Euphémie ZUFFEREY (1857-1933)
                Joseph Louis ZUFFEREY (1888-1967) ép Stéphanie SALAMIN (1891-1972)
                    Jean Louis Bertrand ZUFFEREY (1935-2018) ép  Anne Marie BEZENCON (1934)
                        Christian ZUFFEREY (1959) ép Véréna MARTY (1958)
                        Thierry ZUFFEREY (1962)
                        Isabelle ZUFFEREY (1965)

Running:
    python3 txt2ged.py toto.txt toto.ged

The script writes a GEDCOM file with individuals and families.
"""

import sys
import re
from pathlib import Path

# Regular expression to parse a person entry
# Example: "Pierre ZUFFEREY (1837) ép Marguerite ROSSIER (1850)"
PERSON_RE = re.compile(r"(?P<name>[^()]+?)\s*\((?P<birth>\d{4})(?:-(?P<death>\d{4}))?\)\s*(?:ép\s*(?P<spouse>.+))?$")

# Helper to generate unique IDs
class IdGenerator:
    def __init__(self, prefix):
        self.prefix = prefix
        self.counter = 1

    def next(self):
        id_ = f"@{self.prefix}{self.counter}@"
        self.counter += 1
        return id_

# Data structures
class Individual:
    def __init__(self, name, birth, death=None):
        self.id = None
        self.name = name.strip()
        self.birth = birth
        self.death = death
        self.famc = None  # family where this individual is a child
        self.fams = []     # families where this individual is a spouse

class Family:
    def __init__(self):
        self.id = None
        self.husband = None
        self.wife = None
        self.children = []

# Parse a line into Individual objects and spouse list

def parse_line(line):
    line = line.rstrip()
    match = PERSON_RE.match(line)
    if not match:
        raise ValueError(f"Line not in expected format: {line}")
    name = match.group('name').strip()
    birth = match.group('birth')
    death = match.group('death')
    spouse_str = match.group('spouse')
    person = Individual(name, birth, death)
    spouses = []
    if spouse_str:
        # spouses may be separated by 'ép' again? In input, only one spouse per line
        # but we support multiple separated by 'ép'
        for sp in re.split(r"\s+ép\s+", spouse_str):
            sp = sp.strip()
            if not sp:
                continue
            # Ensure leading spaces are removed before matching
            sp = sp.lstrip()
            # spouse string may contain name and years
            m = PERSON_RE.match(sp)
            if not m:
                raise ValueError(f"Spouse string not in expected format: {sp}")
            sp_name = m.group('name').strip()
            sp_birth = m.group('birth')
            sp_death = m.group('death')
            spouses.append(Individual(sp_name, sp_birth, sp_death))
    return person, spouses

# Main conversion function

def convert(input_path, output_path):
    # Read all lines preserving indentation
    lines = input_path.read_text(encoding='utf-8').splitlines()
    # Stack to keep track of parent families by indentation level
    stack = []  # each element: (indent_level, family)
    individuals = []
    families = []
    id_gen_ind = IdGenerator('I')
    id_gen_fam = IdGenerator('F')

    for raw_line in lines:
        if not raw_line.strip():
            continue
        # Count leading tabs
        indent = len(raw_line) - len(raw_line.lstrip('\t'))
        line = raw_line.lstrip('\t')
        person, spouses = parse_line(line)
        # Assign ID
        person.id = id_gen_ind.next()
        for sp in spouses:
            sp.id = id_gen_ind.next()
        # Create family for spouses
        if spouses:
            fam = Family()
            fam.id = id_gen_fam.next()
            fam.husband = person
            fam.wife = spouses[0]
            fam.children = []
            families.append(fam)
            person.fams.append(fam)
            spouses[0].fams.append(fam)
        else:
            fam = None
        # Handle parent-child relationship
        if stack:
            # Pop until we find a parent at a higher indentation level
            while stack and stack[-1][0] >= indent:
                stack.pop()
            if stack:
                parent = stack[-1][1]
                # Find the family where the parent is husband or wife
                parent_family = None
                for f in families:
                    if f.husband == parent or f.wife == parent:
                        parent_family = f
                        break
                if parent_family:
                    parent_family.children.append(person)
                    person.famc = parent_family
        # Push current individual onto stack for future children
        stack.append((indent, person))
        individuals.append(person)
        individuals.extend(spouses)

    # Write GEDCOM
    with output_path.open('w', encoding='utf-8') as f:
        f.write('0 HEAD\n')
        f.write('1 SOUR txt2ged.py\n')
        f.write('1 GEDC\n')
        f.write('2 VERS 5.5.1\n')
        f.write('2 FORM LINEAGE-LINKED\n')
        f.write('1 CHAR UTF-8\n')
        f.write('0 TRLR\n')
        # Write individuals
        for ind in individuals:
            f.write(f'0 {ind.id} INDI\n')
            f.write(f'1 NAME {ind.name}\n')
            f.write(f'1 BIRT\n')
            f.write(f'2 DATE {ind.birth}\n')
            if ind.death:
                f.write('1 DEAT\n')
                f.write(f'2 DATE {ind.death}\n')
            if ind.famc:
                f.write(f'1 FAMC {ind.famc.id}\n')
            for fam in ind.fams:
                f.write(f'1 FAMS {fam.id}\n')
        # Write families
        for fam in families:
            f.write(f'0 {fam.id} FAM\n')
            if fam.husband:
                f.write(f'1 HUSB {fam.husband.id}\n')
            if fam.wife:
                f.write(f'1 WIFE {fam.wife.id}\n')
            for child in fam.children:
                f.write(f'1 CHIL {child.id}\n')
    print(f"GEDCOM written to {output_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 txt2ged.py input.txt output.ged")
        sys.exit(1)
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    convert(input_path, output_path)
