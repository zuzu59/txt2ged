#!/usr/bin/env python3
"""
Script to convert a simple genealogical text file into a GEDCOM file.

The input format is a plain text file where each line represents a person.
Tabs indicate the depth in the family tree.
Each line contains a name, a birth year in parentheses, and optionally a death year
in the same parentheses separated by a dash.  Spouses are separated by the
character sequence "ép".

Example line:
    Pierre ZUFFEREY (1837) ép Marguerite ROSSIER (1850)

The script writes a GEDCOM file with INDI records for each person and spouse
and FAM records linking parents and children.
"""

import sys
import re
from collections import defaultdict

# Regular expression to parse a person entry: name and dates
PERSON_RE = re.compile(r"^(.+?)\s*\((\d{4})(?:-(\d{4}))?\)\s*$")

class Node:
    """Represents a person (and optional spouse) in the tree."""
    def __init__(self, person_name, birth, death, spouse_name=None, spouse_birth=None, spouse_death=None):
        self.person_name = person_name
        self.birth = birth
        self.death = death
        self.spouse_name = spouse_name
        self.spouse_birth = spouse_birth
        self.spouse_death = spouse_death
        self.children = []  # list of Node
        self.individual_id = None
        self.spouse_id = None
        self.family_id = None
        self.parent_family_id = None


def parse_line(line):
    """Parse a line into a Node.

    Returns a tuple (depth, Node).
    """
    # Count leading tabs for depth
    depth = len(line) - len(line.lstrip("\t"))
    content = line.lstrip("\t").strip()
    # Split by the word "ép" with optional surrounding whitespace
    parts = [p.strip() for p in re.split(r"\s*\bép\b\s*", content)]
    # Parse first part
    m = PERSON_RE.match(parts[0])
    if not m:
        raise ValueError(f"Cannot parse person part: {parts[0]}")
    person_name, birth, death = m.group(1), int(m.group(2)), m.group(3)
    death = int(death) if death else None
    spouse_name = spouse_birth = spouse_death = None
    if len(parts) > 1:
        m2 = PERSON_RE.match(parts[1])
        if not m2:
            raise ValueError(f"Cannot parse spouse part: {parts[1]}")
        spouse_name, spouse_birth, spouse_death = m2.group(1), int(m2.group(2)), m2.group(3)
        spouse_death = int(spouse_death) if spouse_death else None
    node = Node(person_name, birth, death, spouse_name, spouse_birth, spouse_death)
    return depth, node


def build_tree(lines):
    """Build a tree of Node objects from the input lines.

    Returns a list of root nodes.
    """
    roots = []
    stack = []  # stack of (depth, node)
    for line in lines:
        if not line.strip():
            continue
        depth, node = parse_line(line)
        # Adjust stack to current depth
        while stack and stack[-1][0] >= depth:
            stack.pop()
        if stack:
            parent_node = stack[-1][1]
            parent_node.children.append(node)
        else:
            roots.append(node)
        stack.append((depth, node))
    return roots


def assign_ids(roots):
    """Assign unique IDs to individuals and families.

    Returns dictionaries mapping nodes to IDs.
    """
    indiv_counter = 1
    fam_counter = 1
    def traverse(node):
        nonlocal indiv_counter, fam_counter
        node.individual_id = f"@I{indiv_counter}@"
        indiv_counter += 1
        if node.spouse_name:
            node.spouse_id = f"@I{indiv_counter}@"
            indiv_counter += 1
        node.family_id = f"@F{fam_counter}@"
        fam_counter += 1
        for child in node.children:
            child.parent_family_id = node.family_id
            traverse(child)
    for root in roots:
        traverse(root)
    for root in roots:
        traverse(root)


def write_gedcom(roots, output_path):
    with open(output_path, "w", encoding="utf-8") as out:
        # Write families first
        def write_family(node):
            out.write(f"0 {node.family_id} FAM\n")
            if node.spouse_name:
                out.write(f"1 HUSB {node.individual_id}\n")
                out.write(f"1 WIFE {node.spouse_id}\n")
            else:
                out.write(f"1 HUSB {node.individual_id}\n")
            for child in node.children:
                out.write(f"1 CHIL {child.individual_id}\n")
            for child in node.children:
                write_family(child)

        for root in roots:
            write_family(root)

        # Write individuals
        def write_individual(node):
            out.write(f"0 {node.individual_id} INDI\n")
            out.write(f"1 NAME {node.person_name}\n")
            out.write("1 BIRT\n")
            out.write(f"2 DATE {node.birth}\n")
            if node.death:
                out.write("1 DEAT\n")
                out.write(f"2 DATE {node.death}\n")
            # Parent family reference
            if node.parent_family_id:
                out.write(f"1 FAMC {node.parent_family_id}\n")
            # Family reference for parents
            if node.family_id:
                out.write(f"1 FAMS {node.family_id}\n")
            if node.spouse_name:
                out.write(f"0 {node.spouse_id} INDI\n")
                out.write(f"1 NAME {node.spouse_name}\n")
                out.write("1 BIRT\n")
                out.write(f"2 DATE {node.spouse_birth}\n")
                if node.spouse_death:
                    out.write("1 DEAT\n")
                    out.write(f"2 DATE {node.spouse_death}\n")
                # Spouse family reference
                if node.family_id:
                    out.write(f"1 FAMS {node.family_id}\n")
            for child in node.children:
                write_individual(child)

        for root in roots:
            write_individual(root)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 txt2ged.py input.txt output.ged")
        sys.exit(1)
    input_path, output_path = sys.argv[1], sys.argv[2]
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    roots = build_tree(lines)
    assign_ids(roots)
    write_gedcom(roots, output_path)
    print(f"GEDCOM file written to {output_path}")

if __name__ == "__main__":
    main()
