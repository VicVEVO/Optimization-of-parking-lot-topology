"""
score compacité parking : rapport entre surface occupée par les places de parking et surface totale du parking. Un parking compact est plus efficace car il permet de caser plus de voitures dans un espace réduit.
facilité de navigation : nombre de virages nécessaires pour atteindre une place de parking. Un parking qui permet d'accéder facilement aux places de parking est plus efficace.
"""

from fonctions_techniques import *
from fonctions_affichage import *
from fonctions import *
from constantes import *
from copy import deepcopy
from random import choice

### Fonctions de score

def scoreNombrePlaces(parking):
    nbPlacesAccessibles = 0
    placesAcc = placesBordsRoute(parking)
    for (i,j) in placesAcc:
        nbPlacesAccessibles += len(placesAcc[i,j])
    return SCORE_SEUIL - nbPlacesAccessibles

def scoreTailleRoute(parking,coordsRoute):
    tailleRoute = 0
    for (i,j) in coordsRoute:
        tailleRoute += len(coordsRoute[i,j])
    return SCORE_SEUIL + 1/(tailleRoute)

def periodeArriveeVoitures(score):
    return a_T*abs(score) + b_T

def scoreSimulationFinale(parking):
    evolParkings = np.zeros((N_ITERATIONS,LARGEUR_PARKING,LONGUEUR_PARKING))
    voitures = []
    parkingSim = deepcopy(parking)
    coordsPlacesAccess = placesBordsRoute(parking)
    tMoyGarage,tMoySortie = 0,0

    for k in range(N_ITERATIONS):
        if k%FREQ_APPARITION_VOITURES == 0:
            (iEntr,jEntr) = choice(list(COORDS_ENTREES))
            voitures.append([(iEntr,jEntr),False])
            
        for numVoiture in range(len(voitures)):
            if voitures[numVoiture]: # si la voiture n'est pas arrivée
                voitures[numVoiture], tMoyGarage, tMoySortie = nvVoiture(voitures[numVoiture],parkingSim,parking,coordsPlacesAccess,tMoyGarage,tMoySortie)
                
        evolParkings[k] = parkingSim
    affichageLoop(evolParkings)
    return COEFF_MISE_A_NIVEAU_SCORES_SIMFINALE/(tMoyGarage+tMoySortie)

def scoreSimulationAleatoire(parking):
    evolParkings = np.zeros((N_ITERATIONS,LARGEUR_PARKING,LONGUEUR_PARKING))

    voitures = []
    parkingSim = deepcopy(parking)
    tMoyGarage,tMoySortie = 0,0

    for k in range(N_ITERATIONS):
        if k%FREQ_APPARITION_VOITURES == 0:
            (iApparition, jApparition) = choice(list(COORDS_ENTREES))
            voitures.append([(iApparition,jApparition),False])
            
        for numVoiture in range(len(voitures)):
            if voitures[numVoiture]: # si la voiture n'est pas arrivée
                voitures[numVoiture], tMoyGarage, tMoySortie = nvVoitureRandom(voitures[numVoiture],parkingSim,parking,tMoyGarage,tMoySortie)
                
        evolParkings[k] = parkingSim

    affichageLoop(evolParkings)
    return COEFF_MISE_A_NIVEAU_SCORES_SIMALEA/(tMoyGarage+tMoySortie)

def score(parking,typeSimulation = ''):
    """
    Critère de notation d'un parking défini en 2 parties:
    Si parking n'est pas linéaire, on privilégie la taille de la route principale
    Sinon on lui associe un score selon une méthode donnée
    """
    coordsRoute = coordonneesRoutes(parking)

    entreePasDansRoute = coordsRoute == {}

    if entreePasDansRoute:
        return SCORE_MAUVAIS
    
    parkingLineaire = False
    for cheminRoute in coordsRoute:
        for (iSortie,jSortie) in COORDS_SORTIES:
            if (iSortie,jSortie) in coordsRoute[cheminRoute]:
                parkingLineaire = True
    
    if parkingLineaire:
        if typeSimulation == 'simFinale':
            return scoreSimulationFinale(parking)
        elif typeSimulation == 'simAlea':
            return scoreSimulationAleatoire(parking)
        else:
            return scoreNombrePlaces(parking)
    return scoreTailleRoute(parking,coordsRoute)

### Fonctions de croisement

def croisementAleatoire(P1,scoreP1,P2,scoreP2):
    """
    Fonction de croisement aléatoire. On crée un parking p3 et p4
    héritant respectivement de moitiés de P1 et P2 choisies aléatoirement
    """
    p3, p4 = deepcopy(P1), deepcopy(P2)
    iAleaChoisis = np.random.choice(LARGEUR_PARKING,size = LONGUEUR_PARKING*LARGEUR_PARKING//2, replace = False)
    jAleaChoisis = np.random.choice(LONGUEUR_PARKING,size = LONGUEUR_PARKING*LARGEUR_PARKING//2, replace = False)
    for i in range(LONGUEUR_PARKING*LARGEUR_PARKING//2):
        p3[iAleaChoisis,iAleaChoisis] = P2[iAleaChoisis,jAleaChoisis]
        p4[iAleaChoisis,iAleaChoisis] = P1[iAleaChoisis,jAleaChoisis]
    
    return [(P1,scoreP1),(P2,scoreP2),(p3,score(p3)),(p4,score(p4))]

def croisement2Coupage(P1,scoreP1,P2,scoreP2):
    """
    Fonction de croisement à un point de coupure. On crée un parking p3 et p4
    héritant respectivement d'une zone supérieure de P1 et P2
    """
    iCoupage,jCoupage = randint(0,LARGEUR_PARKING-1),randint(0,LONGUEUR_PARKING-1)
    p3, p4 = deepcopy(P1), deepcopy(P2)
    p3[:iCoupage,:jCoupage] = P1[:iCoupage,:jCoupage]
    p4[:iCoupage,:jCoupage] = P2[:iCoupage,:jCoupage]
    
    return [(P1,scoreP1),(P2,scoreP2),(p3,score(p3)),(p4,score(p4))]

def croisementRoutes(P1,scoreP1,P2,scoreP2):
    """
    Fonction de croisement où l'on crée un parking p3 et p4 héritant respectivement
    de la route principale de P1 et de P2
    """
    coordonneesRouteP1, coordonneesRouteP2 = coordonneesRoutes(P1), coordonneesRoutes(P2)
    p3, p4 = deepcopy(P1), deepcopy(P2)
    
    for (i,j) in coordonneesRouteP1:
        for (x,y) in coordonneesRouteP1[i,j]:
            p3[x,y] = NUM_ROUTE
    for (i,j) in coordonneesRouteP2:
        for (x,y) in coordonneesRouteP2[i,j]:
            p4[x,y] = NUM_ROUTE
        
    return [(P1,scoreP1),(P2,scoreP2),(p3,score(p3)),(p4,score(p4))]

### Fonctions de mutation

def mutationRandom(parking,probaMut):
    """
    Fonction de mutation aléatoire d'un parking, c'est-à-dire en modifiant
    aléatoirement chacune de ses composantes
    """
    for i in range(LARGEUR_PARKING):
        for j in range(LONGUEUR_PARKING):
            if (i,j) not in COORDS_ENTREES and (i,j) not in COORDS_SORTIES:
                if random()<probaMut:
                    parking[i,j] = [NUM_MUR,NUM_ROUTE,NUM_PLACE][randint(0,2)]

def mutationDeviation(parking):
    """
    Fonction de mutation d'un parking en modifiant une des trajectoires d'une
    de ses routes principales
    """
    coordsRoutes = coordonneesRoutes(parking)
    numRoutePrincipale = randint(0,len(coordsRoutes)-1)
    coordsRoute = np.array(list(coordsRoutes[COORDS_ENTREES[numRoutePrincipale]]))
    sensAllongement = ['haut','bas'][randint(0,1)]

    (iCoup1,jCoup1), (iCoup2,jCoup2) = coordonneesCoupage(parking,coordsRoute,sensAllongement)
    
    enleveRoute(parking,iCoup1,jCoup1,iCoup2,jCoup2,coordsRoute,sensAllongement)
    ajouteRoute(parking,iCoup1,jCoup1,iCoup2,jCoup2)
    return parking

def mutationAjoutBoutRoute(parking):
    """
    Fonction de mutation d'un parking en ajoutant un morceau de route sur une
    des extrémités d'une de ses routes principales puis en supprimant un bloc
    aléatoire de route s'il n'affecte pas sa linéarité.
    """
    coordsRoutes = coordonneesRoutes(parking)
    numRoutePrincipale = randint(0,len(coordsRoutes)-1)
    idRoutePrincipale = list(coordsRoutes)[numRoutePrincipale]
    coordsRoute = np.array(list(coordsRoutes[idRoutePrincipale]))
    nbBlocsRoute = len(coordsRoute) - 1
    
    (iAjout,jAjout) = coordsRoute[randint(0,nbBlocsRoute)]
    sensAjout = ['haut','bas','gauche','droite'][randint(0,3)]
    (iAjout,jAjout) = coordonneesFrontiere(iAjout,jAjout,parking,sensAjout,'ajout_morceau_route')

    if (iAjout,jAjout) not in COORDS_ENTREES and (iAjout,jAjout) not in COORDS_SORTIES:
        parking[iAjout,jAjout] = NUM_ROUTE
        
    ## On supprime un bloc random de route
    placesRouteParking = np.argwhere(parking == NUM_ROUTE)
    [iSuppr,jSuppr] = placesRouteParking[randint(0,placesRouteParking.shape[0]-1)]
    if neCassePas(iSuppr,jSuppr,parking):
        parking[iSuppr,jSuppr] = [NUM_MUR,NUM_PLACE][randint(0,1)]


if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")
