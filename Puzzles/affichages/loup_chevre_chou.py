from outils.vizu_graphe import VizuGraphe

class Dessin:

    def __init__(self):
        self.model = {'0000': ['1000', '1100', '1010', '1001'],
                     '0001': ['1001', '1101', '1011'],
                     '0010': ['1010', '1110', '1011'],
                     '0011': ['1011', '1111'],
                     '0100': ['1100', '1110', '1101'],
                     '0101': ['1101', '1111'],
                     '0110': ['1110', '1111'],
                     '0111': ['1111'],
                     '1000': ['0000'],
                     '1001': ['0001', '0000'],
                     '1010': ['0010', '0000'],
                     '1011': ['0011', '0001', '0010'],
                     '1100': ['0100', '0000'],
                     '1101': ['0101', '0001', '0100'],
                     '1110': ['0110', '0010', '0100'],
                     '1111': ['0111', '0011', '0101', '0110']}

        self.depart_arrivee = ['0000', '1111']
        self.perdant = ['0110', '0011', '1001', '1100']
        self.couleurs = {elt : (0.67, 0.4, 1) for elt in self.depart_arrivee}
        for perdu in self.perdant:
            self.couleurs[perdu] = (1, 0.4, 1)

        self.v = VizuGraphe('liste', self.model, oriente = True, moteur = 'sfdp', couleurs = self.couleurs )