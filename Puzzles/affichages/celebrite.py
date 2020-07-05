from outils.vizu_graphe import VizuGraphe
from outils.xile import File, Pile
from random import randint, choice



class Dessin():
    
    def __init__(self, nb_personnes):
        self.nb_personnes = nb_personnes
        self.graphe = self.generer_matrice()
        self.v = VizuGraphe('matrice_bool', self.graphe, oriente = True, 
                                                         moteur = 'neato',
                                                         label = 'Un graphe de connaissances')  
        
    def generer_matrice(self):
        
        M = [[False for col in range(self.nb_personnes)] for lig in range(self.nb_personnes)]
        taux_connaissance = 0.2
        for lig in range(self.nb_personnes):
            for col in range(self.nb_personnes):
                M[lig][col] = choice((True, False, False, False, False))
                
        celebrite = choice((True, False))
        #on fait une célébrité par défaut
        k = randint(0, self.nb_personnes-1)
        M[k] = [False for col in range(self.nb_personnes)]
        for lig in range(self.nb_personnes):
            M[lig][k] =  True
            
        #qu'on transforme en "presque-célébrité" s'il n'en faut pas
        if not celebrite:
            for i in range(2):
                p = k
                while p == k:
                    p = randint(0, self.nb_personnes - 1)
                M[p][k] = False
                M[k][p] = True

        return M
    
    def x_connait_y(self, x, y):
        return self.graphe[x][y]
            
        
        
        