from random import random

def maillage(H, L, taux, oriente = False):
    '''
    Renvoie un graphe planaire pseudo aléatoire en forme de
    reseau rectangulaire avec des trous (filet de pêche abimé)
    comportant L*H sommets sous forme de liste d'adjacence
    - L et H : entiers indiquant la hauteur et la largeur du maillage (inférieurs à 26)
    - taux : flottant entre 0 et 1 indiquant le taux de présence des arêtes 
            (présence ou absence tirée au sort)
    - oriente : booléen indiquant si le graphe fourni est orienté ou pas
    Les sommets sont indexés sous la forme 'AA, AB, AB, ...'
    '''
    assert H <= 26 and L<= 26
    
    def ij_to_ab(i, j):
        return chr(65+i)+chr(65+j)
    
    adj = dict()
    for i in range(H):
        for j in range(L):
            adj[ij_to_ab(i, j)] = []
            if i>0:
                if random() < taux:
                    adj[ij_to_ab(i, j)].append(ij_to_ab(i-1, j))
            if i<H-1:
                if random() < taux:
                    adj[ij_to_ab(i, j)].append(ij_to_ab(i+1, j))
            if j>0:
                if random() < taux:
                    adj[ij_to_ab(i, j)].append(ij_to_ab(i, j-1))
            if j<L-1:
                if random() < taux:
                    adj[ij_to_ab(i, j)].append(ij_to_ab(i, j+1))
    if not oriente :
        for sommet in adj:
            for voisin in adj[sommet]:
                if sommet not in adj[voisin]:
                    adj[voisin].append(sommet)
    return adj


def etoiles_reliees(S_M_L_XL):
    '''
    Renvoie un graphe planaire en forme d'etoiles reliees sous forme de liste d'adjacence
    - SM_M_L_XL : 'S', 'M', 'L' ou 'XL'
    '''  
    nb_branches = {'S':4, 'M':5, 'L':5, 'XL':6}[S_M_L_XL]
    
    def etoile_depart(nb_sommets):
        liste = dict()
        liste[0] = []
        for i in range(1, 1+nb_sommets):
            liste[0].append(i)
            liste[i] = [0]
        return liste
    
    def ajouter_etoile(liste, sommet, nb_sommets_en_plus):
        indice_depart = len(liste)
        for i in range(indice_depart, indice_depart + nb_sommets_en_plus):
            liste[sommet].append(i)
            liste[i] = [sommet]                    
    e = etoile_depart(nb_branches)
    for i in range(1, 1+nb_branches):
        ajouter_etoile(e, i, nb_branches)
    for i in range(1+nb_branches, 1+nb_branches*(nb_branches+1)):
        ajouter_etoile(e, i, nb_branches-1)
    if S_M_L_XL in 'XL' :    
        for i in range(1+nb_branches*(nb_branches+1), 
                       1+nb_branches*(nb_branches+1) + nb_branches * nb_branches * (nb_branches - 1) ):
            ajouter_etoile(e, i, nb_branches-2)    
    return e

def soleil(nb_branches, longueur_branches):
    '''
    Renvoie un graphe planaire en forme de soleil sous forme de liste d'adjacence
    - nb_branches = nombre de branches = nombre de sommets créant le cercle du "soleil"
    - longueur_branches = nombre de sommets constituant les branches
    '''  
    def rond_depart(nb_branches):
        dico = { i:[(i+1)%nb_branches] for i in range(nb_branches) }
        for i in range(nb_branches):
            dico[(i+1)%nb_branches].append(i)
        return dico
    
    def ajouter_branches(soleil, longueur_branches):
        nb_branches = len(soleil)
        for sommet_du_rond in range(nb_branches):
            nb_sommets = len(soleil)
            soleil[sommet_du_rond].append(nb_sommets)
            soleil[nb_sommets] = [sommet_du_rond]
            for sommet_de_branche in range(nb_sommets + 1, nb_sommets + longueur_branches):
                soleil[sommet_de_branche] = [sommet_de_branche - 1]
                soleil[sommet_de_branche - 1].append(sommet_de_branche)
                
    soleil = rond_depart(nb_branches)
    ajouter_branches(soleil, longueur_branches)
    return soleil


def l_to_m_adjacence(liste, trie = False):
    '''
    Convertit une liste d'adjacence non pondérée en matrice d'adjacence booléenne.
    La liste d'adjacence est du type dict de list (key de type quelconque, val de type list of keys)
    Renvoie une matrice d'adjacence booléenne (sommets triés par ordre croissant si trie = True)
    ainsi que la liste des étiquettes correspondant aux sommets donnés dans la liste d'adjacence.
    '''
    nb_sommets = len(liste)
    etiquettes = list(liste.keys())
    if trie:
        etiquettes.sort()
    dico_etiq_to_index = { etiquettes[i]:i for i in range(nb_sommets)}
    
    matrice = [[False for j in range(nb_sommets)] for i in range(nb_sommets)]
    
    for i in range(nb_sommets):
        sommet = etiquettes[i]
        successeurs = liste[sommet]
        for succ in successeurs:
            j = dico_etiq_to_index[succ]
            matrice[i][j] = True
    
    return matrice, etiquettes
    
        
def m_to_l_adjacence(matrice):
    '''
    Convertit une matrice d'adjacence booléenne (False / True) ou binaire (0 / 1)
    en liste d'adjacence.
    La liste d'adjacence renvoyée est du type dict de list 
    (key de type quelconque, val de type list of keys)
    '''
    nb_sommets = len(matrice)
    liste = dict()
    
    for i in range(nb_sommets):
        successeurs = []
        for j in range(nb_sommets):
            if matrice[i][j] == True or matrice[i][j] == 1:
                successeurs.append(j)
        liste[i] = successeurs
    return liste  

























