from outils.interface_grille import Vue

class Dessin:
    
    def __init__(self):
        self.dim = 23
        self.vue = Vue(self.dim, self.dim, max_dim = 5)
        self.matrice = self.fournir_matrice()
        self.afficher_matrice()

    def fournir_matrice(self):
        ligne = list('ENGAGELEJEUQUEJELEGAGNE')
        matrice = [0]*self.dim
        for i in range(self.dim//2):
            space = ['']*(self.dim//2 - i)
            ligne_en_cours = space + ligne[:i+1] + (ligne[-i:] if i != 0 else []) + space
            matrice[i] = ligne_en_cours.copy()
            matrice[-1-i] = ligne_en_cours.copy()
        matrice[self.dim//2] = ligne
        return matrice
        

    def afficher_matrice(self):
        for y in range(self.dim):
            for x in range(self.dim):
                self.vue.modifier_grille('texte', y, x, t = self.matrice[y][x], tp = 13, visible = True)
                