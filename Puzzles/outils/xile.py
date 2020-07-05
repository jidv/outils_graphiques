class Cellule:
    
    def __init__(self, element, succ):
        self.element = element
        self.succ = succ
        
    def get_element(self):
        return self.element
    
    def get_succ(self):
        return self.succ

    def set_succ(self, cell):
        self.succ = cell
        
    def __repr__(self):
        return '|' + str(self.element)
    
class Pile:
    
    def __init__(self):
        self.cellule = None
        
    def est_vide(self):
        return self.cellule == None
        
    def ajouter(self, element):
        self.cellule = Cellule(element, self.cellule)
    
    def extraire(self):
        assert not self.est_vide()
        x = self.cellule.get_element()
        self.cellule = self.cellule.get_succ()
        return x
        
    def __repr__(self):
        c = self.cellule
        s = '|'
        while not c is None:
            s = c.__repr__() + s
            c = c.get_succ()
        return s[:]  + '\u2B80'  

class File:
    
    def __init__(self):
        self.tete = None
        self.dernier = None
        
    def est_vide(self):
        return self.tete == None
        
    def ajouter(self, element):
        if not self.est_vide():
            self.dernier.set_succ(Cellule(element, None))
            self.dernier = self.dernier.get_succ()
        else:
            self.dernier = Cellule(element, None)
            self.tete = self.dernier
    
    def extraire(self):
        assert not self.est_vide()
        x = self.tete.get_element()
        self.tete = self.tete.get_succ()
        return x 
        
    def __repr__(self):
        c = self.tete
        s = ''
        while not c is None:
            s = s + c.__repr__()
            c = c.get_succ()
        return '\u2BA4|' + s[:] + '\u2BA0'   
                  
