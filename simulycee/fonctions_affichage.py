"""
Programme secondaire répertoriant les fonctions d'affichage.
"""

from constantes import *

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

def affichage(tab):
    tab = np.array(tab,dtype=int)

    fig, ax = plt.subplots(figsize=(0.2*LARGEUR_PARKING, 0.2*LARGEUR_PARKING))

    image = plt.imshow(tab, vmin=-1, vmax=2)
    
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.set_cmap('BrBG') #gist_gray ou bone

    plt.show()

def affichageLoop(tab):
    fig, ax = plt.subplots(figsize=(0.2*LARGEUR_PARKING, 0.2*LARGEUR_PARKING))

    image = plt.imshow(tab[0], vmin=-1, vmax=2)
    ani = animation.FuncAnimation(fig, updateAni, frames = tab.shape[0], interval = int(1000*5/tab.shape[0]), fargs=(tab, image), repeat = True)

    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.set_cmap('BrBG') #gist_gray ou bone

    plt.show()

def updateAni(i, tab, image):
    
    image.set_data(tab[i])
    
    return True

def affichageEvolScore(scores):
    abscisses = np.arange(N_GENERATIONS)
    plt.plot(abscisses,scores)
    plt.title("EVOLUTION DU MEILLEUR SCORE")
    plt.xlabel('Nombre de générations')
    plt.ylabel('Meilleur score')
    plt.show()

def diagrammeDispersionScores(scores):
    scores = scores[scores!= SCORE_MAUVAIS]
    precision = abs(int(np.floor(np.log10(abs((np.max(scores) - np.min(scores))/100)))))
    
    '''
    for i in range(len(scores)):
        scores[i] = np.around(scores[i],precision)
    print('Scores:',scores)
    '''
    
    occurrences, scoresUniques = np.unique(scores, return_counts=True)
    
    plt.bar(occurrences,scoresUniques)
    plt.title("DISPERSION DES SCORES")
    plt.xlabel('Scores')
    plt.ylabel('Nombre d\'occurrences')
    plt.show()
    
    
if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")
    