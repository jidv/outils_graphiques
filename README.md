# outils_graphiques

Outils d'affichages graphiques adaptés au programme de NSI.

Objectif principal : commandes simples et faciles d'accès, adaptées à tous les profils d'élèves.
 
- Grille2D : interface d'affichage d'une grille 2D (pour labyrinthes, sudokus, mots croisés, échecs, morpions, bataille navale etc.) proposant également la gestion de quelques évènements. Basée sur le module matplotlib.

- VizuGraphe : interface d'affichage de graphes (une seule instruction d'affichage suffit). Ce module nécessite de disposer du logiciel [graphviz](https://graphviz.org/download/) ainsi que du module graphviz pour python (`pip install graphviz`).


- VizuArbre : interface d'affichage d'arbres binaires (une seule instruction d'afficahge suffit). Ce module nécessite de disposer du logiciel [graphviz](https://graphviz.org/download/) ainsi que du module graphviz pour python (`pip install graphviz`).

### Installation de graphviz sous Windows

- On évitera ce qui est indiqué sur la page [Downloads](https://graphviz.org/download/) de Graphviz.
Il vaut mieux préférer l'installeur .msi de la version 2.38 :  

**[installeur MSI pour Windows](https://graphviz.gitlab.io/_pages/Download/Download_windows.html)** 

- Une fois l'installation du logiciel effectuée, on ajoutera graphviz au Path Windows (pour que python puisse le trouver) :

	- Paramètres > Propriétés Système > Variables d'environnement > Variables système > Path > Modifier > Nouveau 
	
	- copier le chemin vers l'installation de graphviz (sans doute "C:\Program Files (x86)\Graphviz2.38\bin")
	
- Il suffira ensuite d'installer le module permettant à Python de communiquer avec le logiciel Graphviz :

	- `pip install graphviz`

