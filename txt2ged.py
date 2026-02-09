#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from datetime import datetime

class Person:
    def __init__(self, given_name, surname, birth_year, death_year=None):
        self.given_name = given_name
        self.surname = surname
        self.birth_year = birth_year
        self.death_year = death_year
        self.id = None
        self.fams = []  # Families where this person is a spouse
        self.famc = None  # Family where this person is a child
    
    def __repr__(self):
        return f"{self.given_name} {self.surname} ({self.birth_year}-{self.death_year or ''})"

class Family:
    def __init__(self, husband, wife):
        self.husband = husband
        self.wife = wife
        self.children = []
        self.id = None
    
    def __repr__(self):
        return f"Family {self.id}: {self.husband} & {self.wife}, children: {len(self.children)}"

def parse_person(text):
    """Parse a person string like 'Pierre ZUFFEREY (1837)' or 'Georges Louis ZUFFEREY (1859-1931)'"""
    # Pattern: Name SURNAME (birth) or Name SURNAME (birth-death)
    pattern = r'^(.+?)\s+([A-Z]+)\s+\((\d{4})(?:-(\d{4}))?\)$'
    match = re.match(pattern, text.strip())
    if match:
        given_name = match.group(1).strip()
        surname = match.group(2).strip()
        birth_year = match.group(3)
        death_year = match.group(4)
        return Person(given_name, surname, birth_year, death_year)
    return None

def parse_line(line):
    """Parse a line and return indentation level, person1, person2 (spouse if any)"""
    # Count leading spaces (4 spaces = 1 level)
    indent = len(line) - len(line.lstrip())
    level = indent // 4
    
    content = line.strip()
    
    # Check if there's a marriage (ép)
    if ' ép ' in content:
        parts = content.split(' ép ')
        person1 = parse_person(parts[0])
        person2 = parse_person(parts[1]) if len(parts) > 1 else None
        return level, person1, person2
    else:
        person1 = parse_person(content)
        return level, person1, None

def generate_gedcom(input_file, output_file):
    """Generate GEDCOM file from input text file"""
    
    # Read and parse input
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    all_persons = []
    all_families = []
    person_counter = 1
    family_counter = 1
    
    # Stack to keep track of persons at each level
    level_stack = {}
    
    for line in lines:
        if not line.strip():
            continue
        
        level, person1, person2 = parse_line(line)
        
        if person1:
            person1.id = f"I{person_counter}"
            person_counter += 1
            all_persons.append(person1)
            
            # If there's a spouse, create them and a family
            if person2:
                person2.id = f"I{person_counter}"
                person_counter += 1
                all_persons.append(person2)
                
                # Create family for this couple
                family = Family(person1, person2)
                family.id = f"F{family_counter}"
                family_counter += 1
                all_families.append(family)
                
                # Link persons to this family as spouses
                person1.fams.append(family.id)
                person2.fams.append(family.id)
                
                # Store this couple at current level for children
                level_stack[level] = (person1, person2, family)
            else:
                # Single person (no spouse mentioned)
                level_stack[level] = (person1, None, None)
            
            # Link to parent family if this person has parents (level > 0)
            if level > 0 and (level - 1) in level_stack:
                parent_tuple = level_stack[level - 1]
                if parent_tuple and len(parent_tuple) > 2 and parent_tuple[2]:
                    parent_family = parent_tuple[2]
                    # This person is a child of the parent family
                    person1.famc = parent_family.id
                    parent_family.children.append(person1)
                    
                    # If person1 has a spouse, the spouse is also a child of parent family
                    # Wait, no - only person1 is the child
                    # person2 is not a child of person1's parents
    
    # Write GEDCOM file
    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("0 HEAD\n")
        f.write("1 SOUR txt2ged.py\n")
        f.write("1 GEDC\n")
        f.write("2 VERS 5.5.1\n")
        f.write("2 FORM LINEAGE-LINKED\n")
        f.write("1 CHAR UTF-8\n")
        f.write(f"1 DATE {datetime.now().strftime('%d %b %Y').upper()}\n")
        
        # Individuals
        for person in all_persons:
            f.write(f"0 @{person.id}@ INDI\n")
            f.write(f"1 NAME {person.given_name} /{person.surname}/\n")
            f.write(f"2 GIVN {person.given_name}\n")
            f.write(f"2 SURN {person.surname}\n")
            
            # Birth
            if person.birth_year:
                f.write("1 BIRT\n")
                f.write(f"2 DATE {person.birth_year}\n")
            
            # Death
            if person.death_year:
                f.write("1 DEAT\n")
                f.write(f"2 DATE {person.death_year}\n")
            
            # Family as child
            if person.famc:
                f.write(f"1 FAMC @{person.famc}@\n")
            
            # Families as spouse
            for fam_id in person.fams:
                f.write(f"1 FAMS @{fam_id}@\n")
        
        # Families
        for family in all_families:
            f.write(f"0 @{family.id}@ FAM\n")
            f.write(f"1 HUSB @{family.husband.id}@\n")
            f.write(f"1 WIFE @{family.wife.id}@\n")
            
            for child in family.children:
                f.write(f"1 CHIL @{child.id}@\n")
        
        # Trailer
        f.write("0 TRLR\n")
    
    print(f"GEDCOM file generated: {output_file}")
    print(f"Total persons: {len(all_persons)}")
    print(f"Total families: {len(all_families)}")
    print("\nFamilies structure:")
    for family in all_families:
        print(f"  {family}")

if __name__ == "__main__":
    generate_gedcom("input.txt", "test.ged")
