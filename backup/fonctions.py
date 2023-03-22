from fonctions_techniques import *
from constantes import *
from fonctions_affichage import *
from fonctions_algogen import *

import numpy as np
from random import randint,random
from time import time
from copy import deepcopy

def creationRandomParking(longueur,largeur):
    return np.random.randint(NUM_MUR, NUM_VOITURE, size=(largeur, longueur))

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

def croisementParkings(popParkingsxScores):
    grosseListeParkings = []

    for i in range(0,N_PARKINGS//2,2):
        (pere,scorePere), (mere,scoreMere) = popParkingsxScores[i], popParkingsxScores[i+1]
        if scorePere>SCORE_SEUIL or scoreMere>SCORE_SEUIL:
            parkingsAjout = croisement2Coupage(pere,scorePere,mere,scoreMere)
        else:
            parkingsAjout = croisement2Coupage(pere,scorePere,mere,scoreMere)
        grosseListeParkings += parkingsAjout
    
    return grosseListeParkings

def mutationParkings(popParkingsxScore):
    for numParking in range(2,N_PARKINGS):
        (parking,score) = popParkingsxScore[numParking]
        if score > SCORE_SEUIL:
            mutationRandom(parking)
        else:
            mutationAjoutBoutRoute(parking)
        popParkingsxScore[numParking] = (parking,score)
    return popParkingsxScore

def evolutionGenetique():

    popParkingsxScores = [(creationRandomParking(LONGUEUR_PARKING,LARGEUR_PARKING),SCORE_MAUVAIS) for _ in range(N_PARKINGS)]
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
        print(meilleurActuel[1],'//',np.round(t2-t1,1),'//',_)

    affichageEvolScore(EvolScores)
    diagrammeDispersionScores(np.array(popParkingsxScores)[:,1])
    return evolParkings,popParkingsxScores

if __name__ == '__main__':
    p = _parking_cool_test(LONGUEUR_PARKING,LARGEUR_PARKING)
    print(score(p))
    #print("Ce programme n'est pas destiné à être lancé.")
