'''
Created on 25.09.2010

@author: simon
'''

from util.ressourceLoader import RessourceLoader
import menuItems as menuItems
from util.events import Event
import pygame

class Menu(object):
    '''
    classdocs
    '''


    def moveDown(self):
        try:
            self.curItem.markUnSelected()
            self.curIndex += 1
            self.curItem = self.menuItems[self.curIndex]
        except:
            self.curIndex = 0
            self.curItem = self.menuItems[self.curIndex]

    def moveUp(self):
        # no try/except because listIndex -1 is a valid one! 
        if self.curIndex > 0:
            self.curItem.markUnSelected()
            self.curIndex -= 1
            self.curItem = self.menuItems[self.curIndex]
        else:
            self.curItem.markUnSelected()
            self.curIndex = len(self.menuItems)-1
            self.curItem = self.menuItems[self.curIndex]
    
    def update(self):
        self.curItem.markSelected()

    def execute(self):
        self.menuItems[self.curIndex].onClick()
        
    def getBackground(self):
        return self.background
    
    def getMenuItems(self):
        return self.menuItems

class MainMenu(Menu):
    
    def __init__(self):
        Menu.__init__(self)
        self.background = RessourceLoader().load_graphic("menu_bg_mainMenu.png")
        self.menuItems = []
        self.menuItems.append(menuItems.TextItem("main menu"))
        self.menuItems.append(menuItems.ButtonItem("> start game", Event.NEWGAME))
        self.menuItems.append(menuItems.ButtonItem("> Quit Application", pygame.QUIT))
        self.curIndex = 0
        self.curItem = self.menuItems[self.curIndex]
    