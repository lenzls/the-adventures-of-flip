'''
Created on 26.09.2010

@author: simon
'''
from util.events import Event

class MenuItem():
    def __init__(self, caption, eventType):
        self.caption = caption
        self.eventType = eventType
        
    def onClick(self):
        Event.raiseCstmEvent(self.eventType)

class TextItem(MenuItem):
    '''
        basic Text item (works like a button)
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