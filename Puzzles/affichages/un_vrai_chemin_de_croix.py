from outils.interface_grille import Vue

class Dessin:
    
    def __init__(self):
        self.haut = 9
        self.larg = 9
        self.vue = Vue(self.haut, self.larg, max_dim = 5)
        self.c_1 = (200, 230, 250)
        self.c_2 = (200, 250, 230)
        self.c_3 = (250, 250, 250)
        self.matrice = self.fournir_matrice_croix()
        self.afficher_matrice()

    def fournir_matrice_croix(self):
        ligne_a = [0, 0, 0, 1, 1, 1, 0, 0, 0]
        ligne_b = [1 for i in range(9)]
        matrice = [ligne_a.copy() if i not in (3, 4, 5) else ligne_b.copy() for i in range(9)]
        return matrice
        

    def afficher_matrice(self):
        for y in range(self.haut):
            for x in range(self.larg):
                if self.matrice[y][x] == 1:
                    self.vue.modifier_grille('fond', y, x, c = self.c_1 if (y+x)%2 == 0 else self.c_2, visible = True)
                else :
                    self.vue.modifier_grille('fond', y, x, c = self.c_3, visible = True)
                    
                

