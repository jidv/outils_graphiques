from outils.interface_grille import Vue
from random import shuffle

class Dessin:
    
    def __init__(self):
        self.haut = 10
        self.larg = 3
        self.vue = Vue(self.haut, self.larg, max_dim = 6)
        self.m = ['R'] * self.haut + ['G'] * self.haut + ['B'] * self.haut
        shuffle(self.m)
        
        self.matrice = [[self.m[self.larg * j + i] for i in range(self.larg)] for j in range(self.haut)]
        self.afficher_matrices()


    def afficher_matrices(self):
        dico_chemins = {'R':'./pions/pion_rouge.png', 'G':'./pions/pion_vert.png', 'B':'./pions/pion_bleu.png'}
        for y in range(self.haut):
            for x in range(self.larg):
                self.vue.modifier_grille('image', y, x, cf = dico_chemins[self.matrice[y][x]],
                                                       visible = True)

    def echanger_couleurs(self, col, lig_a, lig_b) :
        assert col in range(self.larg) and lig_a in range(self.haut) and lig_b in range(self.haut)
        self.matrice[lig_a][col], self.matrice[lig_b][col] = self.matrice[lig_b][col], self.matrice[lig_a][col]
        self.afficher_matrices()  