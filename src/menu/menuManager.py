'''
Created on 02.10.2010

@author: simon
'''
import menu

class MenuManager(object):
    MAINMENU = 0
    TESTMENU = 1
    
    
    def __init__(self):
        self.menuList = []
        self.menuList.append(menu.MainMenu())
        self.menuList.append(menu.TestMenu())

        self.curMenu = self.menuList[self.MAINMENU]
        
    def loadMenu(self, menuIndex):
        self.curMenu = self.menuList[menuIndex]