from fonctions_techniques import *
from constantes import *
from fonctions_affichage import *

import numpy as np
from random import randint,random
from copy import deepcopy
from time import time

def creationRandomParking(longueur,largeur): #ok
    return np.random.randint(-1, 2, size=(largeur, longueur))

def _parking_cool_test(longueur,largeur):
    
    bords = -np.ones(longueur,dtype=int)

    parking = -np.ones((largeur,longueur),dtype=int)
    
    for x in range(3,longueur-1):
        if x%4 == 1 or x%4 == 2:
            for y in range(2,largeur-2):
                parking[y,x] = 1
        else:
            parking[:,x] = 0 # files vides

    parking[largeur//2],parking[largeur//2-1] = 0,0 # création de la route principale 
    parking[0,3:-1],parking[1,3:-1],parking[-1,3:-1],parking[-2,3:-1] = 0,0,0,0 # création des routes des fins de files

    parking = np.append(bords,parking).reshape(largeur+1,longueur)
    parking = np.append(parking,bords).reshape(largeur+2,longueur)

    return np.array(parking)

def simulation(parking): #ok
    #evolParkings = np.zeros((N_ITERATIONS,LARGEUR_PARKING+2,LONGUEUR_PARKING))
    #evolParkings = np.zeros((N_ITERATIONS,LARGEUR_PARKING,LONGUEUR_PARKING))
    voitures = []
    parkingSim = deepcopy(parking)
    coordsPlacesAccess = placesBordsRoute(parking)
    tMoyGarage,tMoySortie = 0,0

    for k in range(N_ITERATIONS):
        if k%FREQUENCE_APPARITION==0:
            voitures.append([(I_ENTREE,J_ENTREE),False])
        for numVoiture in range(len(voitures)):
            if voitures[numVoiture]: # si la voiture n'est pas arrivée
                voitures[numVoiture], tMoyGarage, tMoySortie = nvVoiture(voitures[numVoiture],parkingSim,parking,coordsPlacesAccess,tMoyGarage,tMoySortie)
    #    evolParkings[k] = parkingSim
    #affichageLoop(evolParkings)
    return tMoyGarage

def score(parking):
    """
    Score en 2 parties:
    Si parking pas connexe:
        - Doit privilégier taille route principale
    - Doit ensuite privilégier une route avec bcp de places dispo (<=> on s'y gare vite)
    """
    coordsRoute = coordonneesRoutes(parking)
    entreePasDansRoute = coordsRoute == set()
    if entreePasDansRoute:
        return 99999

    nbBlocsRoute = np.count_nonzero((parking == 0))
    sortieDansRoute = (I_SORTIE,J_SORTIE) in coordsRoute

    if sortieDansRoute:
        dureeGarage = simulation(parking)
        #nbPlacesAccessibles = len(placesBordsRoute(parking))
        #score1 = 1-nbPlacesAccessibles
        score1 = 1-150/dureeGarage
        return score1
    else:
        tailleRoute = len(coordsRoute)
        score2 = 1+1/(tailleRoute)
        return score2
        
def selectionPopParkings(popParkingsxScore):
    
    resultats = []

    for numParking in range(N_PARKINGS):
        parking = popParkingsxScore[numParking][0]
        scoreParking = score(parking)
        resultats.append([parking,scoreParking])

    resultats = np.array(resultats,dtype=object)
    resultats = resultats[resultats[:,1].argsort()] # on trie les parkings par score croissant

    meilleurParking1 = deepcopy(resultats[0]) # on garde des sauvegardes des 2 meilleurs
    meilleurParking2 = deepcopy(resultats[1])
    return ([(meilleurParking1[0],meilleurParking1[1])]+[(meilleurParking2[0],meilleurParking2[1])]+[(resultats[i][0],resultats[i][1]) for i in range(N_PARKINGS//2-2)]) # on renvoie les (parkings,score)

def croisementMauvais(P1,scoreP1,P2,scoreP2):
        iCoupage,jCoupage = randint(0,LARGEUR_PARKING-1),randint(J_ENTREE,J_SORTIE)
        p3, p4 = np.copy(P1), np.copy(P2)

        p3[:iCoupage,:jCoupage] = P2[:iCoupage,:jCoupage] # p3 hérite d'une zone supérieure de P2 
        p4[:iCoupage,:jCoupage] = P1[:iCoupage,:jCoupage] # p4 hérite d'une zone supérieure de P1
        
        return [(P1,scoreP1),(P2,scoreP2),(p3,score(p3)),(p4,score(p4))]

def croisementBon(P1,scoreP1,P2,scoreP2):
    coordonneesRouteP1, coordonneesRouteP2 = coordonneesRoutes(P1), coordonneesRoutes(P2)
    p3, p4 = np.copy(P1), np.copy(P2)
    
    for (i,j) in coordonneesRouteP1:
        p4[i,j] = 0 # p4 hérite de la route de P1
    for (i,j) in coordonneesRouteP2:
        p3[i,j] = 0 # p3 hérite de la route de P2
        
    return [(P1,scoreP1),(P2,scoreP2),(p3,score(p3)),(p4,score(p4))]

def croisementParkings(popParkingsxScores):
    grosseListeParkings = []

    for i in range(0,N_PARKINGS//2,2):
        (pere,scorePere), (mere,scoreMere) = popParkingsxScores[i], popParkingsxScores[i+1]
        if scorePere>1 or scoreMere>1:
            parkingsAjout = croisementMauvais(pere,scorePere,mere,scoreMere)
        else:
            parkingsAjout = croisementMauvais(pere,scorePere,mere,scoreMere)
        grosseListeParkings += parkingsAjout
    
    return grosseListeParkings

def mutationRandom(parking):
    coordsRoute = coordonneesRoutes(parking)
    for i in range(LARGEUR_PARKING):
        for j in range(LONGUEUR_PARKING):
            if (i,j) != (I_ENTREE,J_ENTREE) and (i,j) != (I_SORTIE,J_SORTIE):
                if random()<PROBA_MUTATION:
                    parking[i,j] = [-1,0,1][randint(0,2)]

def mutationBon(parking):
    """
    Si le parking est bon on modifie une des trajectoires de sa route principale.
    """
    coordsRoute = np.array(list(coordonneesRoutes(parking)))
    sensAllongement = ['haut','bas'][randint(0,1)]

    (iCoup1,jCoup1), (iCoup2,jCoup2) = coordonneesCoupage(parking,coordsRoute,sensAllongement)
    
    enleveRoute(parking,iCoup1,jCoup1,iCoup2,jCoup2,coordsRoute,sensAllongement)
    ajouteRoute(parking,iCoup1,jCoup1,iCoup2,jCoup2)
    return parking

def neCassePas(iSuppr,jSuppr,parking):
    """
    fct qui verifie si la route n'est pas cassée en remplacant un bloc du parking
    """
    parkingModifie = deepcopy(parking)
    parkingModifie[iSuppr,jSuppr] = -1 # on remplace le bloc de route par un bloc de mur
    return (I_SORTIE,J_SORTIE) in coordonneesRoutes(parkingModifie)

def mutationAjoutBoutRoute(parking):
    coordsRoute = np.array(list(coordonneesRoutes(parking)))
    nbBlocsRoute = len(coordsRoute) - 1
    
    (iAjout,jAjout) = coordsRoute[randint(0,nbBlocsRoute)]
    sensAjout = ['haut','bas','gauche','droite'][randint(0,3)] # on ajoute de la route en haut, en bas, à gauche ou à droite
    (iAjout,jAjout) = coordonneesFrontiere(iAjout,jAjout,parking,sensAjout,'ajout_morceau_route')

    if (iAjout,jAjout) != (I_ENTREE,J_ENTREE) and (iAjout,jAjout) != (I_SORTIE,J_SORTIE):
        parking[iAjout,jAjout] = 0
        
    ## On supprime un bloc random de route
    placesRouteParking = np.argwhere(parking == 0)
    [iSuppr,jSuppr] = placesRouteParking[randint(0,placesRouteParking.shape[0]-1)]
    if neCassePas(iSuppr,jSuppr,parking):
        parking[iSuppr,jSuppr] = [-1,1][randint(0,1)]

def mutationParkings(popParkingsxScore):
    for numParking in range(2,N_PARKINGS):
        (parking,score) = popParkingsxScore[numParking]
        if score > 1: # si le parking ne lie pas l'entrée à la sortie
            mutationRandom(parking)
        else:
            mutationAjoutBoutRoute(parking)
        popParkingsxScore[numParking] = (parking,score)
    return popParkingsxScore

def evolutionGenetique():

    popParkingsxScores = [(creationRandomParking(LONGUEUR_PARKING,LARGEUR_PARKING),0) for _ in range(N_PARKINGS)]
    EvolScores = np.empty(N_GENERATIONS)
    evolParkings = np.zeros((N_GENERATIONS,LARGEUR_PARKING,LONGUEUR_PARKING))

    for _ in range(N_GENERATIONS):
        t1 = time()
        popParkingsxScores = selectionPopParkings(popParkingsxScores)
        meilleurActuel = popParkingsxScores[0]

        popParkingsxScores = croisementParkings(popParkingsxScores)

        popParkingsxScores = mutationParkings(popParkingsxScores)
        
        evolParkings[_] = meilleurActuel[0]
        EvolScores[_] = meilleurActuel[1]
        t2 = time()
        print(meilleurActuel[1],'duree:',t2-t1,_)

    affichageEvolScore(EvolScores)
    diagrammeDispersionScores(np.array(popParkingsxScores)[:,1])
    return evolParkings

def testMutation():
    P = 1 + np.zeros((LARGEUR_PARKING,LONGUEUR_PARKING))
    P[I_ENTREE] = 0
    A = np.zeros((500,LARGEUR_PARKING,LONGUEUR_PARKING))
    for i in range(500):
        A[i] = P
        mutationAjoutBoutRoute(P)
    affichageLoop(A)

def testSim():
    P = _parking_cool_test(LONGUEUR_PARKING,LARGEUR_PARKING)
    #P = creationRandomParking(LONGUEUR_PARKING,LARGEUR_PARKING)
    t = time()
    s = simulation(P)
    print(time()-t)
    print(s)

if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")
