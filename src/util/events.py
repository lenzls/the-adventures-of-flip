'''
Created on 26.09.2010

@author: simon
'''
import pygame

class Event(object):
    '''
    classdocs
    '''
    NEWGAME = 24

    def raiseNewGameEvent(self, argDict={}):
        pygame.event.post(pygame.event.Event(self.NEWGAME, argDict))
        