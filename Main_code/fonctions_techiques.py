from constantes import *

import numpy as np
from random import randint, random

def rechercheCheminMin(parking,i1, j1, i2, j2, volOiseau=True,justeProchCoord=False):
    """
    Fonction renvoyant avec la méthode A* le chemin le plus court liant (i1,j1) et (i2,j2)
    Parameters
    ----------
    parking: array
    i1, j1, i2, j2: int
    volOiseau: bool
        Est vrai si on ignore les murs
    justeProchCoord: bool
        Est vrai si on ne veut que la première coordonnée du chemin le plus court (utilisé pour nvVoit)

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

    balFini = False

    while not balFini and V:
        minValue,minCoords = float('inf'),None
        for i,j in C.keys():
            if C[i,j] <= minValue and (i,j) in V:
                minValue,minCoords = C[i,j],(i,j)

        (i,j) = V.pop(V.index((minCoords[0],minCoords[1]))) # on examine le prochain indice dans la queue
        D[i,j] = True
        
        if i == i2 and j == j2:
            balFini = True
            
        else:
            for (iVois,jVois) in [(i, j+1), (i-1, j), (i, j-1), (i+1, j)]:
                if 0 <= iVois < LARGEUR_PARKING and 0 <= jVois < LONGUEUR_PARKING and not D[iVois, jVois]: # si la case n'est pas visitée
                    if parking[iVois,jVois] == NUM_ROUTE or volOiseau or (iVois,jVois) == (i2,j2):
                        D[iVois, jVois] = True
                        C[iVois, jVois] = C[i,j] + 1 + heuristique(iVois,jVois)
                        P[(iVois, jVois)] = (i, j) # on stocke les indices précédents pour i_vois,j_vois

    if not balFini or P == {}: # si les 2 points ne sont pas joignables
        if justeProchCoord:
            return (i1,j1)
        return [(i1,j1)]
    
    ### On renvoie la liste des coordonnées dans l'ordre en partant de l'arrivée
    
    chemin = []
    i, j = i2, j2
    while (i, j) in P:
        chemin.append((i, j))
        i, j = P[(i, j)]

    if justeProchCoord:
        if chemin:
            return chemin[-1]
        return (i1,j1)
    return list(reversed(chemin))

def coordonneesRoutes(parking):
    """
    Fonction renvoyant avec un parcours en profondeur l'ensemble des coordonnées
    des blocs de route sur chacune des routes principales (liant une entrée et une sortie)
    du parking.
    Returns: dict
    """
    coordsRoutes = {} # compo avec chacune coords routes
    for (iEntr, jEntr) in COORDS_ENTREES:
        casesVisitees = set()
        fileCoordsAVisiter = [(iEntr,jEntr)]
        
        while fileCoordsAVisiter:
            iBal,jBal = fileCoordsAVisiter.pop(0)
            if iBal < 0 or iBal >= LARGEUR_PARKING or jBal < 0 or jBal > LONGUEUR_PARKING-1:
                continue

            if parking[iBal,jBal] != NUM_ROUTE or (iBal,jBal) in casesVisitees:
                continue
            casesVisitees.add((iBal,jBal))
            fileCoordsAVisiter.extend([(iBal-1,jBal),(iBal+1,jBal),(iBal,jBal-1),(iBal,jBal+1)])
        
        casesVisiteesDejaMises = False
        for coordsRoute in coordsRoutes:
            if casesVisitees == coordsRoute:
                casesVisiteesDejaMises = True
        if not casesVisiteesDejaMises and casesVisitees != set():
            coordsRoutes[(iEntr,jEntr)] = casesVisitees
    return coordsRoutes

def neCassePas(iSuppr,jSuppr,parking):
    """
    Fonction vérifiant si la linéarité du parking n'est pas supprimée en
    remplacant un de ses blocs par un bloc de mur.
    """
    parkingModifie = np.copy(parking)
    parkingModifie[iSuppr,jSuppr] = NUM_MUR
    coordsRoutesParkingModif = coordonneesRoutes(parkingModifie)
    for (iEntr,jEntr) in coordsRoutesParkingModif:
        for (iSortie,jSortie) in COORDS_SORTIES:
            if (iSortie,jSortie) in coordsRoutesParkingModif[iEntr,jEntr]:
                return True
    return False

def coordonneesFrontiere(i,j,parking,sens,etape=''):
    """
    Fonction renvoyant les coordonnées des bordures de la route principale.
    Si on appelle cette fonction pour ajouter un morceau de route on s'intéresse
    aux coordonnés externes.
    """
    epsi = 1
    if etape == 'ajout_morceau_route':
        epsi = 0

    if sens == "haut":
        for ligne in range(i-1, -1, -1):
            if parking[ligne][j] != NUM_ROUTE:
                return (ligne+epsi, j)
    elif sens == "bas":
        for ligne in range(i+1, LARGEUR_PARKING):
            if parking[ligne][j] != NUM_ROUTE:
                return (ligne-epsi, j)
    elif sens == "gauche":
        for colonne in range(j-1, -1, -1):
            if parking[i][colonne] != NUM_ROUTE:
                return (i, colonne+epsi)
    elif sens == "droite":
        for colonne in range(j+1, LONGUEUR_PARKING):
            if parking[i][colonne] != NUM_ROUTE:
                return (i, colonne-epsi)
    return (i,j) 

def coordonneesDerivation(i0,j0,i1,j1):
    """
    Fonction renvoyant des coordonnées sur la médiatrice de la droite liant
    (i0,j0) à (i1,j1)
    """
    iMil = int((i0 + i1) / 2)
    jMil = int((j0 + j1) / 2)
    coordonnees = []

    if i0 == i1: # si on a une ligne horizontale joignant (i0,j0) à (i1,j1)
        iChoisi = randint(max(iMil-COEFF_DEVIATION_MUT,0),min(iMil+COEFF_DEVIATION_MUT,LARGEUR_PARKING-1))
        return(iChoisi,jMil)

    elif j0 == j1: # si la ligne est verticale
        jChoisi = randint(max(jMil-COEFF_DEVIATION_MUT,0),min(jMil+COEFF_DEVIATION_MUT,LONGUEUR_PARKING-1))
        return(iMil,jChoisi)
        
    else: # sinon on a une droite d'équation i=mj+p
        m = -1/((j1 - j0) / (i1 - i0))
        p = iMil - (m * jMil)
        if j0>j1:
            j0, j1 = j1, j0
        couples = []
        for j in range(j0,j1+1):
            i = int(m*j+p)
            if 0<=i<=LARGEUR_PARKING-1:
                couples.append((i,j))

        return couples[randint(0,len(couples)-1)]

def enleveRoute(parking,i0,j0,i1,j1,coordsRoute,sensAllongement):
    """
    Procédure enlevant la route liant (i0,j0) à (i1,j1) en la remplacant par
    d'autres blocs
    """
    for j in range(j0+1,j1):
        for i in range(LARGEUR_PARKING):
            for (iEntr,jEntr) in coordsRoute:
                if (i,j) in coordsRoute[iEntr,jEntr]:
                    parking[i,j] = [NUM_MUR,NUM_ROUTE,NUM_PLACE][randint(0,2)]
    if sensAllongement == 'bas':
        for i in range(i0+1,LARGEUR_PARKING):
            for (iEntr,jEntr) in coordsRoute:
                if (i,j0) in coordsRoute[iEntr,jEntr]:
                    parking[i,j0] = [NUM_MUR,NUM_ROUTE,NUM_PLACE][randint(0,2)]
        for i in range(i1+1,LARGEUR_PARKING):
            for (iEntr,jEntr) in coordsRoute:
                if (i,j1) in coordsRoute[iEntr,jEntr]:
                    parking[i,j1] = [NUM_MUR,NUM_ROUTE,NUM_PLACE][randint(0,2)]
    else:
        for i in range(i0-1,-1,-1):
            for (iEntr,jEntr) in coordsRoute:
                if (i,j0) in coordsRoute[iEntr,jEntr]:
                    parking[i,j0] = [NUM_MUR,NUM_ROUTE,NUM_PLACE][randint(0,2)]
        for i in range(i1-1,-1,-1):
            for (iEntr,jEntr) in coordsRoute:
                if (i,j1) in coordsRoute:
                    parking[i,j1] = [NUM_MUR,NUM_ROUTE,NUM_PLACE][randint(0,2)]

def ajouteRoute(parking,i0,j0,i1,j1):
    """
    Procédure déviant la route joigant (i0,j0) à (i1,j1) sur le parking
    """
    (iDev, jDev) = coordonneesDerivation(i0,j0,i1,j1)
    chemin = [(i0,j0)] + rechercheCheminMin(parking,i0,j0,iDev,jDev) + rechercheCheminMin(parking,iDev,jDev,i1,j1)
    etape = 0
    nbEtapes = len(chemin)

    while etape != nbEtapes:
        (iBal,jBal) = chemin[etape]
        parking[iBal,jBal] = NUM_ROUTE
        etape += 1

def coordonneesCoupage(parking,coordsRoute,sensAllongement):
    """
    Fonction renvoyant 2 couples de coordonnées aléatoires sur la route à partir
    desquelles la route qui les a rejoint sera déviée
    """
    numRouteChoisicc1 = randint(0,len(coordsRoute)-1)
    coordsRoute1 = coordsRoute[numRouteChoisicc1]

    couplesCoup1 = coordsRoute1[(coordsRoute1[:,1] >= randint(0,int(2/3*LONGUEUR_PARKING))) & (coordsRoute1[:,1] <= 2/3*LONGUEUR_PARKING)]
    nbCouplesCoup1 = len(couplesCoup1)
    if nbCouplesCoup1 == 1:
        (iCoup1,jCoup1) = couplesCoup1[0]
    else:
        (iCoup1,jCoup1) = couplesCoup1[randint(0,nbCouplesCoup1-1)]
    
    numRouteChoisicc2 = randint(0,len(coordsRoute)-1)
    coordsRoute2 = coordsRoute[numRouteChoisicc1]

    couplesCoup2 = coordsRoute2[coordsRoute2[:,1] >= randint(jCoup1+1,LONGUEUR_PARKING-2)]
    nbCouplesCoup2 = len(couplesCoup2)
    if nbCouplesCoup2 == 1:
        (iCoup2,jCoup2) = couplesCoup2[0]
    else:
        (iCoup2,jCoup2) = couplesCoup2[randint(0,nbCouplesCoup2-1)]
    
    return coordonneesFrontiere(iCoup1,jCoup1,parking,sensAllongement), coordonneesFrontiere(iCoup2,jCoup2,parking,sensAllongement)

def placesBordsRoute(parking):
    """
    Fonction renvoyant le nombre de places disponibles depuis chacune des routes principale
    du parking
    >> return dict
    """
    coordsPlacesTot = {}
    coordsRoutesDepuisEntrees = coordonneesRoutes(parking)
    for (iEntr,jEntr) in coordsRoutesDepuisEntrees:
        coordsPlaces = set()
        
        for (iBal,jBal) in coordsRoutesDepuisEntrees[iEntr,jEntr]:
            coordonnes_entourant = [(iBal+1,jBal),(iBal,jBal+1),(iBal-1,jBal),(iBal,jBal-1)]
            for (iEntourant,jEntourant) in coordonnes_entourant:
                if 0<=iEntourant<=LARGEUR_PARKING-1 and 0<=jEntourant<=LONGUEUR_PARKING-1 and parking[iEntourant,jEntourant] == NUM_PLACE:
                    coordsPlaces.add((iEntourant,jEntourant))
        coordsPlacesTot[iEntr,jEntr] = np.array(list(coordsPlaces))
    return coordsPlacesTot

def coordonneesPlaceProche(parking,coordsPlacesAccess,i,j):
    """
    Fonction renvoyant les coordonnées de la place la plus proche de (i,j) selon
    la norme 1 (distance de Manhattan)
    """
    coordsPlacesLibres = []
    for (iEntr,jEntr) in coordsPlacesAccess:
        coordsPlacesLibres += [(x,y) for x,y in coordsPlacesAccess[iEntr,jEntr] if parking[x,y] != NUM_VOITURE]
    
    if coordsPlacesLibres == []:
        return (i,j)
    coordsPlacesLibres = np.array(coordsPlacesLibres)
    distancescoordsPlacesLibres = abs(coordsPlacesLibres[:,0]-i) + abs(coordsPlacesLibres[:,1]-j)
    indiceMin = np.argmin(distancescoordsPlacesLibres)
    return coordsPlacesLibres[indiceMin]

def coordonneesSortieProche(parking,i,j):
    """
    Fonction renvoyant les coordonnées de la sortie la plus proche de (i,j) selon
    la norme 1 (distance de Manhattan)
    """
    coordsSorties = np.array(list(COORDS_SORTIES))
    distancescoordsPlacesLibres = abs(coordsSorties[:,0]-i) + abs(coordsSorties[:,1]-j)
    indiceMin = np.argmin(distancescoordsPlacesLibres)
    return coordsSorties[indiceMin]

def refresh(parking,parkingRef,iPrec,jPrec,iSuiv,jSuiv):
    parking[iPrec,jPrec], parking[iSuiv,jSuiv] = parkingRef[iPrec,jPrec], NUM_VOITURE

def nvVoiture(voiture,parkingSim,parking,coordsPlacesAccess,tMoyGarage,tMoySortie): # À update à la fin avec plusieurs entrees & sorties
    """
    Fonction renvoyant la voiture actualisée, ayant un nouvel état et de
    nouvelles coordonnées
    """
    (i,j) = voiture[0]
    voitureEnSortie = voiture[1]
    if not voitureEnSortie:
        tMoyGarage += 1/NTOT_VOITURES
        (iPlace,jPlace) = coordonneesPlaceProche(parkingSim,coordsPlacesAccess,i,j)
        (iSuiv,jSuiv) = rechercheCheminMin(parkingSim,i,j,iPlace,jPlace,False,True)
        if parking[iSuiv,jSuiv] == NUM_PLACE:
            voitureEnSortie = True

    else:
        if parking[i,j] == NUM_PLACE:
            voitureRepart = random()>PROBA_SORTIE_GARAGE
        else:
            voitureRepart = True
        if voitureRepart:
            tMoySortie += 1/NTOT_VOITURES
            iSortie,jSortie = coordonneesSortieProche(parking,i,j)
            (iSuiv,jSuiv) = rechercheCheminMin(parkingSim,i,j,iSortie,jSortie,False,True)
            
            if (iSuiv,jSuiv) == (iSortie,jSortie):
                refresh(parkingSim,parking,i,j,iSortie,jSortie)
                return [], tMoyGarage, tMoySortie
        else:
            (iSuiv,jSuiv) = (i,j)

    refresh(parkingSim,parking,i,j,iSuiv,jSuiv)
    return [(iSuiv,jSuiv),voitureEnSortie], tMoyGarage, tMoySortie

def nvVoitureRandom(voiture,parkingSim,parking,tMoyGarage,tMoySortie):
    """
    Fonction renvoyant la voiture actualisée, ayant un nouvel état et de
    nouvelles coordonnées
    """
    (i,j) = voiture[0]
    voitureEnSortie = voiture[1]
    if not voitureEnSortie:
        tMoyGarage += 1/NTOT_VOITURES
        coordsPlacesProches, coordsRoutesProches = [], []

        for (iVois,jVois) in [(i, j+1), (i-1, j), (i, j-1), (i+1, j)]:
            
            if 0 <= iVois < LARGEUR_PARKING and 0 <= jVois < LONGUEUR_PARKING:
                if parkingSim[iVois,jVois] == NUM_ROUTE:
                    coordsRoutesProches.append((iVois,jVois))
                elif parkingSim[iVois,jVois] == NUM_PLACE:
                    coordsPlacesProches.append((iVois,jVois))
        
        if coordsPlacesProches != []:
            (iSuiv,jSuiv) = coordsPlacesProches[randint(0,len(coordsPlacesProches)-1)]
        elif coordsRoutesProches != []:
            (iSuiv,jSuiv) = coordsRoutesProches[randint(0,len(coordsRoutesProches)-1)]
        else:
            (iSuiv,jSuiv) = (i,j)
        
        if parking[iSuiv,jSuiv] == NUM_PLACE:
            voitureEnSortie = True
        
    else:
        
        if parking[i,j] == NUM_PLACE:
            voitureRepart = random()>PROBA_SORTIE_GARAGE
        else:
            voitureRepart = True

        if voitureRepart:
            tMoySortie += 1/NTOT_VOITURES
            coordsRoutesProches = []

            for (iVois,jVois) in [(i, j+1), (i-1, j), (i, j-1), (i+1, j)]:
                
                if 0 <= iVois < LARGEUR_PARKING and 0 <= jVois < LONGUEUR_PARKING:
                    if parkingSim[iVois,jVois] == NUM_ROUTE:
                        coordsRoutesProches.append((iVois,jVois))
            
            if coordsRoutesProches != []:
                (iSuiv,jSuiv) = coordsRoutesProches[randint(0,len(coordsRoutesProches)-1)]
            else:
                (iSuiv,jSuiv) = (i,j)

            if (iSuiv,jSuiv) in COORDS_SORTIES:
                refresh(parkingSim,parking,i,j,iSuiv,jSuiv)
                return [], tMoyGarage, tMoySortie
        else:
            (iSuiv,jSuiv) = (i,j)

    refresh(parkingSim,parking,i,j,iSuiv,jSuiv)
    return [(iSuiv,jSuiv),voitureEnSortie], tMoyGarage, tMoySortie


#####________________________

def count_parkings(parkings):
    occurences = {}
    for parking, _ in parkings:
        key = str(parking) # Convertir le numpy array en string pour pouvoir l'utiliser comme clé du dictionnaire
        occurences[key] = occurences.get(key, 0) + 1
    return occurences

def saveData(popParkings,name):
    np.savetxt(name,popParkings,delimiter=',')

def openData(name):
    return np.loadtxt(name,delimiter=',')

if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")
