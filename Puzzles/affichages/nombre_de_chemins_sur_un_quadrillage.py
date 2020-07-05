from random import randint
from outils.interface_grille import Vue


class Dessin:
    
    def __init__(self):
        self.haut, self.larg = 4, 5
        self.vue = Vue(self.haut, self.larg, max_dim = 5)
        self.nouveau()


    def generer_matrices(self):
        fonds = [[True for x in range(self.larg)] for y in range(self.haut)]
        aretes_v = [[True for x in range(self.larg+1)] for y in range(self.haut)]
        aretes_h = [[True for x in range(self.larg)] for y in range(self.haut+1)]
        trous = [ (x, randint(1, self.haut-1)) for x in range(1, self.larg, 3) ]
        for (x, y) in trous:
            for dy in (0, 1):
                for dx in (0, 1):
                    fonds[y - dy][x - dx] = False
            for dy in (0, 1):   
                aretes_v[y-dy][x] = False
            for dx in (0, 1):
                aretes_h[y][x-dx] = False
        return fonds, aretes_v, aretes_h

    def redessiner_matrices(self, f, av, ah):
        for y in range(self.haut):
            for x in range(self.larg):
                self.vue.modifier_grille('fond', y, x, c = (180, 255, 180) if f[y][x] else (255, 180, 180), 
                                                  visible = True)
        for y in range(self.haut):
            for x in range(self.larg+1):    
                self.vue.modifier_grille('mur_v', y, x, ci = (255, 255, 180), 
                                                   visible = True if av[y][x] else False)

        for y in range(self.haut+1):
            for x in range(self.larg):    
                self.vue.modifier_grille('mur_h', y, x, ci = (255, 255, 180), 
                                                   visible = True if ah[y][x] else False)
    def nouveau(self):   
        f, av, ah = self.generer_matrices()
        self.redessiner_matrices(f, av, ah)
