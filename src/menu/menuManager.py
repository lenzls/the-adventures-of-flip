'''
Created on 02.10.2010

@author: simon
'''
import menu

class MenuManager(object):
    MAINMENU = 0
    LEVELMENU = 1
    OPTIONSMENU = 2
    
    
    def __init__(self, stateManager):
        self.menuList = []
        self.menuList.append(menu.MainMenu())
        self.menuList.append(menu.LevelMenu(stateManager))
        self.menuList.append(menu.OptionsMenu(stateManager))

        self.curMenu = self.menuList[self.MAINMENU]
        
        self.stateManager = stateManager
        
    def loadMenu(self, menuIndex):
        self.curMenu = self.menuList[menuIndex]