from fonctions_techniques import *
from constantes import *
from fonctions_affichage import *

import numpy as np
from random import randint,random
from copy import deepcopy

def creationRandomParking(longueur,largeur):
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

def simulation(parking):
    #evolParkings = np.zeros((N_ITERATIONS,LARGEUR_PARKING+2,LONGUEUR_PARKING))
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
        #evolParkings[k] = parkingSim
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
    entreePasDansRoute = not np.any(coordsRoute)
    
    if entreePasDansRoute:
        return 99999

    nbBlocsRoute = np.count_nonzero((parking == 0))
    sortieDansRoute = np.any(np.all([I_SORTIE,J_SORTIE] == coordsRoute, axis=1))

    if sortieDansRoute:
        scoreDuree = simulation(parking)
        #nbPlacesAccessibles = len(placesBordsRoute(parking))
        scoreConnexité = 1-100/scoreDuree
    else:
        tailleRoute = len(coordsRoute)
        scoreConnexité = 1+1/(tailleRoute) # tend vers 1 pour un bon parking

    return scoreConnexité

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

def mutationMauvais(parking):
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
    coordsRoute = coordonneesRoutes(parking)
    sensAllongement = ['haut','bas'][randint(0,1)]
    (iCoup1,jCoup1) = coordsRoute[coordsRoute[:,1] >= randint(0,LARGEUR_PARKING-2)][0]
    (iCoup2,jCoup2) = coordsRoute[coordsRoute[:,1] >= randint(jCoup1+1,LARGEUR_PARKING-1)][0] # on choisit d'autres coordonnées
    (iCoup1,jCoup1) , (iCoup2,jCoup2) = coordonneesFrontiere(iCoup1,jCoup1,parking,sensAllongement) , coordonneesFrontiere(iCoup2,jCoup2,parking,sensAllongement)
    enleveRoute(parking,iCoup1,jCoup1,iCoup2,jCoup2,coordsRoute,sensAllongement)
    ajouteRoute(parking,iCoup1,jCoup1,iCoup2,jCoup2)
    return parking

def mutationParkings(popParkingsxScore):
    for numParking in range(2,N_PARKINGS):
        (parking,score) = popParkingsxScore[numParking]
        if score > 1:
            mutationMauvais(parking)
        else:
            mutationMauvais(parking)
        popParkingsxScore[numParking] = (parking,score)
    return popParkingsxScore

def evolutionGenetique():

    popParkingsxScores = [(creationRandomParking(LONGUEUR_PARKING,LARGEUR_PARKING),0) for _ in range(N_PARKINGS)]
    EvolScores = np.empty(N_GENERATIONS)
    evolParkings = np.zeros((N_GENERATIONS,LARGEUR_PARKING,LONGUEUR_PARKING))

    for _ in range(N_GENERATIONS):
        popParkingsxScores = selectionPopParkings(popParkingsxScores)
        meilleurActuel = popParkingsxScores[0]

        popParkingsxScores = croisementParkings(popParkingsxScores)

        popParkingsxScores = mutationParkings(popParkingsxScores)
        
        evolParkings[_] = meilleurActuel[0]
        EvolScores[_] = meilleurActuel[1]

    affichageEvolScore(EvolScores)
    diagrammeDispersionScores(np.array(popParkingsxScores)[:,1])
    return evolParkings

def test():
    P = _parking_cool_test(LONGUEUR_PARKING,LARGEUR_PARKING)
    simulation(P)

if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")
