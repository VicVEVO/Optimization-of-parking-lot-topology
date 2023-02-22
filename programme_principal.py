from constantes import *
from fonctions import *
from fonctions_affichage import *
from fonctions_techniques import *

## Début du programme

def main():
    evolParkings = evolutionGenetique()
    affichageLoop(evolParkings)
    #testMutation()
    #testSim()

if __name__ == '__main__':
    main()

'''
Idées à tester: Algo génétique progressif (N_itérations augmente au fur et à mesure)
                Faire stopper la simulation dès qu'aucune voiture ne peut bouger >> faster
Problèmes: croisement inutile
'''
