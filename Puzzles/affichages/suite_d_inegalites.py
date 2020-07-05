from outils.interface_grille import Vue
from random import choice, randint

class Dessin:
    
    def __init__(self):
        self.k = 5
        self.haut = 3
        self.larg = 4*self.k+1
        self.vue = Vue(self.haut, self.larg, max_dim = 7)

        self.inegalites = ['' if i%2 == 0 else choice(('<', '>')) for i in range(self.larg)]
        self.nombres = [str(randint(0,99)) if i>= self.k and i <= 3*self.k else '' for i in range(self.larg)]
        self.fonds = [(245, 245, 245) if i%2 == 0 else (255, 255, 255) for i in range(self.larg)]
        
        self.afficher_matrices()

    

    def afficher_matrices(self):
        for y in range(self.haut):
            for x in range(self.larg):
                self.vue.modifier_grille('texte', 0, x, t = self.nombres[x], tp = 13, visible = True)
                self.vue.modifier_grille('texte', 2, x, t = self.inegalites[x], tp = 13, visible = True)
                self.vue.modifier_grille('fond', 2, x, c = self.fonds[x], visible = True)
                

    def inserer(self, nombre, position) :
        if str(nombre) in self.nombres and 0 <= position and position < 2*self.k+1 and position%2 == 0:
            self.vue.modifier_grille('texte', 2, 2*position, t = str(nombre), tp = 13, visible = True)

