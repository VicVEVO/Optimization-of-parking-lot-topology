from constantes import *
from fonctions import *
from fonctions_affichage import *
from fonctions_techniques import *

## Début du programme

def main():
    evolParkings = evolutionGenetique()
    affichageLoop(evolParkings)

if __name__ == '__main__':
    main()
