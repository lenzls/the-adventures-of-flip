'''
Created on 26.09.2010

@author: simon
'''
from util.events import Event
import pygame
from util.options import Options

class MenuItem():
    def __init__(self, caption, eventType, argDict={}):
        self.caption = caption
        self.eventType = eventType
        self.eventArgs = argDict
       
        self.color = []
        self.select = False
        self.markUnSelected()
        
    def onClick(self):
        Event().raiseCstmEvent(self.eventType, argDict=self.eventArgs)
        
    def markSelected(self):
        self.select = True
        
    def markUnSelected(self):
        self.select = False

    def getCaption(self):
        return self.caption
    
    def getSelect(self):
        return self.select

class TextItem(MenuItem):
    '''
        basic Text item
    '''
    def __init__(self, caption, argDict={}):
        MenuItem.__init__(self, caption, pygame.NOEVENT, argDict=argDict)
        
class ButtonItem(MenuItem):
    '''
       (works like a button)
    '''
    def __init__(self, caption, eventType, argDict={}):
        MenuItem.__init__(self, caption, eventType, argDict=argDict)
    
class SwitchItem(MenuItem):
    '''
        item for switching stuff
        like sound on of
    '''
    def __init__(self, caption, eventType, argDict={}):
        MenuItem.__init__(self, caption, eventType, argDict=argDict)

    def getCaption(self):
        return self.caption + str(Options.getOption(self.eventArgs["option"]))