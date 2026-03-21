---
applyTo: "**/*.py"
---

# Instructions Agent : txt2ged - convertisseur texte -> GEDCOM

## 1. Objectif fonctionnel
1. Lire un fichier source `input.txt` décrivant un arbre généalogique (texte indenté).
2. Générer un fichier GEDCOM valide (`test.ged`) en préservant tous les liens de parenté.
3. Viser robustesse, traçabilité, tests et conformité GEDCOM 5.5.1.

## 2. Pipeline recommandé
1. Extraction (parser) :
   - Interpréter la hiérarchie par indentation (4 espaces = génération).
   - Distinguer individus, familles, parents/enfants, conjoints (`ep` / `ép`).
   - Construire objets métiers : `Individual`, `Family`, `FamilyLink`.
2. Staging SQLite :
   - Base mémoire ou fichier avec tables `individuals`, `families`, `family_links`.
   - Mappage des XREFs GEDCOM (`@I1@`, `@F1@`) vers IDs internes.
3. Validation et upsert :
   - Chaque insertion vérifie l’intégrité : un parent ET au moins un enfant pour chaque famille, pas de références orphelines.
   - Rejet avec Exception pour violation de règles métier.
4. Export GEDCOM :
   - Utilisation de la lib python-gedcom pour l'exportation.
   - Reconstituer INDI/FAM avec cross-refs correctes.
   - Générer un GEDCOM 5.5.1 compatible.

## 3. Règles métier
- Ne jamais inférer le sexe depuis le nom.
- Roles `HUSB`, `WIFE`, `CHIL` définis uniquement par structure et séparateurs.
- Famille invalide = erreur (génération, insertion SQL, ou marquage explicite).
- IDs persistés et traçables via logs.

## 4. Schéma SQLite
- `individuals` : (id INTEGER PRIMARY KEY, nom, prenom, date_naiss, sexe, id_origine_gedcom)
- `families` : (id INTEGER PRIMARY KEY, id_mari, id_femme, date_mariage, lieu_mariage)
- `family_links` : (id INTEGER PRIMARY KEY, id_famille, id_individu, role CHECK(role IN ('HUSB','WIFE','CHIL')))
- `xref_map` : (xref TEXT UNIQUE, table TEXT, row_id INTEGER)

## 5. Architecture du code
- Classes clefs : `Individual`, `Family`, `FamilyLink`, `DatabaseManager`, `GedcomExporter`, `TxtParser`.
- Docstrings Google style + type hints (`typing`).
- Exceptions métiers : `InvalidFamilyException`, `MissingPersonException`, `ParserError`.
- Logging audit : `logging.getLogger('txt2ged')` + niveau DEBUG.

## 6. Qualité et tests
- Framework : `pytest`.
- Couverture minimale : parsing, base SQLite, validation, export GEDCOM.
- Cas à tester : famille sans parent, sans enfant, références XREF manquantes, couple avec un seul époux (possible si explicite), multi-époux selon need.

## 7. Commandes
- Installation : `pip install python-gedcom`
- Exécution : `python3 txt2ged.py input.txt test.ged`
- Tests : `pytest -q`
- Clean : `rm -f test.ged`.

---

# Directives supplémentaires pour l’agent

- Pas de génération de code basée sur `test.ged` déjà existant (benchmark doit rester déterministe).
- Si le fichier `input.txt` est mal formé, échouer proprement et documenter le problème.
- Prioriser lisibilité et maintenabilité sur abscondes optimisations.

