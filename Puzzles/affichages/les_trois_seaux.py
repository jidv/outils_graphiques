from outils.vizu_graphe import VizuGraphe
from outils.xile import File, Pile

class Dessin:
    
    def __init__(self):
        self.graphe = dict()
        self.depart = (8, 0, 0)
        self.gagnant = (4, 0, 0)
        self.volumes = {0:8, 1:5, 2:3}
        #self.couleurs = {elt : (0.67, 0.4, 1) for elt in self.bon_chemin}
        self.peupler()
        filiations = self.parcours_2_ter()
        bon_chemin = self.donner_chemin(filiations)
        bon_chemin[self.tts(self.depart)] = (0.85, 1, 1)
        bon_chemin[self.tts(self.gagnant)] = (0.85, 1, 1)
        self.v = VizuGraphe('liste', self.graphe, oriente = True, moteur = 'dot', couleurs = bon_chemin)
        
    def peupler(self):
        file = File()
        file.ajouter(self.depart)
        while not file.est_vide():
            t = file.extraire()
            descendants = self.donner_descendants(t)
            for desc in descendants:
                if self.gerer_graphe(t, desc):   #<------------------- #on met à jour le graphe et
                    file.ajouter(desc)                                 #si nécessaire on ajoute
                                                                       #le descendant à la file
                        
                #if desc == self.gagnant:        #<-------------------- # pourquoi pas ?                            
                    #return
                
    def tts(self, t):
        return str(t[0]) + str(t[1]) + str(t[2])
        
    def gerer_graphe(self, t, desc):
        '''
        met à jour le graphe et renvoie 
        True si le descendant de t a besoin d'être exploré (mis dans la file)
        et False sinon (pas mis dans la pile)
        '''
        #effet de bord
        t_as_str = self.tts(t)
        desc_as_str = self.tts(desc)
        if t_as_str in self.graphe.keys():
            if desc_as_str not in self.graphe[t_as_str]: 
                self.graphe[t_as_str].append(desc_as_str)
        else:
            self.graphe[t_as_str] = [desc_as_str]
        if desc_as_str not in self.graphe.keys():
            self.graphe[desc_as_str] = []
            return True
        else:
            return False
        
                

        
        
    def donner_descendants(self, t):
        #t = 3-uplet des volumes
        descendants = set()
        descendants.add((0, t[1], t[2]))
        descendants.add((t[0], 0, t[2]))
        descendants.add((t[0], t[1], 0))
        for i in range(3):
            for j in range(3):
                if j != i:
                    l = list(t)
                    volume_de_j_apres_transvase = min(self.volumes[j], t[j] + t[i])
                    volume_de_i_apres_transvase = t[i] - (volume_de_j_apres_transvase - t[j])
                    l[i] = volume_de_i_apres_transvase
                    l[j] = volume_de_j_apres_transvase
                    descendants.add(tuple(l))
        return descendants
    
    
    
    def parcours_2_ter(self):
        '''
        On renvoie un dictionnaire {sommet : predecesseur for sommet in graphe}
        '''
        graphe = self.graphe
        depart = self.tts(self.depart)
        parents = dict()

        def visiter(successeur, sommet):      #<sss
            parents[successeur] = sommet

        a_explorer = File()
        deja_vu = dict()
        deja_vu[depart] = True
        parents[depart] = None                  #<sss
        a_explorer.ajouter(depart)
        while not a_explorer.est_vide():
            sommet = a_explorer.extraire()
            for successeur in graphe[sommet]:       
                if successeur not in deja_vu.keys():
                    deja_vu[successeur] = True
                    visiter(successeur, sommet)    #<sss
                    a_explorer.ajouter(successeur)

        return parents


    def donner_chemin(self, parents):
        depart = self.tts(self.depart)
        sommet = self.tts(self.gagnant)
        if sommet not in parents.keys():
            return dict()
        chemin_inverse = Pile()
        chemin_inverse.ajouter(sommet)
        longueur = 0
        while parents[sommet] != None:
            sommet = parents[sommet]
            chemin_inverse.ajouter(sommet)
            longueur = longueur + 1

        longueur_chemin = longueur
        chemin = dict()
        while longueur>=0:
            sommet = chemin_inverse.extraire()
            chemin[sommet] = (1, 1, 1)
            longueur = longueur - 1

        return chemin
       
       
                    
            
            
            
            