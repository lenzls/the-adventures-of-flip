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
        

class MenuItem():
    def __init__(self):
        pass

class TextItem(MenuItem):
    '''
        basic Text item (works like a button)
    '''
    def __init__(self, caption):
        MenuItem.__init__(self)
    
class SwitchItem(MenuItem):
    '''
        item for switching stuff
        like sound on of
    '''
    def __init__(self, caption):
        MenuItem.__init__(self)