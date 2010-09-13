'''
Created on 25.07.2009

@author: CaptnLenz
'''

import entities.mob as mob
import entities.player as player
import map
import xml.dom.minidom as dom


class LevelManager(object):
    def __init__(self, physics, renderer):
        '''
        
        @param physics: current physicManager
        @param renderer: current renderManager
        '''
        self.physics = physics
        self.renderer = renderer
        self.levelPathList = []
        self.curLevel = None
        self._addLevelPath('newspec.lxml')
        
    def _addLevelPath(self, mapPath):       #to the levelList
        self.levelPathList.append(mapPath)
        
    def loadLevel(self, levelIndex):
        self.curLevel = Level(self.physics, self.renderer, self.levelPathList[levelIndex])
        
    def update(self):
        self.updateEntities()
    
    def updateEntities(self):
        self.curLevel.updateEntities()
    
class Level(object):
    '''
    classdocs
    '''


    def __init__(self, physics, renderer, levelFilePath):
        '''
        Constructor
        '''
        self.physics = physics
        self.renderer = renderer
        self.levelFilePath = levelFilePath
        self.player = None

        self.map = map.Map(self.levelFilePath).getMapInstance()
        
        self.entities = []
        
        self._loadEntityFile(self.map.entityFilePath)
        
        
        
    
    def _loadEntityFile(self, entityFile):
        #durchsucht nur den "Entities"-teil der xml und gibt dann an die entity klasse den "entities-info" baum als parameter mit
        xmlEntityMap = dom.parse('../data/level/'+entityFile)
        entityInfoTrees = {}
        for node in xmlEntityMap.firstChild.childNodes:
            if node.nodeName == 'EntitiesInfo':
                for childNode in node.childNodes:
                    if childNode.nodeName == 'Entity':
                        entityInfoTrees[childNode.getAttribute('name')] = childNode
            elif node.nodeName == 'Entities':
                for childNode in node.childNodes:
                    if childNode.nodeName == 'absEntity':
                        
                        entityPos = [0,0]
                        for childChildNode in childNode.childNodes:
                            if childChildNode.nodeName == 'position':
                                for childChildChildNode in childChildNode.childNodes:
                                    if childChildChildNode.nodeName == 'horizontal':
                                        entityPos[0] = int(childChildChildNode.firstChild.data)
                                    elif childChildChildNode.nodeName == 'vertical':
                                        entityPos[1] = int(childChildChildNode.firstChild.data)
                        
                        if childNode.getAttribute('name') == 'player':
                            self.player = player.Player(entityPos, self.map, entityInfoTrees['player'], self.physics, self.renderer)
                            self.entities.append(self.player)
                        elif childNode.getAttribute('name') == 'grob':
                            self.entities.append(mob.Grob(entityPos, self.map, entityInfoTrees['grob'], self.physics, self.renderer))
        
    def updateEntities(self):
        for entity in self.entities:
            entity.update()
        