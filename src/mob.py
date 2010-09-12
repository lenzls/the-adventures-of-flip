'''
Created on 10.07.2009

@author: CaptnLenz
'''

import xml.dom.minidom as dom

import util

class Mob(object):
    '''
    Baseclass for all mob's
    '''


    def __init__(self, map, infoTree, renderer, physics):
        '''
        Constructor
        '''        
        self.renderer = renderer
        self.physics = physics
        self.map = map
        self.alive = True
        
        self.jumplock = False
        
        self.position = util.Vector(0,0)
        self.dimensions = (0,0)
        
        self._loadInfo(infoTree)
        
        self.colShape = physics.ColShape(self)
        self.sprite = renderer.Sprite(self, renderer)
        
        #add rect
        #add ani
        
    def _loadInfo(self, datei):
        #position
        #animations
        pass
        #geschwindigkeiten
        
    def isAlive(self):
        return self.isAlive     

class Grob(Mob):
    def __init__(self, position, map, infoTree, renderer, physics):   #infoTree = xmlBaum
        Mob.__init__(self, map, infoTree, renderer, physics)