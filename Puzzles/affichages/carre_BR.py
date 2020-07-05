from random import randint
from outils.interface_grille import Vue

        

class Dessin:
    def __init__(self, dim = 10):
        self.dim = dim
        self.vue = Vue(self.dim, self.dim, max_dim = 5)
        self.vue.lier_evenement('selection_objet', self.gestionnaire_selection, True)
        self.matrice = self.generer_matrice()
        self.visibles = [[False for col in range(self.dim)] for lig in range(self.dim)]
        self.redessiner_matrice()
        self.message_nombre_a_trouver()
            
    def generer_matrice(self):
        m = [[0 for x in range(self.dim)] for y in range(self.dim)]
        m[0][0] = randint(1,99)
        for idx in range(1, self.dim):
            m[idx][0] = m[idx-1][0] + randint(1, 46)
            m[0][idx] = m[0][idx-1] + randint(1, 46)
        for lig in range(1, self.dim):
            for col in range(1, self.dim):
                m[lig][col] = max(m[lig-1][col], m[lig][col-1]) + randint(1, 46)
        return m
        

    def redessiner_matrice(self):
        for lig in range(self.dim):
            for col in range(self.dim):
                vis = self.visibles[lig][col]
                self.vue.modifier_grille('texte', lig, col, t = self.matrice[lig][col], tp = 15, visible = vis)
                self.vue.modifier_grille('fond', lig, col, ce = (0, 140, 140), ci = (150, 240, 240), visible = True)
                
    
    def message_nombre_a_trouver(self):
        lig, col = randint(1, self.dim - 1), randint(1, self.dim - 1)
        nat = self.matrice[lig][col]
        nat = nat + randint(0, 1)
        self.vue.mzt(t = 'En cliquant sur les cases, déterminez si le nombre ' + str(nat) + 
                         ' est présent parmi les cartes.', tp = 10, ct = (255, 0, 0))
    
    def gestionnaire_selection(self, event):
        lig = event['lig']
        col = event['col']
        self.visibles[lig][col] = True
        self.redessiner_matrice()
