from outils.interface_grille import Vue
from copy import deepcopy

class Dessin:
    
    def __init__(self):
        self.haut = 4
        self.larg = 4
        self.vue = Vue(self.haut, self.larg*3+4, max_dim = 5)

        self.m_depart = [[1,  2,  3,  4], 
                    [5,  6,  7,  8],
                    [9 , 10, 11, 12],
                    [13, 14, 15, 16]]

        self.m_arrivee = [[12, 10, 11, 9], 
                     [16, 14, 5,  13],
                     [8,  6,  7,  15],
                     [4,  2,  3,  1]]
        
        self.m = deepcopy(self.m_depart)
        self.afficher_matrices()

    

    def afficher_matrices(self):
        for y in range(self.haut):
            for x in range(self.larg):
                self.vue.modifier_grille('texte', y, x, t = self.m_depart[y][x], tp = 13, visible = True)
                self.vue.modifier_grille('texte', y, x + 6, t = self.m[y][x], tp = 13, visible = True, c = (0,0,255)),
                self.vue.modifier_grille('texte', y, x + 12, t = self.m_arrivee[y][x], tp = 13, visible = True)

    def echanger_lignes(self, i, j) :
        self.m[i], self.m[j] = self.m[j], self.m[i]
        self.afficher_matrices()

    def echanger_colonnes(self, i, j) :
        for lig in range(self.haut):
            self.m[lig][j], self.m[lig][i] = self.m[lig][i], self.m[lig][j]
        self.afficher_matrices()   


    