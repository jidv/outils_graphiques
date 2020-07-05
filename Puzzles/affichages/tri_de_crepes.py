from outils.interface_grille import Vue
from random import shuffle


class Dessin:
    
    def __init__(self, nb_crepes = 7):
        #la matrice stocke aussi les couleurs d'affichage
        self.haut = nb_crepes
        self.larg = 2*self.haut+2
        self.vue = Vue(self.haut, self.larg, max_dim = 6)
        
        self.matrice = self.generer_matrice()

        self.afficher_matrice()

    def generer_ligne(self, larg):
        #larg varie de 1 à self.haut (pas de 2 à self.larg)
        ligne = [(255, 255, 255)] * self.larg
        curseur = int((255*(larg-1))/(self.haut-1))
        for i in range(larg):
            ligne[self.larg//2+i] = (255 - curseur, curseur, 255)
            ligne[self.larg//2-i-1] = (255 - curseur, curseur, 255)
        return ligne
    
    def generer_matrice(self):
        matrice =[]
        largeurs = list(range(1, self.haut+1))
        shuffle(largeurs)
        for larg in largeurs:
            matrice.append(self.generer_ligne(larg))
        return matrice

    def afficher_matrice(self):
        for y in range(self.haut):
            for x in range(self.larg):
                self.vue.modifier_grille('fond', y, x, c = self.matrice[y][x], visible = True)

    def retourner_x_crepes(self, x):
        for i in range((x)//2):
            self.matrice[x - i - 1], self.matrice[i] = self.matrice[i], self.matrice[x - i - 1]
        self.afficher_matrice()

 

