from constantes import *
from fonctions import *
from fonctions_affichage import *
from fonctions_techniques import *

## Début du programme

def main():

    evolParkings,derniereGenxScores = evolutionGenetique()
    saveData(evolParkings[0], "parkingsDerniereGenScore_{score}.csv".format(score=derniereGenxScores[0][1]))
    
    '''
    evolDerniereGen = np.zeros((N_PARKINGS,LARGEUR_PARKING,LONGUEUR_PARKING))
    for i in range(N_PARKINGS):
        evolDerniereGen[i] = derniereGenxScores[i][0]
    '''
    affichageLoop(evolDerniereGen)

    affichageLoop(evolParkings)


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
