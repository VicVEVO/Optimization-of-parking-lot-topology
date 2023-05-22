import numpy as np
from random import randint, random
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import time,copy

### CONSTANTES #########################################################

I_TYPE_CASE = 0
N_ITERATIONS = 40
DUREE_GARAGE = 5 #s/iterations
PROBA_MUTATION = 0.02
longueur_parking = 10
largeur_parking = 10
I_SORTIE,J_SORTIE = largeur_parking//2,longueur_parking-1
N_parkings = 10
N_generations = 500

### FONCTIONS GENERALES ################################################

def parking_cool_test(longueur,largeur):
    
    bords = -np.ones(longueur,dtype=int)

    parking = -np.ones((largeur,longueur),dtype=int)
    
    for x in range(3,longueur-1):
        if x%4 == 1 or x%4 == 2:
            for y in range(2,largeur-2):
                parking[y,x] = 1
        else:
            parking[:,x] = 0 # files vides

    parking[largeur//2],parking[largeur//2-1] = 0,0 # création de la route principale 
    parking[0,3:-1],parking[1,3:-1],parking[-1,3:-1],parking[-2,3:-1] = 0,0,0,0 # création des routes des fins de files

    parking = np.append(bords,parking).reshape(largeur+1,longueur)
    parking = np.append(parking,bords).reshape(largeur+2,longueur)

    T = np.array([True]*longueur*(largeur+2)).reshape(largeur+2,longueur)

    return np.array([parking,T,T,T,T])

def creation_random_parking(longueur_parking,largeur_parking):
    """Crée un parking aléatoirement.

    Parameters
    ----------
    longueur_parking: int
    largeur_parking: int

    Returns
    -------
    array
        tableau numpy LxN composé de quintuplets [genre,dir1,dir2,dir3,dir4]
        genre: int
            entier décrivant la nature du bloc pouvant valoir -1 (mur), 0 (route) ou 1 (place)
        dir1 (resp. dir2, ..): bool
            booléen vrai si la voiture peut avancer devant (resp. à gauche,..) par rapport à l'entrée. [cf fichier paint]

        parking = | [0,True,True,False,False] , ... , [-1,True,True,False,True] |

        Correspondant à :

                    | [0,True,True,False,False]             ...             [-1,True,True,False,True] |
                    |            ...                                                   ...            |
                    |            ...                                                   ...            |
        parking =   |            ...                                                   ...            |
                    |            ...                                                   ...            |
                    |            ...                                                   ...            |
                    | [-1,True,False,True,True]             ...             [-1,True,True,False,True] |

    """

    P = []
    for _ in range(largeur_parking):
        for __ in range(longueur_parking):
            P.append([randint(-1,1),[True,False][randint(0,1)],[True,False][randint(0,1)],[True,False][randint(0,1)],[True,False][randint(0,1)]])
    
    P[longueur_parking*(largeur_parking//2)][0] = 0 # on impose que l'entrée ne soit pas condamnée
    P[longueur_parking*(largeur_parking//2+1)-1][0] = 0 # de même pour la sortie
    
    P = np.array(P,dtype=list)
    parking = np.empty(5,dtype=list)
    for i in range(5):
        parking[i] = P[:,i].reshape((largeur_parking,longueur_parking))

    return parking

def dijkstra(parking, i1, j1, i2, j2):
    """
    Algorithme cherchant avec la méthode de Dijkstra un chemin liant deux points (i1,j1) et (i2,j2) dans arr
    Parameters
    ----------
    parking: array
    i1: int
    j1: int
    i2: int
    j2: int

    Returns
    -------
    array
        liste des coordonnées successives des points du chemin liant (i1,j1) et (i2,j2).
    """
    taille_parking = parking[0].shape # (nb_lignes,nb_colonnes)
    indices_visités = np.full(taille_parking, False)
    queue = [(i1, j1)] # queue pour garder les indices que l'on doit visiter
    ind_precedents = {} # dico pour garder les indices précédemment étudiés pour chaque indice
    indices_visités[i1, j1] = True

    while queue: # tant qu'il y a des indices à étudier
        i, j = queue.pop(0) # on prend le prochain indice dans la queue
        if i == i2 and j == j2: # si l'indice actuel est arrivé sur l'indice de destination on arrête le programme
            break

        voisinage = [(i, j+1), (i-1, j), (i, j-1), (i+1, j)] # devant, gauche, derrière, droite

        for num_voisin in range(len(voisinage)):

            i_vois, j_vois = voisinage[num_voisin]

            if 0 <= i_vois < taille_parking[0] and 0 <= j_vois < taille_parking[1] and not indices_visités[i_vois, j_vois]: # si la case est pas visitée est qu'il n'y a pas de OOB
                accessible = parking[num_voisin+1][i,j] # booléen vrai si la case (i_vois,j_vois) est accessible depuis (i,j)
                if accessible and parking[0][i_vois,j_vois] == 0: # si la case est accessible physiquement et que c'est de la route
                    indices_visités[i_vois, j_vois] = True # le voisin est désormais visité
                    queue.append((i_vois, j_vois)) # on l'ajoute parmi les prochains a devoir être visité

                    ind_precedents[(i_vois, j_vois)] = (i, j) # on garde les indices précédents pour i_vois,j_vois
                accessible = False

    chemin = []

    i, j = i2, j2 # on part de l'arrivée
    while (i, j) in ind_precedents:
        chemin.append((i, j))
        i, j = ind_precedents[(i, j)]

    return list(reversed(chemin))

def directions_dispo(i,j,direction,parking):
    devant_dispo = parking[1][i,j] # /!\ ce n'est pas devant elle mais devant par rapport à l'entrée
    gauche_dispo = parking[2][i,j]
    droite_dispo = parking[3][i,j]
    derriere_dispo = parking[4][i,j]
    
    candidats_dir_dispo = []
    for A in [[devant_dispo,i,j+1],[gauche_dispo,i-1,j],[droite_dispo,i+1,j],[derriere_dispo,i,j-1]]:
        if 0<=A[1]<parking[0].shape[0] and 0<=A[2]<parking[0].shape[1]: # si les coordonnées ne sont pas hors limite
            candidats_dir_dispo.append(A)
    return candidats_dir_dispo            

def etapes_sortie(parking):
    '''
    Fonction renvoyant un dictionnaire avec pour chaque place le chemin à parcourir pour sortir du parking
    '''
    chemins = {}
    coordonnees_places = np.argwhere(parking[0]==1)
    for i_place,j_place in coordonnees_places:
        chemins[(i_place,j_place)] = dijkstra(parking,i_place,j_place,I_SORTIE,J_SORTIE)
    return chemins
    
def simulation(parking):
    """
    Simule les tutures
    """
    chemins_sortie = etapes_sortie(parking)
    voitures = [[[largeur_parking//2,0],1,False]] # [(i,j), direction, est_garee]
    parking_ref = copy.deepcopy(parking)
    Ntot_voitures = N_ITERATIONS//3 + 1 # nb total de voitures qui apparaîtront
    T_moy_garage , T_moy_sortie = 0 , 0
    
    for i in range(N_ITERATIONS):
        #tab[i] = parking[0] # pour afficher en loop
        if i%3==0 and i != 0: # apparition d'une nouvelle voiture
            voitures.append([[largeur_parking//2,0],1,False])

        for num_voiture in range(len(voitures)):
            voiture = voitures[num_voiture]

            if voiture: # si la voiture n'est pas arrivée
                [i,j] = voiture[0]

                if not voiture[2]: # si la voiture n'est pas garée
                    direction = voiture[1]

                    parking[0][voiture[0][0],voiture[0][1]] = np.copy(parking_ref[0])[voiture[0][0],voiture[0][1]]

                    candidats_dir_dispo = directions_dispo(i,j,direction,parking)
                    direction_opposee = direction + 2
                    if direction_opposee > 4:
                        direction_opposee %= 4

                    dir_dispo , dir_place = [] , []

                    for num_dir in range(len(candidats_dir_dispo)): # on teste chaque direction autour de la voiture
                        if num_dir != direction_opposee:
                            i_dir,j_dir = candidats_dir_dispo[num_dir][1],candidats_dir_dispo[num_dir][2]
                            
                            if candidats_dir_dispo[num_dir][0] and 0 <= parking[0][i_dir,j_dir] <= 1: # si la case est accessible règlementairement et physiquement
                                if parking[0][i_dir,j_dir] == 1: # si c'est une place
                                    dir_place.append([candidats_dir_dispo[num_dir][1],candidats_dir_dispo[num_dir][2],num_dir+1])
                                else: # si c'est de la route
                                    dir_dispo.append([candidats_dir_dispo[num_dir][1],candidats_dir_dispo[num_dir][2],num_dir+1])
                    
                    if dir_place != []: # la voiture va en priorité à la place s'il y en a une
                        voiture = [[dir_place[0][0],dir_place[0][1]],dir_place[0][2],True]
                    elif dir_dispo != []: # sinon elle avance aléatoirement là où elle peut
                        choix_alea = randint(0,len(dir_dispo)-1)
                        voiture = [[dir_dispo[choix_alea][0],dir_dispo[choix_alea][1]],dir_dispo[choix_alea][2],False]

                    T_moy_garage += 1/Ntot_voitures
                    parking[0] = copy.deepcopy(parking[0]) # éviter aliasing et changer valeur parking_ref
                    parking[0][voiture[0][0],voiture[0][1]] = 2

                else: # si la voiture est garée, elle suit un chemin prédéfini pour sortir
                    if len(voiture) == 3: # si la voiture vient juste de se garer
                        chemin_sortie = chemins_sortie[i,j] # (i,j) et voiture (j,i)
                        voiture.append(chemin_sortie)
                        voiture.append(-DUREE_GARAGE)
                    
                    T_moy_sortie += 1/Ntot_voitures
                    if voiture[4] != len(voiture[3]): # si la voiture n'est pas arrivée
                        if voiture[4] > 0: # si la voiture veut partir et qu'il n'y a pas d'autre voiture sur la case
                            [i_nv,j_nv] = voiture[3][voiture[4]]

                            if parking[0][i_nv,j_nv] != 2:
                                parking[0][voiture[0][0],voiture[0][1]] = np.copy(parking_ref[0])[voiture[0][0],voiture[0][1]]
                                voiture[0] = [i_nv,j_nv] # on change les coordonnées de la voiture
                                parking[0] = copy.deepcopy(parking[0])
                                parking[0][voiture[0][0],voiture[0][1]] = 2

                        voiture[4] += 1 # l'indice_etape_sortie augmente de 1

                    else: # si la voiture est arrivée devant la sortie
                        parking[0][i,j] = np.copy(parking_ref[0])[i,j]
                        voiture = [] # il faut trouver un moyen de vanish les tutures
                    
            voitures[num_voiture] = voiture

    if T_moy_sortie == 0:
        T_moy_sortie = 100000
    
    return T_moy_garage,T_moy_sortie,parking_ref

def score(parking):
    """
    Renvoie le score du parking.
    Ce score est basé sur:
    - la durée moyenne de processus de garage
    - la durée moyenne de sortie du parking
    - le nombre de murs (il faut des arbres)       # À réfléchir...
    - le nombre de places

    PB: cv trop lentement, parking full places trop favorisés

    Parameters
    ----------
    parking: array     # on suppose que le parking n'est plus une array linéaire mais rectangulaire

    Returns
    -------
    score: float
        Note positive = 1/(3*t_moy_garage) + 1/(3*t_moy_sortie) + nb_murs/12 + 3*nb_places/12
        Plus la note est faible, meilleur est le parking.
    parking_ref: array
        On renvoie aussi la configuration du parking vide
    """

    nb_murs, nb_places = np.count_nonzero(parking[0]==-1),np.count_nonzero(parking[0]==1)
    t_moy_garage,t_moy_sortie,parking_ref = simulation(parking)
    return t_moy_garage + t_moy_sortie - nb_murs/50 - nb_places , parking_ref

def selection(liste_parkings,nb_parkings):
    """
    Sélectionne la moitié des meilleurs parkings selon leur score
    """
    resultats = []

    for num_parking in range(nb_parkings):
        score_parking , parking = score(liste_parkings[num_parking])
        resultats.append([score_parking,parking])

    resultats = np.array(resultats,dtype=object)
    resultats = resultats[resultats[:,0].astype(int).argsort()]

    premiers_meilleurs = [resultats[i][1] for i in range(nb_parkings//2)] # on garde la moitié des meilleurs parkings
    
    return premiers_meilleurs

def croisement(liste_parkings,nb_parkings):
    """
    Procédure croisant les chromosomes des parkings
    Regroupés par couples, chaque paire de parkings sélectionnés croisent leur chromosomes pour donner 2 enfants
    On fait le beau découpage proposé par Mr Poirier le boss
    """
    for i in range(0,nb_parkings//2,2):
        parent1 , parent2 = liste_parkings[i] , liste_parkings[i+1]
        i_coupage,j_coupage = randint(0,longueur_parking-1),randint(0,largeur_parking-1)
        
        #enfant1 = np.array([np.concatenate((parent1[k][:largeur_parking//2],parent2[k][largeur_parking//2:])) for k in range(5)])
        #enfant2 = np.array([np.concatenate((parent2[k][:largeur_parking//2],parent1[k][largeur_parking//2:])) for k in range(5)])
        enfant1 , enfant2 = np.copy(parent1) , np.copy(parent2)

        for k in range(5):
            enfant1[k][:i_coupage,:j_coupage] = parent2[k][:i_coupage,:j_coupage]
            enfant2[k][:i_coupage,:j_coupage] = parent1[k][:i_coupage,:j_coupage]
        
        liste_parkings.append(enfant1)
        liste_parkings.append(enfant2)
    
def mutation(liste_parkings):
    """
    De façon aléatoire, chaque parking a pour chaque chromosome une toute petite probabilité d'avoir un gène qui mute aléatoirement
    """
    for parking in liste_parkings:
        for i in range(len(parking[0][:,0])):
            for j in range(len(parking[0][0])):
                if (i,j) != (largeur_parking//2,0) and (i,j) != (largeur_parking//2,longueur_parking-1):
                    num_gene = randint(0,4) # on choisit aléatoirement un gène
                    if random()<PROBA_MUTATION:
                        if num_gene == 0:
                            parking[I_TYPE_CASE][i,j] = randint(-1,1)
                        else:
                            parking[num_gene][i,j] = not(parking[num_gene][i,j])

def evolution(N_parkings,N_generations):
    '''
    Algorithme génétique pour une population de N parking.
    '''
    tab = np.zeros((N_generations,largeur_parking,longueur_parking))

    pop_parkings = [creation_random_parking(longueur_parking,largeur_parking) for _ in range(N_parkings)] # population initiale: on crée N parkings (durée: 0.06s)

    for _ in range(N_generations):
        pop_parkings = selection(pop_parkings,N_parkings)
        croisement(pop_parkings,N_parkings)
        mutation(pop_parkings)
        tab[_] = pop_parkings[0][0] # affichage de l'évolution
    
    meilleur_parking = pop_parkings[0]
    affichage_loop(tab)

    return meilleur_parking

### FONCTION D'AFFICHAGE ###############################################

def affichage(tab):

    tab = tab[0] # on ne prend que les premiers indices pour l'afficher
    tab = np.array(tab,dtype=int)

    # Initialisation fenetre
    fig, ax = plt.subplots(figsize=(0.2*longueur_parking, 0.2*largeur_parking))

    # Dessin du tableau
    image = plt.imshow(tab, vmin=-1, vmax=2)
    
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.set_cmap('BrBG') #gist_gray ou bone

    plt.show()

def affichage_loop(tab):
    # Initialisation fenetre
    fig, ax = plt.subplots(figsize=(0.2*longueur_parking, 0.2*largeur_parking))

    # Dessin du tableau
    image = plt.imshow(tab[0], vmin=-1, vmax=2)
    # Animation
    ani = animation.FuncAnimation(fig, update_ani, frames = tab.shape[0], interval = int(1000*5/tab.shape[0]), fargs=(tab, image), repeat = True)

    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.set_cmap('BrBG') #gist_gray ou bone

    plt.show()

def update_ani(i, tab, image):

    image.set_data(tab[i]) #Mise à jour de l'image
    
    return True

### PROGRAMME PRINCIPAL ################################################

parking_final = evolution(N_parkings,N_generations)

'''
P = parking_cool_test(longueur_parking,largeur_parking-2)

tab = np.zeros((N_ITERATIONS,largeur_parking,longueur_parking))

simulation(P,np.copy(P))

affichage_loop(tab)
'''
