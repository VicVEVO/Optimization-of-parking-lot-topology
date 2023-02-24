from constantes import *

import numpy as np
from random import randint, random

def rechercheCheminMin(parking,i1, j1, i2, j2, volOiseau=False):#ok
    """
    Algorithme cherchant avec la méthode A* le chemin le plus court liant (i1,j1) et (i2,j2)
    Parameters
    ----------
    parking: array
    i1, j1, i2, j2: int
    volOiseau: bool

    Returns
    -------
    array
        liste des coordonnées successives des points du chemin liant (i1,j1) et (i2,j2).
    """
    def heuristique(i,j):
        return abs(j-j2) + abs(i-i2)
    
    D = np.full((LARGEUR_PARKING,LONGUEUR_PARKING), False)
    V = [(i,j) for i in range(LARGEUR_PARKING) for j in range(LONGUEUR_PARKING)]
    P = {}
    C = {}

    C = {(i, j): float('inf') for i in range(LARGEUR_PARKING) for j in range(LONGUEUR_PARKING)}
    C[(i1, j1)] = 0

    while V:
        minValue,minCoords = float('inf'),None
        for i,j in C.keys():
            if C[i,j] <= minValue and (i,j) in V:
                minValue,minCoords = C[i,j],(i,j)

        (i,j) = V.pop(V.index((minCoords[0],minCoords[1]))) # on prend le prochain indice dans la queue
        D[i,j] = True
        if i == i2 and j == j2: # si l'indice actuel est arrivé sur l'indice de destination on arrête
            break
        
        voisinage = [(i, j+1), (i-1, j), (i, j-1), (i+1, j)]

        for numVoisin in range(len(voisinage)):

            iVois, jVois = voisinage[numVoisin]
            if 0 <= iVois < LARGEUR_PARKING and 0 <= jVois < LONGUEUR_PARKING and not D[iVois, jVois]: # si la case n'est pas visitée
                if parking[iVois,jVois] == 0 or volOiseau or (iVois,jVois) == (i2,j2): # si la case est accessible physiquement et que c'est de la route
                    D[iVois, jVois] = True # le voisin est désormais visité
                    C[iVois, jVois] = C[i,j] + 1 + heuristique(iVois,jVois)
                    P[(iVois, jVois)] = (i, j) # on stocke les indices précédents pour i_vois,j_vois

    chemin = []

    i, j = i2, j2 # on part de l'arrivée
    while (i, j) in P:
        chemin.append((i, j))
        i, j = P[(i, j)]

    return list(reversed(chemin))

def coordonneesRoutes(parking): #ok
    iBal,jBal = I_ENTREE,J_ENTREE
    casesVisitees = set()
    fileCoordsAVisiter = [(iBal,jBal)]

    while fileCoordsAVisiter:
        iBal,jBal = fileCoordsAVisiter.pop(0)
        if iBal < 0 or iBal >= LARGEUR_PARKING or jBal < J_ENTREE or jBal > J_SORTIE:
            continue # on skip l'itération

        if parking[iBal,jBal] !=0 or (iBal,jBal) in casesVisitees:
            continue
        casesVisitees.add((iBal,jBal))
        fileCoordsAVisiter.extend([(iBal-1,jBal),(iBal+1,jBal),(iBal,jBal-1),(iBal,jBal+1)]) # plus efficace que +=
    return casesVisitees # on travaille directement avec l'ensemble

def coordonneesFrontiere(i,j,parking,sens,etape=''): # donne coords sur bordure (si etape='deviation' dans mutation) inf ou sup de la route principale 
    epsi = 1
    if etape == 'ajout_morceau_route': # astuce pour éviter de faire 2 fonctions
        epsi = 0 # Si on cherche à ajouter un bout de route, la coordonnée extérieure nous intéresse

    if sens == "haut":
        for ligne in range(i-1, -1, -1):
            if parking[ligne][j] != 0:

                return (ligne+epsi, j) #s'il n'y a que de la route au dessus de (i,j), tant pis
    elif sens == "bas":
        for ligne in range(i+1, LARGEUR_PARKING):
            if parking[ligne][j] != 0:
                return (ligne-epsi, j)
    elif sens == "gauche":
        for colonne in range(j-1, -1, -1):
            if parking[i][colonne] != 0:
                return (i, colonne+epsi)
    elif sens == "droite":
        for colonne in range(j+1, LONGUEUR_PARKING):
            if parking[i][colonne] != 0:
                return (i, colonne-epsi)
    return (i,j) 

def coordonneesDerivation(i0,j0,i1,j1):
    """
    Renvoie des coordonnées sur la médiatrice de la droite liant (i0,j0) à (i1,j1)
    """
    iMil = int((i0 + i1) / 2)
    jMil = int((j0 + j1) / 2)
    coordonnees = []

    if i0 == i1:
        # si on a une ligne horizontale joignant (i0,j0) à (i1,j1)
        iChoisi = randint(max(iMil-TAUX_DEVIATION,0),min(iMil+TAUX_DEVIATION,LARGEUR_PARKING-1))
        return(iChoisi,jMil)

    elif j0 == j1:
        # si la ligne est verticale
        jChoisi = randint(max(jMil-TAUX_DEVIATION,0),min(jMil+TAUX_DEVIATION,LONGUEUR_PARKING-1))
        return(iMil,jChoisi)
    else:
        # sinon on a une ligne diagonale
        m = -1/((j1 - j0) / (i1 - i0)) # equation bissectrice i=mj+p
        p = iMil - (m * jMil)
        if j0>j1: # on échange les indices tels que j0<j1
            j0,j1 = j1,j0
        couples = []
        for j in range(j0,j1+1):
            i = int(m*j+p)
            if 0<=i<=LARGEUR_PARKING-1:
                couples.append((i,j))

        return couples[randint(0,len(couples)-1)]

def enleveRoute(parking,i0,j0,i1,j1,coordsRoute,sensAllongement):
    for j in range(j0+1,j1):
        for i in range(LARGEUR_PARKING):
            if (i,j) in coordsRoute:
                parking[i,j] = 1#[-1,1][randint(0,1)]
    if sensAllongement == 'bas':
        for i in range(i0+1,LARGEUR_PARKING):
            if (i,j0) in coordsRoute:
                parking[i,j0] = 1#[-1,1][randint(0,1)]
        for i in range(i1+1,LARGEUR_PARKING):
            if (i,j1) in coordsRoute:
                parking[i,j1] = 1#[-1,1][randint(0,1)]
    else:
        for i in range(i0-1,-1,-1):
            if (i,j0) in coordsRoute:
                parking[i,j0] = 1#[-1,1][randint(0,1)]
        for i in range(i1-1,-1,-1):
            if (i,j1) in coordsRoute:
                parking[i,j1] = 1#[-1,1][randint(0,1)]

def ajouteRoute(parking,i0,j0,i1,j1):
    
    (iDev, jDev) = coordonneesDerivation(i0,j0,i1,j1)
    
    chemin = [(i0,j0)] + rechercheCheminMin(parking,i0,j0,iDev,jDev,True) + rechercheCheminMin(parking,iDev,jDev,i1,j1,True)
    etape = 0
    nbEtapes = len(chemin)

    while etape != nbEtapes:
        (iBal,jBal) = chemin[etape]
        parking[iBal,jBal] = 0
        etape += 1

def coordonneesCoupage(parking,coordsRoute,sensAllongement):
    couplesCoup1 = coordsRoute[(coordsRoute[:,1] >= randint(0,int(2/3*LONGUEUR_PARKING))) & (coordsRoute[:,1] <= 2/3*LONGUEUR_PARKING)]
    nbCouplesCoup1 = len(couplesCoup1)
    if nbCouplesCoup1 == 1:
        (iCoup1,jCoup1) = couplesCoup1[0]
    else:
        (iCoup1,jCoup1) = couplesCoup1[randint(0,nbCouplesCoup1-1)]
    
    # on choisit d'autres coordonnées
    
    couplesCoup2 = coordsRoute[coordsRoute[:,1] >= randint(jCoup1+1,LONGUEUR_PARKING-2)]
    nbCouplesCoup2 = len(couplesCoup2)
    if nbCouplesCoup2 == 1:
        (iCoup2,jCoup2) = couplesCoup2[0]
    else:
        (iCoup2,jCoup2) = couplesCoup2[randint(0,nbCouplesCoup2-1)]
    
    return coordonneesFrontiere(iCoup1,jCoup1,parking,sensAllongement), coordonneesFrontiere(iCoup2,jCoup2,parking,sensAllongement)

def placesBordsRoute(parking): #ok
    coordsPlaces = set()
    
    for (iBal,jBal) in coordonneesRoutes(parking): # indices de balayage
        coordonnes_entourant = [(iBal+1,jBal),(iBal,jBal+1),(iBal-1,jBal),(iBal,jBal-1)]
        for (iEntourant,jEntourant) in coordonnes_entourant:
            if 0<=iEntourant<=LARGEUR_PARKING-1 and J_ENTREE<=jEntourant<=J_SORTIE and parking[iEntourant,jEntourant] == 1: # s'il y a une place accessible depuis la route
                coordsPlaces.add((iEntourant,jEntourant))

    return np.array(list(coordsPlaces))

def coordonneesPlaceProche(parking,coordsPlacesAccess,i,j): #ok
    coordsPlacesDispos = np.array([(x,y) for x,y in coordsPlacesAccess if parking[x,y] != 2]) # on prend les places accessibles libres (où il n'y a pas de voiture garée)
    if not np.any(coordsPlacesDispos): # si toutes les places sont prises la voiture ne bouge pas
        return (i,j)
    distancescoordsPlacesDispos = np.sqrt((coordsPlacesDispos[:,0]-i)**2 + (coordsPlacesDispos[:,1]-j)**2)
    indiceMin = np.argmin(distancescoordsPlacesDispos)
    return coordsPlacesDispos[indiceMin]

def refresh(parking,parkingRef,iPrec,jPrec,iSuiv,jSuiv): #ok
    parking[iPrec,jPrec], parking[iSuiv,jSuiv] = parkingRef[iPrec,jPrec], 2

def nvVoiture(voiture,parkingSim,parking,coordsPlacesAccess,tMoyGarage,tMoySortie): #ok
    (i,j) = voiture[0]
    voitureGaree = voiture[1]
    if not voitureGaree:
        tMoyGarage += 1/NTOT_VOITURES
        (iPlace,jPlace) = coordonneesPlaceProche(parkingSim,coordsPlacesAccess,i,j)
        cheminPlace = rechercheCheminMin(parkingSim,i,j,iPlace,jPlace)
        
        if np.any(cheminPlace): # si la voiture peut
            (iSuiv,jSuiv) = cheminPlace[0]
            if (iSuiv,jSuiv) == (iPlace,jPlace):
                voitureGaree = True
        else:
            (iSuiv,jSuiv) = (i,j)

    else:
        tMoySortie += 1/NTOT_VOITURES
        if parking[i,j] == 1: # si la voiture est garée
            voitureRepart = random()>PROBA_SORTIE_GARAGE
        else:
            voitureRepart = True
        if voitureRepart:
            cheminSortie = rechercheCheminMin(parkingSim,i,j,I_SORTIE,J_SORTIE)
            if np.any(cheminSortie): # si la voiture peut sortir de sa place
                (iSuiv,jSuiv) = cheminSortie[0]
                
                if (iSuiv,jSuiv) == (I_SORTIE,J_SORTIE):
                    refresh(parkingSim,parking,i,j,I_SORTIE,J_SORTIE)
                    return [], tMoyGarage, tMoySortie
            else:
                (iSuiv,jSuiv) = (i,j)
        else:
            (iSuiv,jSuiv) = (i,j)

    refresh(parkingSim,parking,i,j,iSuiv,jSuiv)
    return [(iSuiv,jSuiv),voitureGaree], tMoyGarage, tMoySortie

if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")
