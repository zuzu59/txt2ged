# Essais de petit script pour convertir un arbre généalogique de format texte en format gedcom avec l'IA (Copilot)
zf260206.1635, 260208.1528

## Buts
Faire un petit bench de démo pour tester les possibilités de *Copilot Agent* dans VScode pour écrire du code avec différents LLM, en particulier des LMM locaux avec Ollama.


## Utilisation
Choisir le bon LLM dans la fenêtre Copilot Agent à droite dans VSCode !

Copier le contenu du fichier **prompt.txt** ou **prompt-minimal.txt** dans le chat Coplilot, ajouter comme annexe le fichier **input.txt** et cliquer sur la flèche **send**


## Essais répétitifs avec différents modèles
Le problème avec les *IA*, c'est qu'elles ne sont pas *répétitifs* ! A chaque essais on peut avoir une réponse un peut différentes et ne pas réussir du premier coup le *bench*.

Afin d'être certains de pouvoir comparer les *benches*, avant le lancement, il faut effacer les fichiers générés avec:
````
rm test.ged txt2ged.py
````
Il faut aussi effacer la *pensée* du Copilot Agent en effacçant la session en haut à droite.<br>
Cela va obliger de tout recommencer depuis le début


## Validations du GEDCOM
Il faut utiliser le viewer Topola pour la vérification *visuelle* de la qualité du fichier GEDCOM:

https://pewu.github.io/topola-viewer/

Et *Ged-Inline* pour la vérification *syntaxique* de la qualité du fichier GEDCOM:

https://ged-inline.org/


## Remarques
J'ai constaté, avec les modèles en local sur Ollama, que plus le *prompt* était détaillé, plus il perdait les pédalles et n'arrivait à rien. Si on fait un *prompt* minimaliste, il s'en sort quasiment du 1er coup !
