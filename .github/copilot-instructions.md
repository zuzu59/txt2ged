---
applyTo: "**/*.py"
---

# Instructions Agent : script pour convertir un arbre généalogique de format texte en format gedcom 

## 1. Contexte du Projet
- **Objectif** : Écrire un script en Python3, nommé `txt2ged.py`, qui lit un fichier texte décrivant un arbre généalogique (`input.txt`) et génère un fichier GEDCOM (`test.ged`) tout en préservant 
l'intégrité des liens de parenté.
- **État actuel** : Projet vide. Première étape : créer `txt2ged.py` et l'architecture modulaire.
- **Workflow global** : Import successif (Extraction) -> Stockage SQLite (validation l'intégrité des liens de parenté) -> Export GEDCOM (Output).


## 2. Architecture Technique (Pipeline)
L'Agent doit implémenter le flux suivant :
1. **Extraction** : Parser chaque individu et famille depuis le fichier texte source (`input.txt`). Chaque individu/famille est transformé en un objet Python avec les attributs pertinents (nom, prénom, date de naissance, liens familiaux).
2. **Staging SQLite** : Insérer les données dans une base `sqlite3` (en mémoire ou fichier).
3. **Upsert Logique** : Valider depuis SQLite la structure hiérarchique et les liens de parenté à chaque insertion. 
4. **Export** : Reconstruire l'objet `Gedcom` final depuis SQLite et l'enregistrer avec la lib python GEDCOM.


## 4. Règles Métier & Intégrité
### Gestion des Individus
- **Mapping des IDs** : Créer une table de correspondance entre les XREFs originaux (`@I1@`, `@F1@`) et les IDs auto-incrémentés de SQLite.

### Validation des Liens de Parenté
- **Parenté** : Chaque individu doit être lié à une famille via les rôles `HUSB`, `WIFE`, `CHIL`. 
- **Intégrité** : Toute tentative de créer une famille sans au moins un parent ou un enfant doit être rejetée avec une exception.
- **Non-inferrence du Genre** : Ne pas assigner de genre basé sur les noms. Les rôles dans les familles sont déterminés uniquement par la structure hiérarchique et les séparateurs `ep`/`ép`.

## 5. Schéma de Données SQLite (Recommandé)
- `individuals` : (id, nom, prenom, date_naiss, sexe, id_origine_gedcom)
- `families` : (id, id_mari, id_femme, date_mariage, lieu_mariage)
- `family_links` : (id_famille, id_individu, role) -- roles: 'HUSB', 'WIFE', 'CHIL'

## 6. Standards de Développement
- **Style** : Programmation orientée objet (classes pour `Individual`, `Family`, `DatabaseManager`).
- **Qualité** : Annotations de type obligatoires, Docstrings (format Google), gestion des erreurs via Exceptions.
- **Tests** : Utiliser `pytest`. Créer des tests unitaires pour chaque critère de matching.
- **Journalisation** : Logs détaillés de chaque fusion pour traçabilité (Audit Trail).

## 7. Commandes de Référence
- Installation : `pip install python-gedcom`
- Exécution : `python3 fusion.py input.txt test.ged
- Validation : Utiliser `pytest` pour valider la non-régression.



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
