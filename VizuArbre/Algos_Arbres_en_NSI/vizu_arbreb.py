import graphviz as gv
from copy import copy, deepcopy

# Permet de représenter graphiquement une instance d'arbre binaire.
# Le module doit être paramétré pour prendre en compte l'interface 
# de la classe Arbre utilisée :
#      --> comment accéder au sous-arbre gauche ?
#      --> comment accéder au sous-arbre droit ?
#      --> comment accéder à l'étiquette ?
#      --> comment tester le cas de l'arbre vide ?
# Ce paramétrage s'effectue dans l'en-tête du module.
# Il faut également paramétrer si l'utilisation sera faite en notebook ou pas.

JUPYTER_NOTEBOOK = True

#en tête pour l'interface n°1 du notebook de documentation
#ACCES_VIA_GETTERS= False
#ACCES_E = "valeur"
#ACCES_G = "gauche"
#ACCES_D = "droit"
#ARBRE_VIDE_IS_ARBRE = False
#ACCES_V = None

#en-tête pour l'interface n°2 du notebook de documentation
ACCES_VIA_GETTERS= True
ACCES_E = "get_etiquette"
ACCES_G = "get_gauche"
ACCES_D = "get_droite"
ARBRE_VIDE_IS_ARBRE = True
ACCES_V = "est_vide"


class VizuArbreB:  
    def __init__(self, arbre, etiquettes_secondaires = None,
                              couleurs = None,
                              formes = None,
                              **kwargs):
        '''
        - arbre : instance d'arbre binaire à représenter
        
        - etiquettes_secondaires [ = None] : dictionnaire ayant pour clefs des étiquettes
                                        de l'arbre et pour valeurs les étiquette secondaires
                                        à afficher.
                                                  
        - couleurs [ = None] : dictionnaire ayant pour clefs des étiquettes de l'arbre et pour 
                                        valeurs les couleurs personnalisées des noeuds au format 
                                        (H, S, V) avec H, S, V de type float entre 0 et 1.
                                        
        - formes [ = None] : dictionnaire ayant pour clefs des étiquettes de l'arbre et pour valeurs les formes
                                 des noeuds ('rect', 'rectangle', 'folder', 'house', 'ellipse', 'egg', 
                                 'triangle', 'diamond' [...] 
                                 https://graphviz.org/doc/info/shapes.html   
        
        - **kwargs : il s'agit des paramètres supplémentaires acceptés par la méthode modifier 
        '''     
        self.arbre = arbre
        assert not self._tester_vide(arbre), 'L\'arbre passé en argument est vide'
        self.etiquettes_secondaires = deepcopy(etiquettes_secondaires)
        self.couleurs = copy(couleurs)
        self.formes = copy(formes)   
        self._initialiser_parametres_dessin()
        self._modifier(**kwargs)
        self._creer_objet_graphviz()
            
    def _initialiser_parametres_dessin(self):
        
        self.size = '10'                              #taille maximale de l'image générée
        self.label = ' '                  #titre du graphique
        self.moteur = 'dot'                           #moteur utilisé pour le placement des noeuds
        
        self.node_style = 'filled'                    #remplissage des noeuds
        self.node_shape = 'circle'                    #forme des noeuds
        self.node_fontsize = '12'                     #taille de la police des noeuds
        self.node_small_fontsize = '11'               #taille de la police secondaire des noeuds
        self.node_color = (0.5, 0.2, 1.0)             #couleur par défaut au format HSV
        self.node_width = '0.35'                      #largeur des noeuds
        self.node_height = '0.35'                     #hauteur des noeuds
        self.node_main = True                         #affichage des etiquettes principales
        self.node_naming = 'etiquette'                #methode de nommage des noeuds ('etiquette' ou 'binaire')
        
        self.edge_style = 'solid'                     #flèches en traits pleins
        self.edge_arrowhead = 'none'                  #forme des têtes de flèches
        self.edge_arrowsize = '0.5'                   #taille des têtes de flèches
        self.edge_distinct = False                    #utiliser une forme différente de flèche pour gauche-droite

    def _creer_objet_graphviz(self):
        self.G = gv.Digraph('arbre')
        self._injecter_parametres_dessin_dans_graphviz()
        self._dessiner_arbre(arbre = self.arbre, name = 1)
        if JUPYTER_NOTEBOOK : 
            display(self.G)
        else :
            self.G.render(view=True)
            
    def _injecter_parametres_dessin_dans_graphviz(self):
        
        self.G.attr(root = '',                        
                    size = self.size,                      
                    label = self.label,
                    engine = self.moteur)          
        
        self.G.node_attr.update(style = self.node_style,     
                                shape = self.node_shape,     
                                fontsize = self.node_fontsize,
                                width = self.node_width,       
                                height = self.node_height,      
                                fixedsize = 'False',
                                margin = '0, 0')   
        
        self.G.edge_attr.update(style = self.edge_style,       
                                arrowsize = self.edge_arrowsize     
                               )      

############## METHODES D'ACCES POUR PARCOURIR L'ARBRE FOURNI #######

    def _tester_vide(self, arbre):
        if ARBRE_VIDE_IS_ARBRE :
            return getattr(arbre, ACCES_V)()
        else:
            return arbre == ACCES_V
        
    def _donner_gauche(self, arbre):
        if ACCES_VIA_GETTERS :
            return getattr(arbre, ACCES_G)()
        else:
            return getattr(arbre, ACCES_G)
    
    def _donner_droite(self, arbre):
        if ACCES_VIA_GETTERS :
            return getattr(arbre, ACCES_D)()
        else:
            return getattr(arbre, ACCES_D)    
            
    def _donner_etiquette(self, arbre):
        if ACCES_VIA_GETTERS :
            return getattr(arbre, ACCES_E)()
        else:
            return getattr(arbre, ACCES_E)
        
############## METHODES DE CREATION DES ATTRIBUTS GRAPHIQUES GRAPHVIZ #######
        
    def _tuple_to_string(couleur):
        return ' '.join([str(round(c, 4)) for c in couleur])
    
    def _donner_couleur(self, sommet, name):
        if self.node_naming == 'etiquette':
            nom = sommet
        elif self.node_naming == 'binaire':
            nom = name
        if self.couleurs == None or nom not in self.couleurs.keys() :
            return VizuArbreB._tuple_to_string(self.node_color)
        else:
            return VizuArbreB._tuple_to_string(self.couleurs[nom])
        
    def _donner_label(self, sommet, name):
        if self.node_naming == 'etiquette':
            nom = sommet
        elif self.node_naming == 'binaire':
            nom = name        
        if self.etiquettes_secondaires == None or nom not in self.etiquettes_secondaires.keys() :
            sommet = sommet if self.node_main else ''
            S = '<<B>' + str(sommet) + '</B>>'
            return S
        else:
            e_princ = str(sommet) if self.node_main else ''
            e_secon = str(self.etiquettes_secondaires[nom])
            small = self.node_small_fontsize
            S = '<<B>' + e_princ + '</B><I><FONT POINT-SIZE="' + small + '"><BR/>' + e_secon + '</FONT></I>>'
            return S

    def _donner_forme(self, sommet, name):
        if self.node_naming == 'etiquette':
            nom = sommet
        elif self.node_naming == 'binaire':
            nom = name
        if self.formes == None or nom not in self.formes.keys() :
            return self.node_shape
        else:
            return self.formes[nom]
        
    def _donner_tete(self, sommet, name):
        if not self.edge_distinct:
            return self.edge_arrowhead
        else:
            if name%2 == 0:
                return self.edge_arrowhead
            else:
                if self.edge_arrowhead == 'empty':
                    return 'normal'
                else:
                    return 'empty'
        
            
################  DESSIN ET ENREGISTREMENT ########################
        
    def _dessiner_arbre(self, arbre, name):
        if not self._tester_vide(arbre):
            self.G.node( str(name), label = str(self._donner_label(self._donner_etiquette(arbre), name)),
                                    color = self._donner_couleur(self._donner_etiquette(arbre), name),
                                    shape = self._donner_forme(self._donner_etiquette(arbre), name))
            if name != 1:
                self.G.edge(str(name >> 1), 
                            str(name), 
                            arrowhead = self._donner_tete(self._donner_etiquette(arbre), name))
            sag = self._donner_gauche(arbre)
            sad = self._donner_droite(arbre)
            self._dessiner_arbre(sag, name << 1)
            self._dessiner_arbre(sad, (name << 1) + 1)
        else:
            self.G.node(str(name), label = ' ', color = 'white', penwidth = '0')
            self.G.edge(str(name>>1), str(name), 
                        arrowhead = 'none')
                    
                    
                    
################  MODIFICATION     ########################                    
    
    def _modifier(self, **kwargs):
        legal_args = ("size", "label", "node_style", "node_shape", "node_fontsize", 
                      "node_small_fontsize","node_color", "node_width", "node_height", 
                      "edge_style", "edge_arrowhead", "edge_arrowsize", "reset", "moteur",
                      "etiquettes_secondaires", "couleurs", "formes", "node_naming",
                      "node_main", "edge_distinct")
        
        if "reset" in kwargs.keys():
            if kwargs["reset"] == 'True':
                self._initialiser_parametres_dessin()
                self.etiquettes_secondaires = None
                self.couleurs = None
                self.formes = None
        for key, val in kwargs.items():
            if key in legal_args:
                if type(val) == int or type(val) == float:
                    setattr(self, key, str(val))
                elif type(val) == dict:
                    setattr(self, key, deepcopy(val))
                else:
                    setattr(self, key, val)   
    
    def modifier(self, **kwargs):
        '''
        Une fois un graphique créé et représenté, permet de modifier les paramètres de dessin.
        
        - REINITIALISER LES PARAMETRES
        
            - reset  [ = False]             : booléen indiquant si on réinitialise les modifications
                                                   de paramètres déjà prises en compte auparavant
        
        - PARAMETRES DU GRAPHE EN ENTIER
        
            - size [ = 10  ]                : taille maximale de l'image générée
            
            - label [ = 'Arbre Binaire']    : titre du graphique
            
            - moteur [ = 'dot']             : moteur de placement des noeuds utilisé par graphviz. 
                                                Autres choix : 'circo', 'dot', 'fdp', 'neato', 'osage', 
                                                'patchwork', 'sfdp','twopi'
                                                https://graphviz.org/documentation/
                                              
 
        - PARAMETRES INDIVIDUELS DES NOEUDS

            - etiquettes_secondaires [ = None] : dictionnaire ayant pour clefs des étiquettes
                                                   de l'arbre* et pour valeurs les étiquette secondaires
                                                   à afficher.

            - couleurs [ = None]               : dictionnaire ayant pour clefs des étiquettes de 
                                                    l'arbre* et pour valeurs les couleurs des noeuds 
                                                    au format (H, S, V) avec H, S, V de type float 
                                                    entre 0 et 1.

            - formes [ = None]                 : dictionnaire ayant pour clefs des étiquettes de
                                                   l'arbre* et pour valeurs les formes des sommets ('rect', 
                                                   'rectangle', 'folder', 'house', 'ellipse', 'egg', 
                                                   'triangle', 'diamond' [...] 
                                                   https://graphviz.org/doc/info/shapes.html  
                                                   
            - * : si on choisit node_naming = 'binaire' on peut choisir pour clefs le nommage usuel des arbres *
                  binaires (voir section PARAMETRES DES NOEUDS PAR DEFAUT)
                                                   
        - PARAMETRES DES NOEUDS PAR DEFAUT
        
            - node_shape [ = 'circle']        : forme des noeuds dessinés. Autres formes disponibles
                                                   rect, ellipse, folder, star [...]. 
                                                   https://graphviz.org/doc/info/shapes.html
                                                  
            - node_width [ = 0.35]            : largeur des noeuds
            
            - node_height [ = 0.35]           : hauteur des noeuds
            
            - node_color [ = (0.5, 0.2, 1)]   : couleur des noeuds au format HSV 
            
            - node_fontsize [ = 12]           : taille de police de l'étiquette principale des noeuds
            
            - node_small_fontsize [ = 11]     : taille de police de l'étiquette secondaire des noeuds
            
            - node_style [ = 'filled']        : style de remplissage. Au choix parmi 'solid', 'dashed', 
                                                   'dotted', 'bold', 'rounded', 'filled' [...]
                                                   https://graphviz.org/doc/info/attrs.html#k:style
                                                   
            - node_main [ = True]      : pour activer/désactiver l'affichage des étiquettes principales.
            
            - node_naming [ = 'etiquette']     : en spécifiant ici 'etiquette' ou 'binaire' on précise si
                                              les clefs des dictionnaires servant à passer les paramètres 
                                              individuels sont les étiquettes des sommets ou le nommage
                                              binaire usuel :
                                              - n = 1 pour le sommet 
                                              - n = 2 * n  pour sag (n<<1)
                                              - n = 2 * n + 1 pour sad (n<<1 + 1)            
                                                   
                                                   
        
        - PARAMETRES DES ARCS PAR DEFAUT
        
            - edge_style [ = 'solid']         : style du tracé, au choix parmi 'solid', 'dashed', 
                                                   'dotted', 'bold'
            
            - edge_arrowhead [= 'empty']      : forme de la tête de la flèche. Au choix parmi 'normal', 
                                                   'none', 'invempty', 'open' [...]
                                                   https://graphviz.org/doc/info/attrs.html#k:arrowType
                                                  
            - edge_arrowsize [= 0.5]          : taille de la tête de la flèche   
            
            - self.edge_distinct [= False]    : utiliser une forme différente de flèche pour gauche-droite
        '''
        self._modifier(**kwargs)
        self._creer_objet_graphviz()
            
    def enregistrer(self, nom_fichier = None, format_image = None):
        '''
         Permet d'enregistrer le graphe au format texte 'graphviz' et au format image choisi.
         Il y a donc deux fichiers qui sont générés.
         
          - nom_fichier [ = 'mon_arbre_binaire'] : nom des deux fichiers sauvegardés dont l'un sera
                                                   suffixé avec l'extension correspondant au format 
                                                   image choisi
                                                  
          
          - format_image [ = 'png']              : format de fichier de l'image générée. Au choix parmi : 
                                                   'ps', 'eps', 'svg', 'jpg', 'tiff' [...]
                                                   https://graphviz.org/doc/info/output.html
        '''                                              
        if nom_fichier == None:
            nom_fichier = self.nom_fichier
        if format_image == None:
            format_image = self.format_image
        self.G.render(filename = nom_fichier, format = format_image)