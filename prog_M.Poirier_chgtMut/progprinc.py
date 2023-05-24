from constantes import *
from fonctions import *
#from fonctions_affichage import *
from fonctions_techniques import *
import matplotlib.pyplot as plt
import numpy as np

## Début du programme


# X = np.linspace(0,10,5)
#
# plt.plot(X,X**2)
#
#

def main():

    global PROBA_RANDOM_MUT

    n = 10

    x = np.arange(0,N_GENERATIONS,1)

   # for croisement in []
    for p in ['alea','allong_r','devia_r']:

        print("-"*10)
        print(p)

        evolScores_liste = np.zeros((n, N_GENERATIONS))

        for i in range(n) :
            print("*"*10)
            print(i)

            evolScores,evolParkings = evolutionGenetique(p)
            evolScores_liste[i] = np.array(evolScores)

        evolScores_moy = np.average(evolScores_liste, axis=0)
        evolScores_std = np.std(evolScores_liste, axis=0)

        #plt.plot(x, evolScores_moy, label =str(PROBA_RANDOM_MUT))
        plt.errorbar(x, evolScores_moy, yerr = evolScores_std, label =str(p))

    plt.legend()
    plt.show()
    '''
    evolDerniereGen = np.zeros((N_PARKINGS,LARGEUR_PARKING,LONGUEUR_PARKING))
    for i in range(N_PARKINGS):
        evolDerniereGen[i] = derniereGenxScores[i][0]
    '''
    # affichageLoop(evolDerniereGen)
    #
    # affichageLoop(evolParkings)


if __name__ == '__main__':
    main()

'''

>> Conseil: dès que stagne, remplacer 3/4 des parkings de façon random && garder minimum local (maybe niquel)
>> Changer mettre np.save pour open et tout :)

Idées à tester:
>> algo génétique progressif ?
>> Jviens de mettre une mutation random dès que stagne mais pb: modifie trop parkings et pabo score: dispersion de fou au nv scores
    -> Maybe faire plutôt avec fct ajoutBoutRoute ?
    -> Ajouter chance mutation aléa pour chacun des enfants >> diversité génétique ?


Problèmes (on ignore sagement):
- Les parkings se ressemblent tous: limite évolution
- Croisement inutile ?

A faire:
- Ajout autres croisements: 1 case/2, en 1 pt
- Ajout autres mutations: mutation avec plusieurs mutations de bloc de route

Idées (je le ferai jamais):
- Si stagnation, lancer plusieurs algo génétiques en même temps >> intervertir parkings entre eux

But actuel:
- Tester algo génétique avec différents scores >> différents parkings puis comparer
parkings avec score A* long >> voir meilleure méthode
- Faire varier tous les paramètres à la fin >> voir affectation

'''
