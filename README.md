# outils_graphiques

Outils d'affichages graphiques adaptés au programme de NSI & collection d'énoncés classiques d'algorithmique en lien avec le programme de NSI.

 
- Grille2D : interface d'affichage d'une grille 2D (pour labyrinthes, sudokus, mots croisés, échecs, morpions, bataille navale etc.) proposant également la gestion de quelques évènements. Basée sur le module matplotlib.

- VizuGraphe : interface d'affichage de graphes (une seule instruction d'affichage suffit). Ce module nécessite de disposer du logiciel [graphviz](https://graphviz.org/download/) ainsi que du module graphviz pour python (`pip install graphviz`).


- VizuArbre : interface d'affichage d'arbres binaires (une seule instruction d'afficahge suffit). Ce module nécessite de disposer du logiciel [graphviz](https://graphviz.org/download/) ainsi que du module graphviz pour python (`pip install graphviz`).


- Puzzles : collection de situations algorithmiques classiques en lien avec le programme de NSI, avec un index par notion (`0_INDEX.ipynb`).

### Installation de graphviz sous Windows (méthode 1)

- On se rendra sur la page dédiée : [Downloads](https://graphviz.org/download/) de Graphviz.

	- Normalement le lien pour l'installeur de la version stable (parfois rompu lors des MAJ des dépôts) vous conduit sur cette page :
	- (https://www2.graphviz.org/Packages/stable/windows/). Il faudra ensuite suivre les liens pour parvenir à 
	- (https://www2.graphviz.org/Packages/stable/windows/10/cmake/Release/)

- Lors de l'installation du logiciel, demandez bien à actualiser le PATH Windows.

- Une fois le logiciel installé, il vous faut installer le module permettant à Python de communiquer avec le logiciel Graphviz :

	- `pip install graphviz`
	
### Installation de graphviz sous Windows (méthode 2)

- Si ce qui est indiqué sur la page [Downloads](https://graphviz.org/download/) de Graphviz conduit au dépôt Github (cela arrive parfois lorsque Graphviz effectue une MAJ sur ses serveus de dépôt) on préférera l'installeur .msi de la version 2.38 qui est toujours disponible ici :  

**[installeur MSI pour Windows](https://graphviz.gitlab.io/_pages/Download/Download_windows.html)** 


- Une fois l'installation du logiciel effectuée, on ajoutera alors graphviz au Path Windows (pour que python puisse le trouver) manuellement car la 2.38 ne le propose pas lors de l'installation :

	- Paramètres > Propriétés Système > Variables d'environnement > Variables système > Path > Modifier > Nouveau 
	
	- copier le chemin vers l'installation de graphviz (sans doute "C:\Program Files (x86)\Graphviz2.38\bin")
	
- Il suffira ensuite d'installer le module permettant à Python de communiquer avec le logiciel Graphviz :

	- `pip install graphviz`
    
### Installation de graphviz sous Debian/Ubuntu

- `sudo apt install graphviz`

- Il suffira ensuite d'installer le module permettant à Python de communiquer avec le logiciel Graphviz :

	- `pip install graphviz`

	
### DERNIERES MODIFICATIONS :

- 09/07/2020
	- Correction d'un manquement dans les algorithmes de rééquilibrage des arbres binaires (erreur de renommage et mauvaise gestion du cas du rééquilibrage de l'arbre vide).

- 08/07/20
	- Correction d'un manquement ne permettant pas de modifier les paramètres par défaut lors de l'initialisation des arbres.

- 05/07/20
	- Possibilité de modifier tous les attributs des noeuds et sommets dès la construction des arbres binaires ou graphes.
	- Possibilité de sélectionner tous les noeuds des arbres binaires pour modification éventuelle, y compris lorsqu'ils ont même étiquette.
	- Ajout d'une collection de problèmes classiques d'algorithmique en lien avec le programme de NSI.

### TODO

- Alternative Networkx et non pas Graphviz pour réduire dépendance logicielle et faciliter l'installation en établissement,
- Compléter collection de problèmes classiques.









[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jidv/outils_graphiques/master)






