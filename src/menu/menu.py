'''
Created on 25.09.2010

@author: simon
'''

from util.ressourceLoader import RessourceLoader
import util.constants as constants
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
    
    def getHeading(self):
        return self.heading

class MainMenu(Menu):
    
    def __init__(self):
        #TODO: works but i don't know why i cannot move this line to top of this file:/
        from menuManager import MenuManager

        Menu.__init__(self)
        self.background = RessourceLoader.load_graphic("menu_bg_gradient.png")
        self.menuItems = []
        self.heading = "Main menu"

        self.menuItems.append(menuItems.ButtonItem("> start game", Event.NEWGAME))
        self.menuItems.append(menuItems.ButtonItem("> switchToLevelMenu", Event.SWITCHMENU, argDict={'mIndex' : MenuManager.LEVELMENU}))
        self.menuItems.append(menuItems.ButtonItem("> switchToOptionsMenu", Event.SWITCHMENU, argDict={'mIndex' : MenuManager.OPTIONSMENU}))

        self.menuItems.append(menuItems.ButtonItem("> Quit Application", pygame.QUIT))
        self.curIndex = 0
        self.curItem = self.menuItems[self.curIndex]
        
class OptionsMenu(Menu):
    
    def __init__(self, stateManager):
        #TODO: see line 58
        from menuManager import MenuManager


        Menu.__init__(self)
        self.background = RessourceLoader.load_graphic("menu_bg_gradient.png")
        self.menuItems = []
        self.heading = "options menu"

        self.menuItems.append(menuItems.ButtonItem("> switchToMainMenu", Event.SWITCHMENU, argDict={'mIndex' : MenuManager.MAINMENU}))
        self.menuItems.append(menuItems.SwitchItem("> switchFullscreen: ", Event.OPTIONSWITCH, argDict={'option' : "ISFULLSCR"}))
        self.menuItems.append(menuItems.SwitchItem("> switchResolution: ", Event.OPTIONSWITCH, argDict={'option' : "RESOLUTION"}))
        self.menuItems.append(menuItems.SwitchItem("> switchVolume: ", Event.OPTIONSWITCH, argDict={'option' : "VOLUME"}))
        self.menuItems.append(menuItems.SwitchItem("> switchDebugMode: ", Event.OPTIONSWITCH, argDict={'option' : "ISDEBUG"}))
        self.menuItems.append(menuItems.ButtonItem("> Quit Application", pygame.QUIT))
        self.curIndex = 0
        self.curItem = self.menuItems[self.curIndex]
        
class LevelMenu(Menu):
    
    def __init__(self, stateManager):
        #TODO: see line 58
        from menuManager import MenuManager


        Menu.__init__(self)
        self.background = RessourceLoader.load_graphic("menu_bg_gradient.png")
        self.menuItems = []
        self.heading = "level menu"
        self.menuItems.append(menuItems.ButtonItem("> switchToMainMenu", Event.SWITCHMENU, argDict={'mIndex' : MenuManager.MAINMENU}))
        i = 0
        for level in stateManager.getGameState().levelManager.levelPathList:
            self.menuItems.append(menuItems.ButtonItem("> "+level, Event.SWITCHLEVEL, argDict={'levelIndex' : i}))
            i += 1
        self.menuItems.append(menuItems.ButtonItem("> Quit Application", pygame.QUIT))
        self.curIndex = 0
        self.curItem = self.menuItems[self.curIndex]
    