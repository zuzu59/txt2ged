#!/usr/bin/env python3
"""
Convert a simple tab-indented genealogical text file into a GEDCOM file.

Usage:
    python txt2ged.py input.txt output.ged

The input format is a plain text file where each line represents a person.
Indentation (tabs) indicates the parent-child relationship.  Each line has
the form::

    FirstName LastName (YYYY) ép SpouseFirstName SpouseLastName (YYYY)

The ``ép`` separator indicates the spouse.  Birth years may be a single
year or a range (e.g. ``1859-1931``); the first year is used as the birth
date.
"""

import re
import sys
from pathlib import Path


class Individual:
    def __init__(self, name, birth_year):
        self.id = None  # to be set later
        self.name = name
        self.birth_year = birth_year
        self.fams = []  # families where this person is a spouse
        self.famc = None  # family where this person is a child


class Family:
    def __init__(self, husb_id, wife_id):
        self.id = None  # to be set later
        self.husb_id = husb_id
        self.wife_id = wife_id
        self.children = []  # list of child individual ids


def parse_person_part(part):
    """Parse a string like 'Pierre ZUFFEREY (1837)' into name and birth year."""
    match = re.search(r"(.+?)\s*\(([^)]+)\)", part)
    if match:
        name = match.group(1).strip()
        birth = match.group(2).strip()
        # If birth is a range, take the first year
        birth_year = birth.split("-")[0]
    else:
        name = part.strip()
        birth_year = None
    return name, birth_year


def format_name(name):
    """Convert 'Pierre ZUFFEREY' to GEDCOM name format 'Pierre /ZUFFEREY/'."""
    parts = name.split()
    if len(parts) == 0:
        return " / /"
    last = parts[-1]
    first = " ".join(parts[:-1]) if len(parts) > 1 else ""
    return f"{first} /{last}/".strip()


def main(argv):
    if len(argv) != 3:
        print("Usage: python txt2ged.py input.txt output.ged")
        sys.exit(1)

    input_path = Path(argv[1])
    output_path = Path(argv[2])

    individuals = []  # list of Individual objects
    families = []  # list of Family objects

    # Stack to keep track of parent relationships: (level, person_id, family_id_of_person_as_spouse)
    stack = []

    # Counters for IDs
    indiv_counter = 1
    fam_counter = 1

    for raw_line in input_path.read_text(encoding="utf-8").splitlines():
        if not raw_line.strip():
            continue
        # Count leading tabs for indentation level
        level = 0
        while raw_line.startswith("\t"):
            level += 1
            raw_line = raw_line[1:]
        # Split person and spouse
        parts = raw_line.split(" ép ")
        person_part = parts[0]
        spouse_part = parts[1] if len(parts) > 1 else None
        # Parse person
        person_name, person_birth = parse_person_part(person_part)
        person = Individual(person_name, person_birth)
        person.id = f"@I{indiv_counter}@"
        indiv_counter += 1
        individuals.append(person)
        # Parse spouse if present
        spouse = None
        if spouse_part:
            spouse_name, spouse_birth = parse_person_part(spouse_part)
            spouse = Individual(spouse_name, spouse_birth)
            spouse.id = f"@I{indiv_counter}@"
            indiv_counter += 1
            individuals.append(spouse)
        # Create family for person and spouse
        if spouse:
            fam = Family(person.id, spouse.id)
            fam.id = f"@F{fam_counter}@"
            fam_counter += 1
            families.append(fam)
            person.fams.append(fam.id)
            spouse.fams.append(fam.id)
        else:
            fam = None
        # Link to parent if any
        if level > 0 and stack:
            # Find parent at level-1
            while stack and stack[-1][0] >= level:
                stack.pop()
            if stack:
                parent_level, parent_id, parent_family_id = stack[-1]
                # Add this person as child of parent's family
                if parent_family_id:
                    # Find family object
                    parent_fam = next((f for f in families if f.id == parent_family_id), None)
                    if parent_fam:
                        parent_fam.children.append(person.id)
                        person.famc = parent_family_id
        # Push current onto stack
        stack.append((level, person.id, fam.id if fam else None))

    # Write GEDCOM
    with output_path.open("w", encoding="utf-8") as out:
        # Individuals
        for ind in individuals:
            out.write(f"0 {ind.id} INDI\n")
            out.write(f"1 NAME {format_name(ind.name)}\n")
            if ind.birth_year:
                out.write("1 BIRT\n")
                out.write(f"2 DATE {ind.birth_year}\n")
            for fam_id in ind.fams:
                out.write(f"1 FAMS {fam_id}\n")
            if ind.famc:
                out.write(f"1 FAMC {ind.famc}\n")
        # Families
        for fam in families:
            out.write(f"0 {fam.id} FAM\n")
            out.write(f"1 HUSB {fam.husb_id}\n")
            out.write(f"1 WIFE {fam.wife_id}\n")
            for child_id in fam.children:
                out.write(f"1 CHIL {child_id}\n")

    print(f"GEDCOM file written to {output_path}")


if __name__ == "__main__":
    main(sys.argv)
