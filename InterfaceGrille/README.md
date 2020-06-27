### Fonctionnalités
- InterfaceGrille est une surcouche sur matplotlib qui permet d'afficher rapidement et simplement une grille 2D dont les cellules comportent au choix (cumulatif) :
	- une couleur de fond
	- une image
	- un texte
	- des murs séparateurs

- Il est également possible de récupérer certains évènements (clic sur une cellule, sur un mur, appui sur une touche du clavier).

- Il est possible d'exporter les graphiques produits au format PNG.
	
- Le dossier InterfaceGrille contient le module (`interface_grille.py`) ainsi qu'un notebook de prise en main.
	
- Le dossier images contient les images à afficher par le module. Un point doit retenir l'attention : l'initialisation du module nécessite de disposer de l'image `init.png` dans le dossier images	(à ne pas effacer).

- Le notebook `grille_deux_cas_classiques` présente deux cas classiques - plus élaborés que dans la prise en main - d'utilisation d'une grille (sudoku et labyrinthe). 
	

### Détails techniques

- Ce module nécessite de disposer de matplotlib (`pip install matplotlib`).

- Il a été conçu pour notebooks mais pourra aussi être utilisé dans un environnement python standard en mettant en commentaires éventuellement trois lignes dans l'en-tête du module.

