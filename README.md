# Essais de petit script pour convertir un arbre généalogique de format texte en format gedcom avec l'IA (Copilot)
zf260206.1635, 260207.1700

## Buts
Faire un petit bench de démo pour tester les possibilités de *Copilot Agent* dans VScode pour écrire du code avec différents LLM, en particulier des LMM locaux avec Ollama.


## Utilisation
Choisir le bon LLM dans la fenêtre Copilot Agent à droite dans VSCode !

Ouvrir le *dernier* prompt, copier le *prompt* dans le chat Coplilot et cliquer sur la flèche *send*


## Exécution du script python
````
source venv/bin/activate
python txt2ged.py toto.txt toto.ged
````


## Tests
Il faut utiliser le viewer Topola pour la vérification de la qualité du fichier GEDCOM:

https://pewu.github.io/topola-viewer/



## Amélioration du prompt
Comme j'ai vu qu'il n'arrivait pas, à la 1ère fois, de trouver les dates de décès, je lui ai demandé pourquoi il avait un problème:

```
Petite question ?

Pourquoi tu n'as pas réussi du premier coup pour les dates
de décès ?

Mon prompt n'était pas assez précis ?

Aurais-tu une proposition de reformulation de mon prompt afin
que tu y arrives du 1er coup ?
```

Et il m'a répondu:
```
Le script initial ne traitait qu’une seule valeur entre
parenthèses : il l’interpréta toujours comme une année de 
naissance.
Dans ton fichier d’entrée, les dates de décès apparaissent sous
 la forme 1859-1931.
Comme le script ne reconnaissait pas le séparateur -, il ne
 pouvait pas extraire la seconde année.

Proposition de prompt plus explicite

Écris un script Python qui lit un fichier texte décrivant un
arbre généalogique (exemple : toto.txt) et génère un fichier
GEDCOM (toto.ged).
Chaque ligne contient un nom, une année de naissance et
optionnellement, une année de décès séparées par un tiret
((1837-1901)).
Le script doit conserver la hiérarchie indiquée par les
tabulations, gérer les conjoints séparés par ép, et écrire les
balises GEDCOM BIRT et DEAT pour les dates de naissance et
de décès.

Avec cette formulation, le besoin de gérer les deux dates est
explicitement indiqué.
```


