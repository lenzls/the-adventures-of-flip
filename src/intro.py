'''
Created on 09.07.2009

@author: CaptnLenz
'''
import pygame
from util import ressourceLoader

class Opening(object):

    def __init__(self):

        pygame.mixer.init()

        letterPlop = ressourceLoader.RessourceLoader.load_sound('letter-plop.wav')

    def play(self):
        pass
