"""
À changer:
"""


from fonctions_techniques import *
from constantes import *
from fonctions_affichage import *

import numpy as np
from random import randint,random
from copy import deepcopy

def creationRandomParking(longueur,largeur):
    return np.random.randint(-1, 2, size=(largeur, longueur))

def simulation(parking):
    voitures = []
    parkingSim = deepcopy(parking)
    tMoyGarage,tMoySortie = 0,0

    for k in range(N_ITERATIONS):
        if k%FREQUENCE_APPARITION==0:
            voitures.append([(I_ENTREE,J_ENTREE),False])
        for numVoiture in range(len(voitures)):
            if voitures[numVoiture]: # si la voiture n'est pas arrivée
                voitures[numVoiture], tMoyGarage, tMoySortie = nvVoiture(voitures[numVoiture],parkingSim,parking,tMoyGarage,tMoySortie)

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
        #x = simulation(parking)
        nbPlacesAccessibles = len(placesBordsRoute(parking))
        scoreConnexité = 1-nbPlacesAccessibles
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
    return ([(resultats[i][0],resultats[i][1]) for i in range(N_PARKINGS//2)],deepcopy(resultats[0])) # on renvoie (parkings,score)

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
    print(len(coordsRoute))
    affichage(parking)
    enleveRoute(parking,iCoup1,jCoup1,iCoup2,jCoup2,coordsRoute,sensAllongement)
    ajouteRoute(parking,iCoup1,jCoup1,iCoup2,jCoup2)
    return parking

def mutationParkings(popParkingsxScore):
    for numParking in range(N_PARKINGS):
        (parking,score) = popParkingsxScore[numParking]
        if score > 1:
            mutationMauvais(parking)
        else:
            mutationMauvais(parking)
        popParkingsxScore[numParking] = (parking,score)
    return popParkingsxScore

def evolutionGenetique():
    popParkingsxScores = [(creationRandomParking(LONGUEUR_PARKING,LARGEUR_PARKING),0) for _ in range(N_PARKINGS)]
    evolParkings = np.zeros((N_GENERATIONS,LARGEUR_PARKING,LONGUEUR_PARKING))
    for _ in range(N_GENERATIONS):
        (popParkingsxScores,meilleurActuel) = selectionPopParkings(popParkingsxScores)
        popParkingsxScores = croisementParkings(popParkingsxScores)
        popParkingsxScores = mutationParkings(popParkingsxScores)
        
        popParkingsxScores.pop(-1)
        popParkingsxScores.append(meilleurActuel)

        evolParkings[_] = meilleurActuel[0]

        print(_,meilleurActuel[1],'\n')
    
    return evolParkings

if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")
