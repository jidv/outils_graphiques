from random import choice
from outils.interface_grille import Vue

        

class Dessin:
    
    def __init__(self):
        self.n = 17
        self.plateau = [choice(('R', 'B')) for i in range(self.n)]
        self.vue = Vue(1, self.n)
        self.redessiner_plateau()

    def echanger(self, i, j):
        self.plateau[i], self.plateau[j] = self.plateau[j], self.plateau[i]
        self.redessiner_plateau()

    def redessiner_plateau(self):
        dico = {'R':'./pions/pion_rouge.png', 'B': './pions/pion_blanc.png'}
        lig = 0
        for col in range(self.n):
            self.vue.modifier_grille('fond', lig, col, c = (220, 220, 220), visible = True)
            self.vue.modifier_grille('image', lig, col, cf = dico[self.plateau[col]], visible = True)

    

