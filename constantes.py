"""
Programme secondaire répertoriant les constantes.
"""

I_TYPE_CASE = 0
N_ITERATIONS = 100
DUREE_GARAGE = 50 #s/iterations
PROBA_MUTATION = 0.3
PROBA_APPARITION_NV_ROUTE = 0.2 # pas utilisé
LONGUEUR_PARKING = 10
LARGEUR_PARKING = 10
N_CASES_MUTEES = 1
I_ENTREE = I_SORTIE = LARGEUR_PARKING//2
J_ENTREE, J_SORTIE = 0, LONGUEUR_PARKING-1
DIRECTION_INIT = 1
TAUX_DEVIATION = 2
NB_ROUTES_GEN = 1
FREQUENCE_APPARITION = 3
NTOT_VOITURES = N_ITERATIONS//FREQUENCE_APPARITION + 1 # nb total de voitures qui apparaîtront
N_PARKINGS = 100
N_GENERATIONS = 1000

if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")
