from os import path as os_path
from os import walk as os_walk
from pathlib import Path
from sys import stdout as sys_stdout
from sys import exc_info as sys_exc_info
from traceback import print_exception as traceback_print_exception
from logging import basicConfig as logging_basicConfig
from logging import exception as logging_exception

from math import floor

import matplotlib as mpl

#En cas de problème de backend en utilisation en dehors de notebook on
#pourra forcer l'utilisation du backend basé sur tk en décommentant cette ligne de code :
#mpl.use('TkAgg')

#Deux imports uniquement pour utilisation notebook (backend 'nbAgg')
#peuvent être mis en commentaires si le module est utilisé hors notebook
from IPython.display import display, clear_output, update_display 
from matplotlib.backend_bases import NavigationToolbar2

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
from matplotlib.backend_bases import PickEvent
from matplotlib import rcParams


#############################################################################    
#############################################################################
##
##      classes abstraites
##
#############################################################################
#############################################################################

#############################################################################
#      Accessoires de calcul
#############################################################################
class Calc:
    def tup2str(couleur):
        S = '#'
        for composante in couleur:
            comp_hexa = '{:02x}'.format(composante)
            S = S + comp_hexa
        return S
    
    def obj_lig_col2str(objet, num_lig, num_col):
        ''' transforme le triplet 'objet', 8, 4 en string :  'objet#8#4' '''
        S = objet + '#' + str(num_lig) + '#' + str(num_col)
        return S
    
    def str2obj_lig_col(S):
        ''' transforme la string :  'objet#8#4' en triplet 'objet', 8, 4 '''
        L = S.split('#')
        return L[0], int(L[1]), int(L[2])
    
    def donner_dims(lig, col, max_dim = 7):
        '''
        fournit les dimensions exploitables dans matplotlib, aux "bonnes"
        proportions en fonction du nombre de lignes et de colonnes de la grille
        '''
        c = col + 1 #une marge de 0.5 autour du repère de tracé
        l = lig + 1
        if c>l:
            w_tot = max_dim
            h_gr = max_dim * l/c
            h_zt = 1 #la zone texte fera toujour 1 inche de haut
            h_tot = h_gr + h_zt
            r_zt = h_zt/h_tot
        else:
            w_tot = max_dim * c/l
            h_gr = max_dim
            h_zt = 1
            h_tot = h_gr + h_zt
            r_zt = h_zt/h_tot
        return w_tot, h_tot, r_zt
            
    
#############################################################################
#      Préchargement des images dans un tableau
#############################################################################     
class ImagesMatricielles:
    #précharge toutes les images situées dans le dossier ./images/
    loaded = dict()
    chemin_racine = os_path.abspath('./images/')
    
    for root, subdirs, files in os_walk(chemin_racine):
        for filename in files:
            extension = filename[-4:]
            if extension == '.png' or extension == '.PNG':
                file_path = os_path.join(root, filename)
                loaded[file_path] = plt.imread(file_path)
        
    def donne(chemin_partiel):
        #chemin donné en prenant pour racine './images/'
        chemin_racine = os_path.abspath('./images/')
        chemin = os_path.join(chemin_racine, Path(chemin_partiel))
        return ImagesMatricielles.loaded[chemin]

#############################################################################
#      Désactivation des raccourcis clavier par défaut de matplotlib 
#############################################################################
class Desactivator:
    
    def desactiver_toolbar_et_raccourcis():
        # desactivation des raccourcis clavier standard
        for k in rcParams.keys():
            if k[0:7] == 'keymap.':
                rcParams[k] = []
        # désactivation de la barre d'outils (cas général)   
        if mpl.get_backend() != 'nbAgg':
            rcParams['toolbar'] = 'None' 
            
        # désactivation de la barre d'outils (cas jupyter notebook + backend nbAgg)       
        if mpl.get_backend() == 'nbAgg':
            #home = NavigationToolbar2.home
            #pan = NavigationToolbar2.pan
            #zoom = NavigationToolbar2.zoom
            #back = NavigationToolbar2.back
            #forward = NavigationToolbar2.forward
            def new_tool(self, vue, *args, **kwargs):
                #home(self, *args, **kwargs)            
                #pan(self, *args, **kwargs)            
                #zoom(self, *args, **kwargs)
                #back(self, *args, **kwargs)    
                #forward(self, *args, **kwargs)
                #save_figure(self, *args, **kwargs)
                pass                
            NavigationToolbar2.home = lambda a, *c, **d : new_tool(a, self, *c, **d)
            NavigationToolbar2.pan = lambda a, *c, **d : new_tool(a, self, *c, **d)
            NavigationToolbar2.zoom = lambda a, *c, **d : new_tool(a, self, *c, **d)
            NavigationToolbar2.back = lambda a, *c, **d : new_tool(a, self, *c, **d)
            NavigationToolbar2.forward = lambda a, *c, **d : new_tool(a, self, *c, **d)  

##############################################################################
#   gestion des exceptions avec le backend nbAgg (notebooks)
##############################################################################
class IntegratorOutputError:
    # prépare la cellule jupyter à recevoir erreurs au-dessus de fenêtre matplotlib + logfile tampon
    def initialiser_gestion_erreurs():
        if mpl.get_backend() == 'nbAgg':
            ERROR_OUTPUT = display(display_id = 'error_output')
            ERROR_OUTPUT.display(CustomExceptionContent('Messages d\'erreur s\'afficheront ici ...'))
            with open('./log_erreur.out', 'w') as error_file:
                error_file.write('')
            LOG_FILENAME = './log_erreur.out'
            logging_basicConfig(filename=LOG_FILENAME, filemode = 'w')
            
class CustomExceptionContent(str):
    #display() n'affiche pas les '\n' par défaut d'où utilisation _repr_pretty_
    #voir module standard pprint si besoin
    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text('')
        else:
            for char in self:
                if char in ('\r', '\n', '\r\n'):
                    p.breakable('\n')
                else:
                    p.text(char)
                    #p.pretty(char) ferait afficher 'm''e''s''s''a''g''e'
                    
class ExceptionManager:
    #si on est avec tkinter (backend TkAgg), pas de soucis. Avec notebook (nbAgg)
    #on logge l'exception puis on ré-injecte le fichier via display (pas trouvé mieux)
    def manage_exception():
        exc_type, exc_value, exc_traceback = sys_exc_info()
        if mpl.get_backend() == 'TkAgg':
            traceback_print_exception(exc_type, exc_value, exc_traceback,
                  limit=2, file=sys_stdout)
        elif mpl.get_backend() == 'nbAgg':
            logging_exception('')
            with open('./log_erreur.out', 'r', newline = '') as error_file:
                error = error_file.read()
            custom_error = CustomExceptionContent(error)
            update_display(custom_error, display_id = 'error_output')
            with open('./log_erreur.out', 'w') as error_file:
                error_file.write('')
                
    def clear_exception():
        custom_error = CustomExceptionContent('')
        update_display(custom_error, display_id = 'error_output')
                     
##############################################################################
##############################################################################
##
##   classes associées à la classe Grille
##
##############################################################################
##############################################################################

#############################################################################
#  custom class de matplotlib.image.AxesImage : une instance par case
#############################################################################
class Image:
    def __init__(self, grille, ax, num_ligne, num_colonne, chemin_fichier, taille, alpha, visible):
        self.grille = grille
        self.ax = ax
        self.num_ligne = num_ligne
        self.num_colonne = num_colonne  
        self.chemin_fichier = chemin_fichier
        self.taille = taille
        self.alpha = alpha
        self.visible = visible
        self.image_matrice = ImagesMatricielles.donne(self.chemin_fichier)
        self.axes_image = self.initialiser_affichage()

    def get_artist(self):
        return self.axes_image    
        
    def initialiser_affichage(self):
        marge = (1 - self.taille)/2
        image = self.ax.imshow(self.image_matrice,
                               extent=(self.num_colonne+marge, self.num_colonne + 1 - marge,
                                        -self.num_ligne - 1 + marge, -self.num_ligne - marge), 
                               zorder = 1, 
                               alpha = self.alpha, 
                               visible = self.visible, 
                               gid = Calc.obj_lig_col2str('image', self.num_ligne, self.num_colonne))
        return image
    
    def actualiser_attributs(self, **modifications):
        for clef, valeur in modifications.items():
            if clef == 'a' or clef == 'alpha':
                if self.alpha != valeur:
                    self.alpha = valeur
                    self.axes_image.set_alpha(valeur)
            elif clef == 'v' or clef == 'visible':
                if self.visible != valeur:
                    self.visible = valeur
                    self.axes_image.set_visible(valeur)
            elif clef == 'cf' or clef == 'chemin_fichier':
                if self.chemin_fichier != valeur:
                    self.chemin_fichier = valeur
                    self.image_matrice = ImagesMatricielles.donne(valeur)
                    self.axes_image.set_data(self.image_matrice)
            elif clef == 't' or clef == 'taille':
                if self.taille != valeur:
                    self.taille = valeur
                    marge = (1 - valeur)/2
                    self.axes_image.set_extent((self.num_colonne+marge, self.num_colonne + 1 - marge,
                        -self.num_ligne - 1 + marge, -self.num_ligne - marge))


#############################################################################
#  custom class de matplotlib.patches.Rectangle : une instance par case
#############################################################################
class Fond:
    def __init__(self, grille, ax, num_ligne, num_colonne, couleur_int, alpha, 
                 couleur_ext, couleur, visible):
        self.grille = grille
        self.ax = ax
        self.num_ligne = num_ligne
        self.num_colonne = num_colonne        
        self.couleur_int = Calc.tup2str(couleur_int)
        self.couleur_ext = Calc.tup2str(couleur_ext)
        self.alpha = alpha
        if couleur != None:
            self.couleur_int = Calc.tup2str(couleur)
            self.couleur_ext = Calc.tup2str(couleur)
        self.visible = visible
        self.patch = self.initialiser_affichage()

    def get_artist(self):
        return self.patch        
        
    def initialiser_affichage(self):
        fond = self.ax.add_patch(Rectangle((self.num_colonne, 
                                            -self.num_ligne-1), 
                                           1, 
                                           1, 
                                           facecolor=self.couleur_int, 
                                           zorder = 0, 
                                           visible = self.visible, 
                                           edgecolor = self.couleur_ext, 
                                           alpha = self.alpha, 
                                           gid = Calc.obj_lig_col2str('fond', self.num_ligne, self.num_colonne)))    
        return fond
    
    def actualiser_attributs(self, **modifications):
        for clef, valeur in modifications.items():
            if clef == 'ci' or clef == 'couleur_int':
                c = Calc.tup2str(valeur)
                if self.couleur_int != c:
                    self.couleur_int = c
                    self.patch.set_facecolor(c)
            elif clef == 'ce' or clef == 'couleur_ext':
                c = Calc.tup2str(valeur)
                if self.couleur_ext != c:
                    self.couleur_ext = c
                    self.patch.set_edgecolor(c)
            elif (clef == 'c' or clef == 'couleur') and valeur != None:
                if valeur != None: 
                    c = Calc.tup2str(valeur)
                    if (self.couleur_int != c or self.couleur_ext != c):
                        self.couleur_int = c
                        self.couleur_ext = c
                        self.patch.set_facecolor(c)
                        self.patch.set_edgecolor(c)            
            elif clef == 'a' or clef == 'alpha':
                if self.alpha != valeur:
                    self.alpha = valeur
                    self.patch.set_alpha(valeur)
            elif clef == 'v' or clef == 'visible':
                if self.visible != valeur:
                    self.visible = valeur
                    self.patch.set_visible(valeur)

        
#############################################################################
#  custom class de matplotlib.text.Text : une instance par case
#############################################################################              
class Texte:
    def __init__(self, grille, ax, num_ligne, num_colonne,  visible, taille_police,
                 alpha, couleur, texte):
        self.grille = grille
        self.ax = ax
        self.num_ligne = num_ligne
        self.num_colonne = num_colonne  
        self.taille_police = taille_police
        self.alpha = alpha
        self.visible = visible
        self.couleur = Calc.tup2str(couleur)
        self.texte = texte
        self.text_artist = self.initialiser_affichage()

    def get_artist(self):
        return self.text_artist        
        
    def initialiser_affichage(self):
        x = self.num_colonne + 0.5
        y = - self.num_ligne - 0.5
        texte = self.ax.text(x, 
                             y, 
                             self.texte, 
                             zorder = 4, 
                             fontfamily = 'monospace', 
                             color = self.couleur,
                             ha = 'center', 
                             va = 'center', 
                             fontsize = self.taille_police, 
                             alpha = self.alpha, 
                             visible = self.visible,
                             gid = Calc.obj_lig_col2str('texte', self.num_ligne, self.num_colonne))
        return texte
    
    def actualiser_attributs(self, **modifications):
        for clef, valeur in modifications.items():
            if clef == 't' or clef == 'texte':
                if self.texte != valeur:
                    self.texte = valeur 
                    self.text_artist.set_text(valeur)
            elif clef == 'v' or clef == 'visible':
                if self.visible != valeur:
                    self.visible = valeur
                    self.text_artist.set_visible(valeur)
            elif clef == 'a' or clef == 'alpha':
                if self.alpha != valeur:
                    self.alpha = valeur
                    self.text_artist.set_alpha(valeur)
            elif clef == 'c' or clef == 'couleur':
                c = Calc.tup2str(valeur)
                if self.couleur != c:
                    self.couleur = c
                    self.text_artist.set_color(c)
            elif clef == clef == 'tp' or 'taille_police':
                if self.taille_police != valeur:
                    self.taille_police = valeur
                    self.text_artist.set_fontsize(valeur)

#############################################################################
#  custom class de matplotlib.patches.Polygon : 2*LIG*COL + LIG + COL instances
############################################################################# 
class Bord:           
                        
    def __init__(self, grille, ax, num_ligne, num_colonne, pos, visible, 
                 couleur_int, alpha, epaisseur, couleur_ext, couleur):
        self.grille = grille
        self.ax = ax
        self.num_ligne = num_ligne
        self.num_colonne = num_colonne 
        self.pos = pos
        self.visible = visible
        self.couleur_int = Calc.tup2str(couleur_int)
        self.couleur_ext = Calc.tup2str(couleur_ext)
        if couleur != None:
            self.couleur_int = Calc.tup2str(couleur)
            self.couleur_ext = Calc.tup2str(couleur)
        self.alpha = alpha
        self.epaisseur = epaisseur
        self.patch = self.initialiser_affichage()
    
    def get_artist(self):
        return self.patch
        
    def initialiser_affichage(self):
        x = self.num_colonne
        y = -self.num_ligne
        e = self.epaisseur/2
        if self.pos == 'horizontal':
            xy_array = [[x, y], [x+e, y+e], [x+1-e, y+e], [x+1, y], [x+1-e, y-e], [x+e, y-e]]
            polygone = self.ax.add_patch(Polygon(xy_array, 
                                                 closed = True, 
                                                 facecolor=self.couleur_int, 
                                                 zorder = 2, 
                                                 edgecolor = self.couleur_ext, 
                                                 alpha = self.alpha,  
                                                 visible = self.visible, 
                                                 gid = Calc.obj_lig_col2str('mur_h', self.num_ligne, self.num_colonne) ))
        if self.pos == 'vertical':  
            xy_array = [[x, y], [x+e, y-e], [x+e, y-1+e], [x, y-1], [x-e, y-1+e], [x-e, y-e]]
            polygone = self.ax.add_patch(Polygon(xy_array, 
                                                 closed = True, 
                                                 facecolor=self.couleur_int, 
                                                 zorder = 3,
                                                 edgecolor = self.couleur_ext, 
                                                 alpha = self.alpha, 
                                                 visible = self.visible, 
                                                 gid = Calc.obj_lig_col2str('mur_v', self.num_ligne, self.num_colonne))) 
        return polygone
    
    def actualiser_attributs(self, **modifications):
        for clef, valeur in modifications.items():
            if clef ==  'a' or clef == 'alpha':
                if self.alpha != valeur:
                    self.alpha = valeur
                    self.patch.set_alpha(valeur)
            elif clef == 'v' or clef == 'visible':
                if self.visible != valeur:
                    self.visible = valeur
                    self.patch.set_visible(valeur)
            elif clef == 'ci' or clef == 'couleur_int':
                c = Calc.tup2str(valeur)
                if self.couleur_int != c:
                    self.couleur_int = c
                    self.patch.set_facecolor(c)
            elif clef == 'ce' or clef == 'couleur_ext':
                c = Calc.tup2str(valeur)
                if self.couleur_ext != c:
                    self.couleur_ext = c
                    self.patch.set_edgecolor(c)
            elif clef == 'c' or clef == 'couleur':
                if valeur != None: 
                    c = Calc.tup2str(valeur)
                    if self.couleur_int != c or self.couleur_ext != c:
                        self.couleur_int = c
                        self.couleur_ext = c
                        self.patch.set_edgecolor(c)
                        self.patch.set_facecolor(c)
            elif clef == 'e' or clef == 'epaisseur':
                if self.epaisseur != valeur:
                    self.epaisseur = valeur
                    x = self.num_colonne
                    y = -self.num_ligne
                    e = self.epaisseur/2
                    if self.pos == 'horizontal':
                        xy_array = [[x, y], [x+e, y+e], [x+1-e, y+e], [x+1, y], [x+1-e, y-e], [x+e, y-e]]
                        self.patch.set_xy(xy_array)
                    if self.pos == 'vertical':
                        xy_array = [[x, y], [x+e, y-e], [x+e, y-1+e], [x, y-1], [x-e, y-1+e], [x-e, y-e]]
                        self.patch.set_xy(xy_array)


#############################################################################
#  custom class de matplotlib.Axes contenant les matplotlib.Artist des cases : 1 seule instance
#############################################################################           
class Grille:
  
    def __init__(self, vue, fig, nb_lignes, nb_colonnes, prefs_murs_v, prefs_murs_h, 
                                            prefs_fonds, prefs_images, prefs_textes):  
        self.vue = vue
        self.fig = fig
        plt.figure(self.fig.number) #figure courante = figure passée en argument
        ax = plt.axes([0.01, 0.01 + self.vue._get_ratio_hauteur_zonetexte(), 0.98, 0.98 - self.vue._get_ratio_hauteur_zonetexte()])
        self.ax = ax
        plt.sca(self.ax)
        ax.set_aspect(1)
        
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.prefs_murs_v = prefs_murs_v
        self.prefs_murs_h = prefs_murs_h
        self.prefs_fonds = prefs_fonds
        self.prefs_images = prefs_images
        self.prefs_textes = prefs_textes
            
        self.murs_v = [[Bord(self, self.ax, i, j, 'vertical', **self.prefs_murs_v) 
                        for j in range(self.nb_colonnes + 1)] for i in range(self.nb_lignes)]
        
        self.murs_h = [[Bord(self, self.ax, i, j, 'horizontal', **self.prefs_murs_h) 
                        for j in range(self.nb_colonnes)] for i in range(self.nb_lignes + 1)]
        
        self.fonds = [[Fond(self, self.ax, i, j, **self.prefs_fonds) 
                        for j in range(self.nb_colonnes)] for i in range(self.nb_lignes)]
        
        self.images = [[Image(self, self.ax, i, j, **self.prefs_images) 
                        for j in range(self.nb_colonnes)] for i in range(self.nb_lignes)]
        
        self.textes = [[Texte(self, self.ax, i, j, **self.prefs_textes) 
                        for j in range(self.nb_colonnes)] for i in range(self.nb_lignes)]
                                         
        

        
        #on redonne la main au Axes de la grille par précaution
        plt.sca(self.ax) 
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False) 
        plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
        self.ax.set_frame_on(True)
        
        self.ax.set_xlim([-0.5, self.nb_colonnes + 0.5])
        self.ax.set_ylim([-0.5 - self.nb_lignes, 0.5])
        
    def get_axe(self):
        return self.ax

    def get_murs_v(self):
        return self.murs_v 
    
    def get_murs_h(self):
        return self.murs_h  

    def get_fonds(self):
        return self.fonds 
    
    def get_images(self):
        return self.images     

    def get_textes(self):
        return self.textes
    
    def modifier(self, objet, lig, col, **modifications):
        convertisseur_clef_objet = {'fond' : self.fonds, 'mur_v' : self.murs_v, 
                                    'mur_h' : self.murs_h, 'image' : self.images,
                                    'texte' : self.textes}
        grille_objets = convertisseur_clef_objet[objet]
        grille_objets[lig][col].actualiser_attributs(**modifications)
  
    def reinitialiser(self):
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                self.fonds[i][j].actualiser_attributs(**self.prefs_fonds)
                self.images[i][j].actualiser_attributs(**self.prefs_images)
                self.textes[i][j].actualiser_attributs(**self.prefs_textes)               
        for i in range(self.nb_lignes + 1):
            for j in range(self.nb_colonnes):  
                self.murs_h[i][j].actualiser_attributs(**self.prefs_murs_h)
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes + 1):  
                self.murs_v[i][j].actualiser_attributs(**self.prefs_murs_v)

##############################################################################    
##############################################################################
##
##   classes associées à la classe ZoneTexte
##
##############################################################################
##############################################################################
        
#############################################################################
#  custom class du matplotlib.text.Texte de la zone de texte : 1 seule instance
############################################################################# 
class TexteZoneTexte:
    
    def __init__(self, ax, taille_police, texte, couleur_fond, alpha, couleur_texte):
        self.ax = ax
        x0, x1 = self.ax.get_xlim()
        y0, y1 = self.ax.get_ylim()
        self.texte = texte
        self.taille_police = taille_police
        self.alpha = alpha
        self.couleur_texte = Calc.tup2str(couleur_texte)
        self.couleur_fond = Calc.tup2str(couleur_fond)
        self.x = x0 + 0.03 * (x1 - x0) #<------------- à améliorer en fonction de la taille de police
        self.y = y1 - 0.15 * (y1 - y0) #<------------- à améliorer en fonction de la taille de police
        self.text_artist = self.initialiser_affichage()
        
    def initialiser_affichage(self):
        texte = self.ax.text(self.x, self.y, self.texte, fontfamily = 'monospace', 
                             color = self.couleur_texte,
                             ha = 'left', va = 'top', fontsize = self.taille_police, 
                             alpha = self.alpha, wrap = True )
        self.ax.set_facecolor(self.couleur_fond)
        return texte
    
    def actualiser_attributs(self, **modifications):
        for clef, valeur in modifications.items():
            if clef == 't' or clef == 'texte':
                if self.texte != valeur:
                    self.texte = valeur
                    self.text_artist.set_text(valeur)
            elif clef == 'tp' or clef == 'taille_police':
                if self.taille_police != valeur:
                    self.taille_police = valeur
                    self.text_artist.set_fontsize(valeur)
            elif clef == 'ct' or clef == 'couleur_texte':
                c = Calc.tup2str(valeur)
                if self.couleur_texte != c:
                    self.couleur_texte = c
                    self.text_artist.set_color(c)                     
            elif clef == 'a' or clef == 'alpha':
                if self.alpha != valeur:
                    self.alpha = valeur
                    self.text_artist.set_alpha(valeur)
            elif clef == 'cf' or clef == 'couleur_fond':
                c = Calc.tup2str(valeur)
                if self.couleur_fond != c:
                    self.couleur_fond = c
                    self.ax.set_facecolor(c)    


#############################################################################
#  custom class de matplotlib.Axes contenant le Text de la zone de texte : 1 seule instance
############################################################################# 
class ZoneTexte:
    
    def __init__(self, vue, fig, prefs_zone_texte):
        self.vue = vue
        self.fig = fig
        self.prefs_zone_texte = prefs_zone_texte  
        plt.figure(self.fig.number) #on prend comme figure courante la figure passée en argument
        ax = plt.axes([0.01, 0.01, 0.98, self.vue._get_ratio_hauteur_zonetexte()])
        self.ax = ax
        plt.sca(self.ax)
        #self.ax.set_aspect((self.vue._get_ratio_hauteur_zonetexte())/0.98)
        
        self.texte = TexteZoneTexte(self.ax, **self.prefs_zone_texte )
        
        plt.sca(self.ax)
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False) 
        plt.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
        self.ax.set_frame_on(True)
        self.ax.set_xlim([0, 1])
        self.ax.set_ylim([0, 1])

    def modifier(self, **modifications):
        self.texte.actualiser_attributs(**modifications)
 
    def reinitialiser(self):
        self.texte.actualiser_attributs(**self.prefs_zone_texte)

##############################################################################    
##############################################################################
##
##   classe Vue : Grille, ZoneTexte, gestion des évènements 
##
##############################################################################
############################################################################## 

class Vue:
    '''
    Implémente une interface d'affichage d'une grille un peu interactive.
    '''
    def __init__(self, nb_lignes, nb_colonnes, max_dim = 7):
        '''
        - nb_lignes   : nombre de lignes de la grille
        - nb_colonnes : nombre de colonnes de la grille
        - max_dim     : dimension maximale de la figure en inches (à 100 dpi)
        |
        |
        |
        -----------------------------------------------------------------------------------------------------------        
        '''
        
        #nombre de lignes et de colonnes de la grille
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes
        self.max_dim = max_dim
        
        #préférences d'initialisation des objets matplotlib
        ###pour la grille
        self.prefs_grille_murs_v = {'visible' : False,
                                    'couleur_int' : (128, 128, 128),
                                    'alpha' : 1, 
                                    'epaisseur' : 0.2,
                                    'couleur_ext' : (42, 42, 42),
                                    'couleur' : None}
        
        self.prefs_grille_murs_h = {'visible' : False, 
                                    'couleur_int' : (128, 128, 128),
                                    'alpha' : 1, 
                                    'epaisseur' : 0.2,
                                    'couleur_ext' : (42, 42, 42),
                                    'couleur' : None} 
        
        self.prefs_grille_fonds = {'couleur_int' : (192, 192, 192),
                                   'alpha' : 1,
                                   'couleur_ext' : (42, 42, 42), 
                                   'couleur' : None,
                                   'visible' : False}
        
        self.prefs_grille_images = {'chemin_fichier' : 'init.png',
                                    'taille' : 0.8,
                                    'alpha' : 1.0,
                                    'visible' : False}
        
        self.prefs_grille_textes = {'visible' : False, 
                                    'taille_police' : 8,
                                    'alpha' : 1,
                                    'couleur' : (0, 0, 0),
                                    'texte' : ''}
        
        ###pour la zone de texte
        self.prefs_zonetexte = {'taille_police' : 8,
                                'texte' : 'Zone d\'affichage de texte', 
                                'couleur_fond' : (235, 235, 235),
                                'alpha' : 1,
                                'couleur_texte' : (145, 145, 145)} 
            
        #désactivation des raccourcis clavier standard de matplotlib (zoom etc.)
        Desactivator.desactiver_toolbar_et_raccourcis()
        
        #prépare la cellule jupyter à recevoir erreurs au-dessus de fenêtre matplotlib + logfile tampon
        IntegratorOutputError.initialiser_gestion_erreurs()
        
        #initialisation des objets matplotlib
        w, h, r =  Calc.donner_dims(self.nb_lignes, self.nb_colonnes, max_dim = self.max_dim)
        self.initial_width = w 
        self.initial_height = h
        self.ratio_hauteur_zonetexte = r
        self.initial_dpi = 100
        self.fig = plt.figure(figsize=(self.initial_width,self.initial_height), dpi = self.initial_dpi)
        plt.figure(self.fig.number)
        
        self.fig.set_constrained_layout_pads(w_pad = 0, h_pad = 0, wspace = 0, hspace = 0)
        
        self.grille = Grille(self, self.fig, self.nb_lignes, self.nb_colonnes, self.prefs_grille_murs_v, 
                self.prefs_grille_murs_h, self.prefs_grille_fonds, self.prefs_grille_images, self.prefs_grille_textes)

        self.zonetexte = ZoneTexte(self, self.fig, self.prefs_zonetexte)       
        self.ecouteurs = dict()
        #self.historique = deque()
        #self.longueur_historique = 999999
            
         
    def _get_ratio_hauteur_zonetexte(self):
        return self.ratio_hauteur_zonetexte
                           

    def modifier_grille(self, objet, lig, col, **modifications):
        '''
        Permet de modifier les attributs d'un objet graphique présent dans la grille.
        lig et col désignent les indices de ligne et de colonne de l'objet (0, 0 : coin supérieur gauche).
            - objet : 'mur_v', 'mur_h', 'fond', 'texte', 'image'
            - lig : entier entre 0 et NB_LIGNES - 1 (sauf pour objet = 'mur_h' : entre 0 et NB_LIGNES)
            - col : entier entre 0 et NB_COLONNES - 1 (sauf pour objet = 'mur_v' : entre 0 et NB_COLONNES)
            - **modifications :
               - objet 'mur_v':
                    - couleur_int ou ci : 3 ou 4-uplet d'entiers entre 0 et 255 au format (R, G, B) ou (R, G, B, A) 
                    - couleur_ext ou ce : même type que couleur_int
                    - couleur ou c      : même type que couleur_int, modifie simultanément couleur_int et couleur_ext
                    - visible ou v      : booléen indiquant si l'objet est visible ou pas
                    - alpha ou a        : transparence, flottant entre 0 (trnsparent) et 1 (opaque)
                    - epaisseur ou e    : flottant entre 0 et 1 indiquant l'épaisseur du bord
                    
               - objet 'mur_h':
                    - idem que pour 'mur_v' 
                    
               - objet 'fond':
                    - idem que pour 'mur_v' sauf epaisseur qui n'est pas disponible
               
               - objet 'texte':
                    - texte ou t          : chaîne de caractères (au delà de 3 caractères, risque de débord)
                    - couleur ou c        : 3 ou 4-uplet d'entiers entre 0 et 255 au format (R, G, B) ou (R, G, B, A)
                    - taille_police ou tp : entier, à ajuster (gestion du texte sous matplotlib est peu développée)
                    - visible ou v        : booléen indiquant si l'objet est visible ou pas
                    - alpha ou a          : transparence, flottant entre 0 (trnsparent) et 1 (opaque)                    

               - objet 'image':
                    - chemin_fichier ou cf : chemin d'accès au fichier exprimé depuis la racine de './images/'
                                             Le fichier doit :
                                                - être au format .png
                                                - être situé dans le répertoire './images/' ou dans ses sous-répertoires
                                             Par défaut, initialisée avec './images/init.png' qui doit donc exister.
                    - taille ou t          : flottant entre 0 et 1. Lorsque c'est inférieur à 1 un redimensionnement 
                                             est effectué ce qui introduit du flou.
                    - visible ou v         : booléen indiquant si l'objet est visible ou pas
                    - alpha ou a           : transparence, flottant entre 0 (trnsparent) et 1 (opaque)              
        
        Les préférences initiales sont les attributs suivants de l'instance de Vue :
        prefs_grille_murs_v = { 'visible' : False,
                                'couleur_int' : (128, 128, 128), 
                                'alpha' : 1, 
                                'epaisseur' : 0.2, 
                                'couleur_ext' : (42, 42, 42), 
                                'couleur' : None}
                                
        self.prefs_grille_murs_h = {'visible' : False, 
                                    'couleur_int' : (128, 128, 128), 
                                    'alpha' : 1, 
                                    'epaisseur' : 0.2, 
                                    'couleur_ext' : (42, 42, 42), 
                                    'couleur' : None} 
                                    
        self.prefs_grille_fonds = {'couleur_int' : (192, 192, 192), 
                                   'alpha' : 1, 
                                   'couleur_ext' : (42, 42, 42), 
                                   'couleur' : None, 
                                   'visible' : False}
                                   
        self.prefs_grille_images = {'chemin_fichier' : 'init.png', 
                                    'taille' : 0.8, 
                                    'alpha' : 1.0, 
                                    'visible' : False}
                                    
        self.prefs_grille_textes = {'visible' : False, 
                                    'taille_police' : 8,
                                    'alpha' : 1,
                                    'couleur' : (0, 0, 0), 
                                    'texte' : ''}
        |
        |
        |
        -----------------------------------------------------------------------------------------------------------        
        '''
        try:
            self.grille.modifier(objet, lig, col, **modifications)
            if not plt.isinteractive() :
                plt.show(block = False)
            ExceptionManager.clear_exception() 
        except:
            ExceptionManager.manage_exception()        

    def mg(self, objet, lig, col, **modifications):
        '''
        Voir modifier_grille.
        '''
        self.modifier_grille(objet, lig, col, **modifications)
            
    def modifier_zonetexte(self, **modifications):
        '''
        Permet de modifier les attributs de la zone de texte.
            - **modifications :
                - texte ou t          : chaîne de caractères (au delà de 3 caractères, risque de débord)
                - couleur_texte ou ct : 3 ou 4-uplet d'entiers entre 0 et 255 au format (R, G, B) ou (R, G, B, A)
                - couleur_fond ou cf  : 3 ou 4-uplet d'entiers entre 0 et 255 au format (R, G, B) ou (R, G, B, A)
                - taille_police ou tp : entier, à ajuster (gestion du texte sous matplotlib est peu développée)
                - alpha ou a          : transparence, flottant entre 0 (trnsparent) et 1 (opaque)
                
        Les préférences initiales sont les attributs suivants de l'instance de Vue :
            - self.prefs_zonetexte = {'taille_police' : 8,
                                      'texte' : 'Zone d\'affichage de texte', 
                                      'couleur_fond' : (235, 235, 235),
                                      'alpha' : 1,
                                      'couleur_texte' : (145, 145, 145)}                 
        |
        |
        |
        -----------------------------------------------------------------------------------------------------------        
        '''
        try:
            self.zonetexte.modifier(**modifications)
            if not plt.isinteractive() :
                plt.show(block = False)
                ExceptionManager.clear_exception() 
        except:
            ExceptionManager.manage_exception()

    def mzt(self, **modifications):
        '''
        Voir modifier_zonetexte.
        '''
        self.modifier_zonetexte(**modifications)       
            
            
    def reinitialiser_grille(self):
        '''
        Permet de réinitialiser la grille avec les préférences initiales.
        Les préférences initiales sont les attributs suivants de l'instance de Vue :
            - prefs_grille_murs_v, 
            - prefs_grille_murs_h
            - prefs_grille_fonds
            - prefs_grille_images
            - prefs_grille_textes
        |
        |
        |
        -----------------------------------------------------------------------------------------------------------        
        '''
        try:
            self.grille.reinitialiser()
            if not plt.isinteractive():
                plt.show(block = False)
            ExceptionManager.clear_exception() 
        except:
            ExceptionManager.manage_exception()
            
    def reinitialiser_zonetexte(self):
        '''
        Permet de réinitilaiser la zone de texte avec les préférences initiales.
        Les préférences initiales sont les attributs suivants de l'instance de Vue :
            - prefs_zonetexte
        |
        |
        |
        -----------------------------------------------------------------------------------------------------------        
        '''
        try:
            self.zonetexte.reinitialiser()
            if not plt.isinteractive():
                plt.show(block = False)
            ExceptionManager.clear_exception() 
        except:
            ExceptionManager.manage_exception()
            

            
    def exporter_png(self, chemin_fichier):
        '''
        Permet d'exporter la vue au format png :
            - chemin_fichier : chemin d'accès au fichier qui sera enregistré
        |
        |
        |
        -----------------------------------------------------------------------------------------------------------        
        '''
        try:
            plt.savefig(chemin_fichier)
            ExceptionManager.clear_exception() 
        except:
            ExceptionManager.manage_exception()

    def lier_evenement(self, evenement, gestionnaire, activer, argument = None):
        '''
        Permet d'activer la gestion de certains évènements. 
        - evenement     : 'appui_touche', 'fin_appui_touche', 'selection_objet', 'clic_souris' , 'fin_clic_souris
        - gestionnaire  : fonction qui réceptionnera les évènements déclenchés
                          cette fonction doit avoir un paramètre obligatoire et un paramètre facultatif :
                           - e à qui sera affecté l'évènement qui a été déclenché (requis)
                           - a à qui sera affecté argument s'il a été fourni (facultatif)
        - activer       : booléen indiquant si on active l'écoute ou désactive une écoute mise en place
        
        Voici les contenus des cinq évènements disponibles qui sont des dictionnaires dont les clefs sont :
          - 'appui_touche'       : 'evenement',          'touche', 'lig', 'col', 'moment',         
          - 'fin_appui_touche'   : 'evenement',          'touche', 'lig', 'col', 'moment',         
          - 'selection_objet'    : 'evenement', 'objet', 'touche', 'lig', 'col', 'moment', 'bouton'
          - 'clic_souris'        : 'evenement',          'touche', 'lig', 'col', 'moment', 'bouton'
          - 'fin_clic_souris'    : 'evenement',          'touche', 'lig', 'col', 'moment', 'bouton'
        
        Lors de l'activation de la mise en écoute il n'est pas possible d'écouter une seule 
        touche ou un seul objet de la grille. Le filtrage doit être effectué en aval, dans la fonction ecouteur.
        
        En cas de superposition d'objets graphiques, l'évènement 'selection_objet' n'est lancé que par celui 
        ayant le zorder le plus élevé avec :
        - fond   : zorder = 0
        - image  : zorder = 1
        - mur_h  : zorder = 2
        - mur_v  : zorder = 3
        - texte  : zorder = 4
        
        L'argument à transférer a vocation à être un tableau mutable (typiquement une matrice ou un tableau de matrices)
        
        Les limitations en termes de gestion d'évènements sont volontaires.
        
        La valeur associée à la clef 'moment' correspond à un TimeStamp en milli-secondes.
        Elle n'est affectée que dans le cas des back-ends 'TkAgg' (tkinter) et 'nbAgg' (notebook backend).
        |
        |
        |
        -----------------------------------------------------------------------------------------------------------        
        '''
        
        try:
            conv_clef_ev = {'clic_souris' : 'button_press_event', 
                            'fin_clic_souris' : 'button_release_event',
                            'appui_touche' : 'key_press_event',
                            'fin_appui_touche' : 'key_release_event',
                            'selection_objet' : 'mon_pick_event'}

            type_evenement = conv_clef_ev[evenement]
            pick = (type_evenement == 'mon_pick_event')                              

            if activer:
                if not type_evenement in self.ecouteurs.keys():                        
                    cid = self.fig.canvas.mpl_connect(type_evenement if not pick else 'button_press_event', 
                               lambda e : self.__conditionner_evenement(e, gestionnaire, argument, pick = pick))
                    self.ecouteurs[type_evenement] = cid
                if type_evenement in self.ecouteurs.keys(): 
                    self.fig.canvas.mpl_disconnect(self.ecouteurs[type_evenement])
                    cid = self.fig.canvas.mpl_connect(type_evenement if not pick else 'button_press_event', 
                               lambda e : self.__conditionner_evenement(e, gestionnaire, argument, pick = pick))
                    self.ecouteurs[type_evenement] = cid
            if not activer and type_evenement in self.ecouteurs.keys():
                self.fig.canvas.mpl_disconnect(self.ecouteurs[type_evenement])
                del(self.ecouteurs[type_evenement])
            ExceptionManager.clear_exception() 
        except:
            ExceptionManager.manage_exception()
            
    def __conditionner_evenement(self, e, fonction_gestionnaire, argument, pick):
        try:
            nom = e.name
            if not pick: #les quatre évènements distincts de 'selection_objet' reprennent ceux de mpl
                inaxes = e.inaxes
                if inaxes == self.grille.get_axe():
                    canvas = e.canvas
                    dictionnaire = dict()
                    #event.timeStamp pris en charge sur les backends nbAgg et TkAgg
                    gui_event = e.guiEvent
                    moment = 0
                    if mpl.get_backend() == 'nbAgg': 
                        moment = gui_event['timeStamp']
                    elif mpl.get_backend() == 'TkAgg':
                        moment = gui_event.time
                    dictionnaire['moment']=moment

                    if nom == 'button_press_event':
                        dictionnaire['evenement'] = 'clic_souris'
                        dictionnaire['bouton'] = 'droit' if e.button in (2, 3) else 'gauche'
                        dictionnaire['touche'] = e.key
                        dictionnaire['lig'] = min(max(floor(-e.ydata),0), self.nb_lignes - 1)
                        dictionnaire['col'] = min(max(floor(e.xdata), 0), self.nb_colonnes - 1)
                    elif nom == 'button_release_event':
                        dictionnaire['evenement'] = 'fin_clic_souris'
                        dictionnaire['bouton'] = 'droit' if e.button in (2, 3) else 'gauche'
                        dictionnaire['touche'] = e.key
                        dictionnaire['lig'] = min(max(floor(-e.ydata),0), self.nb_lignes - 1)
                        dictionnaire['col'] = min(max(floor(e.xdata), 0), self.nb_colonnes - 1)
                    elif nom == 'key_press_event':
                        dictionnaire['evenement'] = 'appui_touche'
                        dictionnaire['touche'] = e.key
                        dictionnaire['lig'] = min(max(floor(-e.ydata),0), self.nb_lignes - 1)
                        dictionnaire['col'] = min(max(floor(e.xdata), 0), self.nb_colonnes - 1)
                    elif nom == 'key_release_event':
                        dictionnaire['evenement'] = 'fin_appui_touche'
                        dictionnaire['touche'] = e.key
                        dictionnaire['lig'] = min(max(floor(-e.ydata),0), self.nb_lignes - 1)
                        dictionnaire['col'] = min(max(floor(e.xdata), 0), self.nb_colonnes - 1)
                    
                    #self.historique.append(dictionnaire.copy())
                    #if len(self.historique) > self.longueur_historique:
                    #    self.historique.popleft()
                    #dictionnaire['historique'] = list(deepcopy(self.historique))
                    if argument is not None:          
                        fonction_gestionnaire(dictionnaire, argument)
                    else: 
                        fonction_gestionnaire(dictionnaire)

            else:  # l'évènement 'selection_objet' est optimisé pour tirer profit de la dtructure de grille
                inaxes = e.inaxes
                if inaxes == self.grille.get_axe():
                    #sélection des artistes sous le clic
                    lig = min(max(floor(-e.ydata),0), self.nb_lignes - 1)
                    col = min(max(floor(e.xdata), 0), self.nb_colonnes - 1)
                    cont = [self.grille.get_textes()[lig][col].get_artist(),
                            self.grille.get_murs_v()[lig][col].get_artist(),
                            self.grille.get_murs_h()[lig][col].get_artist(),
                            self.grille.get_murs_v()[lig][col+1].get_artist(),
                            self.grille.get_murs_h()[lig+1][col].get_artist(),
                            self.grille.get_images()[lig][col].get_artist(),
                            self.grille.get_fonds()[lig][col].get_artist()]
                    cont = [a for a in cont if a.get_visible() and a.contains(e)[0]]
                    if cont == []:
                        return
                    else:
                        #on aurait pu recréer un pickEvent dans la méthode 'lier_evenement'         
                        #pick_event = PickEvent('mon_pick_event', self.fig.canvas, e,
                        #    cont[0], guiEvent = e.guiEvent, **cont[0].contains(event)[1])
                        canvas = e.canvas
                        dictionnaire = dict()
                        #event.timeStamp pris en charge sur les backends nbAgg et TkAgg
                        gui_event = e.guiEvent
                        moment = 0
                        if mpl.get_backend() == 'nbAgg': 
                            moment = gui_event['timeStamp']
                        elif mpl.get_backend() == 'TkAgg':
                            moment = gui_event.time
                        dictionnaire['moment']=moment

                        dictionnaire['evenement'] = 'selection_objet'
                        dictionnaire['bouton'] = 'droit' if e.button in (2, 3) else 'gauche'
                        dictionnaire['touche'] = e.key
                        a = cont[0] 
                        objet, num_lig, num_col = Calc.str2obj_lig_col(a.get_gid())
                        dictionnaire['objet'] = objet
                        dictionnaire['lig'] = num_lig
                        dictionnaire['col'] = num_col
                        
                    #self.historique.append(dictionnaire.copy())
                    #if len(self.historique) > self.longueur_historique:
                    #    self.historique.popleft()
                    #dictionnaire['historique'] = list(deepcopy(self.historique))
                    if argument is not None:           
                            fonction_gestionnaire(dictionnaire, argument)
                    else: 
                        fonction_gestionnaire(dictionnaire)
        except:
            ExceptionManager.manage_exception()

