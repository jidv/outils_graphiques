from outils.vizu_graphe import VizuGraphe
from random import choice, randint
#code pas propre : passé en POO après début non POO

class Dessin:
    
    def __init__(self):
        global GRAPHE, V
        self.HAUTEUR = 7
        self.GRAPHE = self.fournir_graphe()
        self.V = VizuGraphe('liste', self.GRAPHE, oriente = True, moteur = 'dot', 
                                    #couleurs = fournir_descente((0.6, 0.2, 1)),
                                    etiquettes_principales = self.fournir_etiquettes())

    def exemple_de_descente(self):
        descente = self.fournir_descente((0.6, 0.2, 1))
        self.V.modifier(couleurs = descente)

    def fournir_graphe(self):
        graphe = dict()
        nb_sommets = 0
        for i in range(self.HAUTEUR):
            for j in range(i+1):
                graphe[nb_sommets] = [nb_sommets+i+1, nb_sommets+i+2] if i < self.HAUTEUR - 1 else []
                nb_sommets = nb_sommets + 1
        return graphe

    def fournir_descente(self, couleur):
        descente = {0:couleur}
        en_cours = 0
        for i in range(self.HAUTEUR):
            gauche = choice((True, False))
            en_cours = (en_cours + i + 1) if gauche else (en_cours + i + 2)
            descente[en_cours] = couleur
        nb_sommets = 0
        for i in range(self.HAUTEUR):
            for j in range(i+1):
                if nb_sommets not in descente.keys():
                    descente[en_cours] = (0.3, 0.2, 1)
                nb_sommets = nb_sommets + 1
        return descente

    def fournir_etiquettes(self):
        etiquettes = dict()
        nb_sommets = 0
        for i in range(self.HAUTEUR):
            for j in range(i+1):
                etiquettes[nb_sommets] = randint(0, 9)
                nb_sommets = nb_sommets + 1
        return etiquettes


