import numpy as np
import time

def coords_veh(L):
    coords = []
    for i in range(len(L)-1,-1,-1):
        if L[i] >= 0: #si on a une voiture immobile ou non
            coords.append(i)
    return coords

def update(L,coords):
    for num_case in coords: #on étudie chaque voiture de droite à gauche (si elles vont de gauche à droite)
        if L[num_case]>0: #si on étudie une voiture avançant
            if num_case == len(L): #si on a une voiture tout à droite qui avance, elle disparaît du champ
                L[num_case] = 0
            elif L[num_case+1] not in cases_stop: #si devant il y a une voiture avançant
                L[num_case],L[num_case+1] = L[num_case+1],L[num_case]
            else: #si devant il y a une voiture à l'arrêt
                L[num_case] = 0 #elle s'arrete aussi

    return(L)


taille = 10
nb_iterations = 10
cases_stop = [0]

L = -np.ones(taille)

L[0],L[4],L[8] = 1,1,0

print(L)

for i in range(nb_iterations):
    L = update(L,coords_veh(L))
    time.sleep(1)
    print(L)