"""
Programme secondaire répertoriant les fonctions d'affichage.
"""

from constantes import *

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

def affichage(tab):
    # on ne prend que les premiers indices pour l'afficher
    tab = np.array(tab,dtype=int)

    # Initialisation fenetre
    fig, ax = plt.subplots(figsize=(0.2*LARGEUR_PARKING, 0.2*LARGEUR_PARKING))

    # Dessin du tableau
    image = plt.imshow(tab, vmin=-1, vmax=2)
    
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.set_cmap('BrBG') #gist_gray ou bone

    plt.show()

def affichageLoop(tab):
    # Initialisation fenetre
    fig, ax = plt.subplots(figsize=(0.2*LARGEUR_PARKING, 0.2*LARGEUR_PARKING))

    # Dessin du tableau
    image = plt.imshow(tab[0], vmin=-1, vmax=2)
    # Animation
    ani = animation.FuncAnimation(fig, updateAni, frames = tab.shape[0], interval = int(1000*5/tab.shape[0]), fargs=(tab, image), repeat = True)

    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.set_cmap('BrBG') #gist_gray ou bone

    plt.show()

def updateAni(i, tab, image):

    image.set_data(tab[i]) #Mise à jour de l'image
    
    return True

if __name__ == '__main__':
    print("Ce programme n'est pas destiné à être lancé.")
    