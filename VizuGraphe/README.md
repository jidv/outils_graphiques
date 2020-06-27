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

- Ce module nécessite de disposer de graphviz (`pip install graphviz`).

- Il a été conçu pour notebooks mais pourra aussi être utilisé dans un environnement python standard en modifiant la constante `JUPYTER_NOTEBOOK` située dans l'en-tête du fichier.