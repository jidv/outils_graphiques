### Fonctionnalités

- VizuArbre est une surcouche sur graphviz qui permet d'afficher rapidement et simplement un arbre binaire implémenté par une classe.

- Il est également possible d'afficher facilement des étiquettes secondaires sur les noeuds (typiquement l'ordre des visites lors d'un parcours). D'autres attributs (couleurs, forme des noeuds) sont également paramétrables facilement.

- Il est possible d'exporter les graphiques produits dans différents formats aussi bien bitmap (png, tiff) que vectoriels (svg et ps).

- Pour s'adapter à la classe d'arbre binaire définie par l'utilisateur, il faut néanmoins modifier l'en-tête du module `vizu_arbre.py` afin de spécifier l'interface implémentée par la classe :
	- la façon dont on accède au sous-arbre droit,
	- la façon dont on accède au sous-arbre gauche,
	- la façon dont on accède à l'étiquette de l'arbre,
	- la façon dont on teste l'arbre vide.

- Le dossier VizuArbre contient le module (`vizu_arbreb.py`) ainsi qu'un notebook de prise en main.
	
- Le dossier Algos_Arbres_en_NSI contient un notebook d'exemples d'utilisation de VizuArbre dans le cadre des éléments au programme de NSI.	

### Détails techniques

- Ce module nécessite de disposer de graphviz (`pip install graphviz`).

- Il a été conçu pour notebooks mais pourra aussi être utilisé dans un environnement python standard en modifiant la constante `JUPYTER_NOTEBOOK` située dans l'en-tête du fichier.