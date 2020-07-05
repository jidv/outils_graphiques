from random import choice
from outils.interface_grille import Vue
#code pas propre : passé en POO après début non POO
        

class Plateau:
    def __init__(self, dessin):
        self.x = 0
        self.y = 7
        self.dessin = dessin
        self.fond = self.generer_matrice()
        self.fond[7][0] = 'BN'
        self.redessiner_matrice()
        
    
    def deplacement_aleatoire(self):
        xo, yo = self.x, self.y
        boucle_max = 0
        while boucle_max < 10000 and (self.x < 0 or self.x > 7 or self.y < 0 or self.y > 7 or self.fond[self.y][self.x] in ('BN', 'BB')):
            dx, dy = choice([(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)])
            self.x = xo + dx
            self.y = yo + dy
            boucle_max = boucle_max + 1
        if not boucle_max == 10000:
            self.fond[self.y][self.x] = 'BN' if self.fond[self.y][self.x] == 'N' else 'BB'
            self.redessiner_matrice()
        else:
            self.x = xo
            self.y = yo
            
    def generer_matrice(self):
        fond = [['B' if (x+y)%2 == 0 else 'N' for x in range(self.dessin.larg)] for y in range(self.dessin.haut)]
        return fond

    def redessiner_matrice(self):
        f, y, x = self.fond, self.y, self.x
        dico = {'N':(150, 150, 150), 'B': (245, 245, 245), 'BN': (150, 150, 245), 'BB' : (220, 220, 245)}
        for lig in range(self.dessin.haut):
            for col in range(self.dessin.larg):
                self.dessin.vue.modifier_grille('fond', lig, col, c = dico[f[lig][col]], visible = True)
                self.dessin.vue.modifier_grille('texte', lig, col, t = '\u265E' if lig == y and col == x else '', 
                                                  visible = True, tp = 45) 
    
class Dessin:
    
    def __init__(self):
        self.haut = 8
        self.larg = 8
        self.vue = Vue(self.haut, self.larg, max_dim = 5)
        self.plateau = Plateau(self)        

    def deplacer_hasard(self):
        self.plateau.deplacement_aleatoire()
