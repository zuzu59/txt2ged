# Essais de petit script pour convertir un arbre généalogique de format texte en format gedcom avec l'IA (Copilot)
zf260206.1635, 260207.1700

## Buts
Faire un petit bench de démo pour tester les possibilités de *Copilot Agent* dans VScode pour écrire du code avec différents LLM, en particulier des LMM locaux avec Ollama.


## Utilisation
Choisir le bon LLM dans la fenêtre Copilot Agent à droite dans VSCode !

Ouvrir le *dernier* prompt, copier le *prompt* dans le chat Coplilot et cliquer sur la flèche *send*


## Essais répétitifs avec différents modèles
Le problème avec les IA, c'est qu'elles ne sont pas *répétitifs* ! A chaque essais on peut avoir une réponse un peut différentes et ne pas réussir du premier coup le *bench*.

Afin d'être certains de pouvoir comparer les *benches*, avant le lancement, il faut effacer les fichiers générés avec:
````
rm toto.txt toto.ged txt2ged.py
````
Il faut aussi effacer la *pensée* du Copilot Agent en effacçant la session en haut à droite.<br>
Cela va obliger de tout recommencer depuis le début


## Exécution du script python
````
source venv/bin/activate
python txt2ged.py toto.txt toto.ged
````


## Tests
Il faut utiliser le viewer Topola pour la vérification de la qualité du fichier GEDCOM:

https://pewu.github.io/topola-viewer/

