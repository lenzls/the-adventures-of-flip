'''
Created on 25.09.2010

@author: simon
'''

import menu.menuItems as menuItems
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
