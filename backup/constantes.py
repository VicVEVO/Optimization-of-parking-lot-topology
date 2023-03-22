"""
Programme secondaire répertoriant les constantes.
"""

# Valeurs pour l'algorithme génétique
N_PARKINGS = 500
N_GENERATIONS = 1500

PROBA_RANDOM_MUT = 0.3
PROBA_TRANSPOSE = 0.05
COEFF_DEVIATION_MUT = 1

SCORE_MAUVAIS = float('inf')
SCORE_SEUIL = 1
SCORE_SUP = -100

T_MAX_VOIT = 10 # 1 voiture/10sec
T_MIN_VOIT = 1 # 1 voiture/sec

a_T = (T_MIN_VOIT-T_MAX_VOIT)/(SCORE_SEUIL-abs(SCORE_SUP))
b_T = T_MAX_VOIT - a_T*SCORE_SEUIL


# Caractéristiques des parkings
LONGUEUR_PARKING = 15
LARGEUR_PARKING = 15

COORDS_ENTREES = {(LARGEUR_PARKING//2,0),(0,LONGUEUR_PARKING//2),(0,0)}
COORDS_SORTIES = {(LARGEUR_PARKING//2,LONGUEUR_PARKING-1)}


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

if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")