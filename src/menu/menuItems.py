'''
Created on 26.09.2010

@author: simon
'''
from util.events import Event
import pygame

class MenuItem():
    def __init__(self, caption, eventType):
        self.caption = caption
        self.eventType = eventType
        
        self.color = [0,0,255]
        
    def onClick(self):
        Event().raiseCstmEvent(self.eventType)
        
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
    def __init__(self, caption):
        MenuItem.__init__(self, caption, pygame.NOEVENT)
        
class ButtonItem(MenuItem):
    '''
       (works like a button)
    '''
    def __init__(self, caption, eventType):
        MenuItem.__init__(self, caption, eventType)
    
class SwitchItem(MenuItem):
    '''
        item for switching stuff
        like sound on of
    '''
    def __init__(self, caption, eventType):
        MenuItem.__init__(self, caption, eventType)