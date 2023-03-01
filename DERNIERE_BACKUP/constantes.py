"""
Programme secondaire répertoriant les constantes.
"""


# Valeurs pour l'algorithme génétique
N_PARKINGS = 100
N_GENERATIONS = 1000

PROBA_RANDOM_MUT = 0.3
COEFF_DEVIATION_MUT = 1


# Caractéristiques des parkings
LONGUEUR_PARKING = 15
LARGEUR_PARKING = 15

I_ENTREE = I_SORTIE = LARGEUR_PARKING//2
J_ENTREE, J_SORTIE = 0, LONGUEUR_PARKING-1


# Propriétés des simulations 
N_ITERATIONS = 300

FREQ_APPARITION_VOITURES = 3
NTOT_VOITURES = N_ITERATIONS//FREQ_APPARITION_VOITURES + 1

DUREE_MOY_GARAGE = 300
PROBA_SORTIE_GARAGE = DUREE_MOY_GARAGE/N_ITERATIONS

# Constantes de représentation
NUM_MUR = -1
NUM_ROUTE = 0
NUM_PLACE = 1
NUM_VOITURE = 2

SCORE_SEUIL = 1
SCORE_MAUVAIS = float('inf')

if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")
