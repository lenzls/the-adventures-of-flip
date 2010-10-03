'''
Created on 26.09.2010

@author: simon
'''
from util.events import Event
import pygame

class MenuItem():
    def __init__(self, caption, eventType, argDict={}):
        self.caption = caption
        self.eventType = eventType
        self.eventArgs = argDict
       
        self.color = [0,0,255]
        
    def onClick(self):
        Event().raiseCstmEvent(self.eventType, argDict=self.eventArgs)
        
    def markSelected(self):
        self.color = [255,0,0]
        
    def markUnSelected(self):
        self.color = [0,0,255]
        
    def getColor(self):
        return self.color
    
    def getCaption(self):
        return self.caption

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