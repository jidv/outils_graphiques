### Fonctionnalités
- VizuGraphe est une surcouche sur graphviz qui permet d'afficher rapidement et simplement un graphe défini par sa matrice d'adjacence ou sa liste d'adjacence.

- Il est également possible d'afficher facilement des étiquettes secondaires sur les sommets (typiquement l'ordre des visites lors d'un parcours). D'autres attributs (couleurs, forme des sommets) sont également paramétrables facilement.

- Il est possible d'exporter les graphiques produits dans différents formats aussi bien bitmap (png, tiff) que vectoriels (svg et ps).

- Pour s'adapter à la représentation choisie, le graphe fourni en argument peut être défini :
	- par une matrice d'adjacence booléenne,
	- par une matrice d'adjacence binaire,
	- par une matrice d'adjacence pondérée,
	- par une liste d'adjacence,
	- par une liste d'adjacence pondérée.
	
- Le dossier VizuGraphe contient le module (`vizu_graphe.py`) ainsi qu'un notebook de prise en main.
	
- Le dossier Algos_Graphes_en_NSI contient un notebook d'exemples d'utilisation de VizuGraphe dans le cadre des éléments au programme de NSI (plus deux modules : `xile.py` implémentant une File et une Pile et `generateurs.py` qui permettent de générer des graphes planaires à fin d'illustration.

### Détails techniques

- Ce module nécessite de disposer du logiciel [graphviz](https://graphviz.org/download/) ainsi que du module graphviz pour python (`pip install graphviz`).


- Il a été conçu pour notebooks mais pourra aussi être utilisé dans un environnement python standard en modifiant la constante `JUPYTER_NOTEBOOK` située dans l'en-tête du fichier.

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
