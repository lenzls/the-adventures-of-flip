'''
Created on 25.09.2010

@author: simon
'''

import menuItems as menuItems
from util.events import Event

class Menu(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

class MainMenu(Menu):
    
    def __init__(self):
        Menu.__init__(self)
        
        self.menuItems = []
        self.menuItems.append(menuItems.TextItem("start game", Event.NEWGAME))
        self.menuItems.append(menuItems.TextItem("asd game", Event.NEWGAME))
        self.curIndex = 0
        self.curItem = self.menuItems[self.curIndex]
        
    def moveDown(self):
        try:
            self.curIndex += 1
            self.curItem = self.menuItems[self.curIndex]
        except:
            self.curIndex = 0
            self.curItem = self.menuItems[self.curIndex]

    def moveUp(self):
        # no try/except because listIndex -1 is a valid one! 
        if self.curIndex > 0:
            self.curIndex -= 1
            self.curItem = self.menuItems[self.curIndex]
        else:
            self.curIndex = len(self.menuItems)-1
            self.curItem = self.menuItems[self.curIndex]

    def select(self):
        self.menuItems[self.curIndex].onClick()