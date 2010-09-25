'''
Created on 25.09.2010

@author: simon
'''

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
        self.menuItems.append(TextItem("start game", "newGame"))
        

class MenuItem():
    def __init__(self, caption, action):
        self.caption = caption
        self.action = action

class TextItem(MenuItem):
    '''
        basic Text item (works like a button)
    '''
    def __init__(self, caption, action):
        MenuItem.__init__(self, caption, action)
    
class SwitchItem(MenuItem):
    '''
        item for switching stuff
        like sound on of
    '''
    def __init__(self, caption, action):
        MenuItem.__init__(self, caption, action)