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
    NEWTRIGGER = 25
    NEWDIALOG = 26
    LEVELFINISHED = 27

    def raiseNewGameEvent(self, argDict={}):
        pygame.event.post(pygame.event.Event(self.NEWGAME, argDict))
        
    def raiseCstmEvent(self, type, argDict={}):
        pygame.event.post(pygame.event.Event(type, argDict))
        