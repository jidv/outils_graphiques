from outils.vizu_graphe import VizuGraphe
from outils.xile import File, Pile
from copy import deepcopy

class Dessin:
    
    def __init__(self):
        self.graphe = dict()
        self.nb_m = 3
        self.nb_c = 3
        self.depart = Situation(self.nb_m,self.nb_c,'g',0,0) 
        self.gagnant = Situation(0,0,'d',self.nb_m,self.nb_c)
      
        self.peupler()
        #filiations = self.parcours_2_ter()
        #bon_chemin = self.donner_chemin(filiations)
        #bon_chemin[self.tts(self.depart)] = (0.85, 1, 1)
        #bon_chemin[self.tts(self.gagnant)] = (0.85, 1, 1)
        bon_chemin = {self.tts(self.depart) : (0.85, 1, 1), self.tts(self.gagnant) : (0.85, 1, 1)}
        self.v = VizuGraphe('liste', self.graphe, oriente = True, moteur = 'neato', couleurs = bon_chemin)
        
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
                        
                #if desc == self.gagnant:         #<-------------------- #pourquoi pas ?                              
                    #return                                              
                
    def tts(self, s):
        s = str(s.mg) + str(s.cg) + ('*| ' if s.bb == 'g' else ' |*') + str(s.md) + str(s.cd)
        return s
        
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
                

        
        
    def donner_descendants(self, s):
        descendants = set()

        if s.bb == 'g':
            if s.mg>=1 and s.cg>=1 and not (s.md+1 < s.cd+1): # and not pour éviter le cas (0, 1) --> (1, 2)
                descendants.add(Situation(s.mg-1, s.cg-1, 'd', s.md+1, s.cd+1))
            if s.mg>=1 and not (0 < s.mg-1 and s.mg-1 < s.cg):
                descendants.add(Situation(s.mg-1, s.cg,   'd', s.md+1, s.cd  ))
            if s.cg>=1 and not (0 < s.md and s.md < s.cd+1):
                descendants.add(Situation(s.mg  , s.cg-1, 'd', s.md,   s.cd+1))
            if s.mg>=2 and not (0 < s.mg-2 and s.mg - 2 < s.cg):
                descendants.add(Situation(s.mg-2, s.cg,   'd', s.md+2, s.cd  ))                   
            if s.cg>=2 and not (0 < s.md and s.md < s.cd + 2):
                descendants.add(Situation(s.mg,   s.cg-2, 'd', s.md,   s.cd+2))
                                
        if s.bb == 'd':
            if s.md>=1 and s.cd>=1 and not (s.mg+1 < s.cg+1):
                descendants.add(Situation(s.mg+1, s.cg+1, 'g', s.md-1, s.cd-1))
            if s.md>=1 and not (0 < s.md-1 and s.md-1 < s.cd):
                descendants.add(Situation(s.mg+1, s.cg,   'g', s.md-1, s.cd  ))
            if s.cd>=1 and not (0 < s.mg and s.mg < s.cg+1):
                descendants.add(Situation(s.mg  , s.cg+1, 'g', s.md,   s.cd-1))
            if s.md>=2 and not (0 < s.md-2 and s.md-2 < s.cd):
                descendants.add(Situation(s.mg+2, s.cg,   'g', s.md-2, s.cd  ))                  
            if s.cd>=2 and not (0 < s.mg and s.mg < s.cg+2):
                descendants.add(Situation(s.mg,   s.cg+2, 'g', s.md,   s.cd-2))
        
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
                
       

class Situation:
    
    def __init__(self, mg, cg, berge_bateau, md, cd):
        self.mg = mg
        self.cg = cg
        self.md = md
        self.cd = cd
        self.bb = berge_bateau
                               
    def est_egal(self, s):
        return s.mg == self.mg and s.cg == self.cg and s.md == self.md and s.cd == self.cd and s.bb == self.bb
                
            
           
                
          
        
         
              
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                