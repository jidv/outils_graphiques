from outils.interface_grille import Vue
from random import shuffle, randint

class Dessin:
    
    def __init__(self):
        self.haut = 10
        self.larg = 13
        self.vue = Vue(self.haut, self.larg, max_dim = 6)
        self.matrice_fraises = self.matrice_depart()
        self.matrice_chemin = [[False for j in range(self.larg)] for i in range(self.haut)]
        self.afficher_matrices()
    
    def matrice_depart(self):
        nb_cells = self.haut*self.larg
        nb_fraises = randint(max(nb_cells/5, 1), min(2*nb_cells/5, nb_cells))
        matrice_en_long = [True] * nb_fraises + [False] * (nb_cells - nb_fraises)
        shuffle(matrice_en_long)
        matrice = [[matrice_en_long[self.larg * j + i] for i in range(self.larg)] for j in range(self.haut)]
        matrice[0][0] = False
        matrice[self.haut - 1][self.larg - 1] = False
        return matrice

    def afficher_matrices(self):
        chemin_img = './nourriture/fraise.png'
        for y in range(self.haut):
            for x in range(self.larg):
                self.vue.modifier_grille('fond', y, x,
                                         ci = (230, 250, 230) if self.matrice_chemin[y][x] else (255, 255, 255), 
                                         ce = (0,128,0), 
                                         visible = True)                    
                if self.matrice_fraises[y][x]:
                    self.vue.modifier_grille('image', y, x, cf = chemin_img, visible = True)
        self.vue.modifier_grille('texte', 0, 0, t = 'DEPART', visible = True)
        self.vue.modifier_grille('texte', self.haut-1, self.larg-1, t = 'ARRIVEE', visible = True)

    def chemin_robot_au_hasard(self) :
        chemin_en_long = [True] * (self.larg - 1) + [False] * (self.haut - 1)
        shuffle(chemin_en_long)
        matrice_chemin = [[False for j in range(self.larg)] for i in range(self.haut)]
        lig, col = 0, 0
        matrice_chemin[lig][col] = True
        for dep in chemin_en_long:
            if dep:
                col = col + 1
            else:
                lig = lig + 1
            matrice_chemin[lig][col] = True
        self.matrice_chemin = matrice_chemin
        self.afficher_matrices()
                
            