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

Idées à tester:
- Algo génétique progressif (N_itérations augmente au fur et à mesure)
- Faire stopper la simulation dès qu'aucune voiture ne peut bouger >> faster

Problèmes:
- Croisement inutile
- Bcp trop long de faire score algo gén A* >> limite nb générations && nb parkings

A faire:
- Tester algo génétique avec différents scores >> différents parkings puis comparer
parkings avec score A* long >> voir meilleure méthode

'''
