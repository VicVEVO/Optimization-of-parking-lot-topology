from fonctions_techniques import *
from constantes import *
#from fonctions_affichage import *
from fonctions_algogen import *

import numpy as np
from random import randint,random
from time import time
from copy import deepcopy

import matplotlib.pyplot as plt

def creationRandomParking(longueur,largeur):
    return np.random.randint(NUM_MUR, NUM_VOITURE, size=(largeur, longueur))

def _parking_cool_test(longueur,largeur):

    parking = np.ones((largeur,longueur),dtype=int)

    for j in range(1,longueur-1):
        if j%3 == 1:
            for i in range(1,largeur-1):
                parking[i,j] = NUM_ROUTE
        else:
            parking[:,j] = NUM_PLACE

    for i in [1,largeur//2,largeur-1]:
        parking[i,1:longueur-1] = NUM_ROUTE

    parking[largeur//2,0], parking[largeur//2,longueur-1] = NUM_ROUTE, NUM_ROUTE

    return np.array(parking)

def selectionPopParkings(popParkingsxScore):
    """
    Fonction renvoyant les parkings associés à leur score, triés par score
    croissant, et une sauvegarde des 2 meilleurs qui ne seront pas modifiés
    """

    resultats = []

    for numParking in range(N_PARKINGS):
        parking = popParkingsxScore[numParking][0]
        scoreParking = score(parking)
        resultats.append([parking,scoreParking])

    resultats = np.array(resultats,dtype=object)
    resultats = resultats[resultats[:,1].argsort()]

    meilleurParking1 = deepcopy(resultats[0])
    meilleurParking2 = deepcopy(resultats[1])
    return ([(meilleurParking1[0],meilleurParking1[1])]+[(meilleurParking2[0],meilleurParking2[1])]+[(resultats[i][0],resultats[i][1]) for i in range(N_PARKINGS//2-2)])

def croisementParkings(popParkingsxScores,p):
    grosseListeParkings = []

    for i in range(0,N_PARKINGS//2,2):
        (pere,scorePere), (mere,scoreMere) = popParkingsxScores[i], popParkingsxScores[i+1]
        if p == "coupure":
            parkingsAjout = croisement2Coupage(pere,scorePere,mere,scoreMere)
        else:
            parkingsAjout = croisementAleatoire(pere,scorePere,mere,scoreMere)
        """
        if scorePere>SCORE_SEUIL or scoreMere>SCORE_SEUIL:
            parkingsAjout = croisement2Coupage(pere,scorePere,mere,scoreMere)
        else:
            parkingsAjout = croisement2Coupage(pere,scorePere,mere,scoreMere)
        """
        grosseListeParkings += parkingsAjout

    return grosseListeParkings

def mutationParkings(popParkingsxScore,stagnationPop):
    for numParking in range(2,N_PARKINGS):
        (parking,score) = popParkingsxScore[numParking]

        mutationRandom(parking)
        # if score > SCORE_SEUIL:
        #     mutationRandom(parking,PROBA_RANDOM_MUT)
        # elif stagnationPop:
        #     mutationRandom(parking,PROBA_RANDOM_MUT/20)
        # else:
        #     mutationAjoutBoutRoute(parking)
        popParkingsxScore[numParking] = (parking,score)
    return popParkingsxScore

def stagne(evolScores):
    return len(evolScores) < SEUIL_STAGNATION or evolScores[-SEUIL_STAGNATION] == evolScores[-1]

def evolutionGenetique(p):

    popParkingsxScores = [(creationRandomParking(LONGUEUR_PARKING,LARGEUR_PARKING),SCORE_MAUVAIS) for _ in range(N_PARKINGS)]
    evolScores = []
    evolParkings = np.zeros((N_GENERATIONS,LARGEUR_PARKING,LONGUEUR_PARKING))
    for _ in range(N_GENERATIONS):
        t1 = time()
        popParkingsxScores = selectionPopParkings(popParkingsxScores)
        meilleurActuel = popParkingsxScores[0]
        popParkingsxScores = croisementParkings(popParkingsxScores,p)
        stagnationPop = stagne(evolScores)
        popParkingsxScores = mutationParkings(popParkingsxScores,stagnationPop)

        evolParkings[_] = meilleurActuel[0]
        evolScores.append(meilleurActuel[1])

        t2 = time()
        print(meilleurActuel[1],'//',np.round(t2-t1,1),'//',_)

    #affichageEvolScore(np.array(evolScores))
    #diagrammeDispersionScores(np.array(popParkingsxScores)[:,1])

    return evolScores,evolParkings


def evolutionPasGenetique():

    parking_max = creationRandomParking(LONGUEUR_PARKING,LARGEUR_PARKING)
    score_max = score(parking_max)

    Parkings = [(creationRandomParking(LONGUEUR_PARKING,LARGEUR_PARKING),SCORE_MAUVAIS) for _ in range(N_PARKINGS)]
    evolScores = []
    evolParkings = np.zeros((N_GENERATIONS,LARGEUR_PARKING,LONGUEUR_PARKING))
    for _ in range(N_GENERATIONS):
        t1 = time()

        Parkings = [(creationRandomParking(LONGUEUR_PARKING,LARGEUR_PARKING),SCORE_MAUVAIS) for _ in range(N_PARKINGS)]

        for numParking in range(N_PARKINGS):
            parking = Parkings[numParking][0]
            scoreParking = score(parking)
            if scoreParking < score_max:
                score_max = scoreParking
                parking_max = parking

        evolScores.append(score_max)

        t2 = time()
        print(score_max,'//',np.round(t2-t1,1),'//',_)


    #affichageEvolScore(np.array(evolScores))
    #diagrammeDispersionScores(np.array(popParkingsxScores)[:,1])

    return evolScores,evolParkings

if __name__ == '__main__':
    p1 = _parking_cool_test(LONGUEUR_PARKING,LARGEUR_PARKING)
    affichage(p1)
    print(score(p1))

    #print("Ce programme n'est pas destiné à être lancé.")
