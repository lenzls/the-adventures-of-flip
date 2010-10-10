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
    ACTIVATETRIGGER = 25
    NEWDIALOG = 26
    LEVELFINISHED = 27
    SWITCHLEVEL = 28
    SWITCHMENU = 29
    SWITCHSTATE = 30
    OPTIONSWITCH = 31

    def raiseCstmEvent(self, type, argDict={}):
        pygame.event.post(pygame.event.Event(type, argDict))
        