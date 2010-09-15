'''
Created on 25.07.2009

@author: CaptnLenz
'''

import entities.mob as mob
from entities.player import Player
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

        self.map = map.Map(self.levelFilePath, self.renderer).getMapInstance()
        
        self.entities = []
        
        self._loadEntityFile(self.map.entityFilePath)
        

    def _loadEntityFile(self, entityFile):
        #durchsucht nur den "Entities"-teil der xml und gibt dann an die entity klasse den "entities-info" baum als parameter mit
        xmlEntityMap = dom.parse('../data/level/'+entityFile)
        entityInfoTrees = {}    #{name, infoTreeNode}
        for node in xmlEntityMap.firstChild.childNodes:
            if node.nodeName == 'entitiySpecification':
                for cNode in node.childNodes:
                    if cNode.nodeName == 'entitySpec':
                        entityInfoTrees[cNode.getAttribute('name')] = cNode
            elif node.nodeName == 'entities':
                for cNode in node.childNodes:
                    if cNode.nodeName == 'absEntity':
                        entityPos = [0,0]
                        for ccNode in cNode.childNodes:
                            if ccNode.nodeName == 'position':
                                for cccNode in ccNode.childNodes:
                                    if cccNode.nodeName == 'horizontal':
                                        entityPos[0] = int(cccNode.firstChild.data)
                                    elif cccNode.nodeName == 'vertical':
                                        entityPos[1] = int(cccNode.firstChild.data)
                        
                        if cNode.getAttribute('name') == 'player':
                            self.player = Player(entityPos, self.map, entityInfoTrees['player'], self.physics, self.renderer)
                            self.entities.append(self.player)
                        elif cNode.getAttribute('name') == 'grob':
                            self.entities.append(mob.Grob(entityPos, self.map, entityInfoTrees['grob'], self.physics, self.renderer))
        
    def updateEntities(self):
        for entity in self.entities:
            entity.update()
        