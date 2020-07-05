from random import choice
from outils.interface_grille import Vue
#code pas propre : passé en POO après début non POO
        

class Dessin:
    def __init__(self):
        self.haut = 8
        self.larg = 8
        self.vue = Vue(self.haut, self.larg, max_dim = 5)
        self.xcoq = 7
        self.ycoq = 0
        self.xf = 0
        self.yf = 7
        self.fond = self.generer_matrice()
        self.redessiner_matrice()
        

    def generer_matrice(self):
        fond = [['B' if (x+y)%2 == 0 else 'N' for x in range(self.larg)] for y in range(self.haut)]
        return fond

    def redessiner_matrice(self):
        dico = {'N':(225, 225, 225), 'B': (245, 245, 245)}
        for lig in range(self.haut):
            for col in range(self.larg):
                self.vue.modifier_grille('fond', lig, col, c = dico[self.fond[lig][col]], visible = True)
                if lig == self.ycoq and col == self.xcoq :
                    self.vue.modifier_grille('image', lig, col, cf = './persos/coq.png', 
                                                                       visible = True)
                if lig == self.yf and col == self.xf :
                    self.vue.modifier_grille('image', lig, col, cf = './persos/Fermiere.png', 
                                                                       visible = True)
 
     

