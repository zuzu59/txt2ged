#!/usr/bin/env python3
"""
txt2ged.py
~~~~~~~~~~~

This script reads a genealogical tree described in ``input.txt`` and
generates a GEDCOM file ``test.ged``.  The input format is a simple
indented list where each line is either a marriage (two names separated
by ``ép``) or a single person.  Indentation (4 spaces per level) defines
the parent/child relationship.

Example input::

    Pierre ZUFFEREY (1837) ép Marguerite ROSSIER (1850)
        Louis ZUFFEREY (1835) ép Madeleine PONT (1824)
            Georges Louis ZUFFEREY (1859-1931) ép Euphémie ZUFFEREY (1857-1933)
                Joseph Louis ZUFFEREY (1888-1967) ép Stéphanie SALAMIN (1891-1972)
                    Jean Louis Bertrand ZUFFEREY (1935-2018) ép Anne Marie BEZENCON (1934)
                        Christian ZUFFEREY (1959) ép Verena MARTY (1958)
                        Thierry ZUFFEREY (1962)
                        Isabelle ZUFFEREY (1965)

The script assigns unique identifiers to individuals (``@I1@``) and
families (``@F1@``) and writes a minimal GEDCOM file.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

INDENT = 4


class Person:
    def __init__(self, name: str, birth: str | None, death: str | None):
        self.name = name
        self.birth = birth
        self.death = death
        self.id: str | None = None

    def __repr__(self):
        return f"Person(id={self.id!r}, name={self.name!r})"


class Family:
    def __init__(self, husb: Person, wife: Person):
        self.husb = husb
        self.wife = wife
        self.children: list[Person] = []
        self.id: str | None = None

    def __repr__(self):
        return f"Family(id={self.id!r}, husb={self.husb.id!r}, wife={self.wife.id!r})"


def parse_person(text: str) -> Person:
    """Parse a string like ``Pierre ZUFFEREY (1837)`` or ``Georges Louis ZUFFEREY (1859-1931)``.

    Returns a :class:`Person` instance.
    """
    # Regex: name (birth-death?)
    m = re.match(r"(.+?)\s*\((\d{4})(?:-(\d{4}))?\)", text.strip())
    if not m:
        raise ValueError(f"Cannot parse person: {text!r}")
    name, birth, death = m.groups()
    return Person(name=name.strip(), birth=birth, death=death)


def main():
    input_path = Path("input.txt")
    if not input_path.exists():
        print("input.txt not found", file=sys.stderr)
        sys.exit(1)

    individuals: list[Person] = []
    families: list[Family] = []
    level_to_family: dict[int, Family | None] = {}

    # Read all lines
    lines = input_path.read_text(encoding="utf-8").splitlines()
    for raw_line in lines:
        if not raw_line.strip():
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        level = indent // INDENT
        line = raw_line.strip()
        if "ép" in line:
            # Marriage line
            left, right = line.split("ép", 1)
            husb = parse_person(left)
            wife = parse_person(right)
            individuals.extend([husb, wife])
            fam = Family(husb, wife)
            families.append(fam)
            level_to_family[level] = fam
            # Link the husband as a child of the parent family if this marriage is nested
            if level > 0:
                parent_fam = level_to_family.get(level - 1)
                if parent_fam:
                    parent_fam.children.append(husb)
        else:
            # Single person (child)
            child = parse_person(line)
            individuals.append(child)
            # Link to parent family
            parent_fam = level_to_family.get(level - 1)
            if parent_fam:
                parent_fam.children.append(child)
            level_to_family[level] = None

    # Assign IDs
    for idx, person in enumerate(individuals, start=1):
        person.id = f"@I{idx}@"
    for idx, fam in enumerate(families, start=1):
        fam.id = f"@F{idx}@"

    # Build mappings for spouse (FAMS) and child (FAMC) families
    person_fams_spouse: dict[str, list[str]] = {}
    person_fams_child: dict[str, list[str]] = {}
    for fam in families:
        for p in (fam.husb, fam.wife):
            person_fams_spouse.setdefault(p.id, []).append(fam.id)
        for child in fam.children:
            person_fams_child.setdefault(child.id, []).append(fam.id)

    # Build GEDCOM lines
    gedcom: list[str] = []
    gedcom.append("0 HEAD")
    gedcom.append("1 SOUR txt2ged")
    gedcom.append("1 GEDC")
    gedcom.append("2 VERS 5.5.1")
    gedcom.append("2 FORM LINEAGE")
    gedcom.append("0 @SUB@ SUBM")
    gedcom.append("1 NAME txt2ged")
    gedcom.append("1 BIRT")
    gedcom.append("2 DATE 01 JAN 2000")
    gedcom.append("0 TRLR")

    # Individuals
    for person in individuals:
        gedcom.append(f"0 {person.id} INDI")
        gedcom.append(f"1 NAME {person.name}")
        # Add FAMS tags for families where this person is a spouse
        for fam_id in person_fams_spouse.get(person.id, []):
            gedcom.append(f"1 FAMS {fam_id}")
        # Add FAMC tags for families where this person is a child
        for fam_id in person_fams_child.get(person.id, []):
            gedcom.append(f"1 FAMC {fam_id}")
        if person.birth:
            gedcom.append("1 BIRT")
            gedcom.append(f"2 DATE {person.birth}")
        if person.death:
            gedcom.append("1 DEAT")
            gedcom.append(f"2 DATE {person.death}")

    # Families
    for fam in families:
        gedcom.append(f"0 {fam.id} FAM")
        gedcom.append(f"1 HUSB {fam.husb.id}")
        gedcom.append(f"1 WIFE {fam.wife.id}")
        for child in fam.children:
            gedcom.append(f"1 CHIL {child.id}")

    # Write to test.ged
    output_path = Path("test.ged")
    output_path.write_text("\n".join(gedcom) + "\n", encoding="utf-8")
    print(f"GEDCOM written to {output_path}")


if __name__ == "__main__":
    main()
