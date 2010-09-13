'''
Created on 09.07.2009

@author: CaptnLenz
'''
import pygame
import util.util as util



class Opening(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pygame.mixer.init()

        letterPlop = util.load_sound('letter-plop.wav')
        
    def play(self):
        pass