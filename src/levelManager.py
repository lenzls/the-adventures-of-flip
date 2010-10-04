'''
Created on 25.07.2009

@author: CaptnLenz
'''

import entities.mob as mob
import entities.item as item
from entities.player import Player
import map
import xml.dom.minidom as dom
from entities import trigger
from util.events import Event
import pygame

class LevelManager(object):
    
    FIRSTLEVEL = 0

    def __init__(self, physics, renderer):
        '''

        @param physics: current physicManager
        @param renderer: current renderManager
        '''
        self.physics = physics
        self.renderer = renderer
        self.levelPathList = []
        self.curLevelC = 0
        self.curLevel = None
        self._addLevelPath('1285970402.43.lxml')
        #self._addLevelPath('1286014149.83.lxml')
        self._addLevelPath('1284743568.37.lxml')

    def _addLevelPath(self, mapPath):
        self.levelPathList.append(mapPath)

    def loadLevel(self, levelIndex):
        self.curLevel = Level(self.physics, self.renderer, self.levelPathList[levelIndex])
        self.renderer.fades.renderFadeNewLvl(self.curLevel.map.getTitle())

    def next_lvl(self):
        if self.curLevelC+1 < len(self.levelPathList):
            self.curLevelC += 1
            self.loadLevel(self.curLevelC)
        else:
            #TODO: show screen | and move maybe to game class
            print "Game finished You Win!:)"
            #Event().raiseCstmEvent(pygame.QUIT, {})
            from game import StateManager
            Event().raiseCstmEvent(Event().SWITCHSTATE, {"state" : StateManager.MENUSTATE})

    def update(self):
        self.updateEntities()
        if self.curLevel.isFinished():
            self.next_lvl()

    def updateEntities(self):
        self.curLevel.updateEntities()

class Level(object):

    def __init__(self, physics, renderer, levelFilePath):
        self.physics = physics
        self.physics.reset()
        self.renderer = renderer
        self.renderer.reset()
        self.triggerManager = trigger.TriggerManager()
        self.levelFilePath = levelFilePath
        self.player = None
        self.finished = False

        self.map = map.Map(self.levelFilePath).getMapInstance()

        self.entities = []

        self.cutSceneState = False

        self._loadEntityFile(self.map.entityFilePath)
        
    def startCutScene(self):

        self.cutSceneState = True
        
    def endCutScene(self):
        self.cutSceneState = False

    def _loadEntityFile(self, entityFile):
        #durchsucht nur den "Entities"-teil der xml und gibt dann an die entity klasse den "entities-info" baum als parameter mit
        xmlEntityMap = dom.parse('../data/level/'+entityFile)
        entityInfoTrees = {}    #{name, infoTreeNode}
        for node in xmlEntityMap.firstChild.childNodes:
            if node.nodeName == 'entitiySpecification':
                for cNode in node.childNodes:
                    if cNode.nodeName == 'entitySpec':
                        entityInfoTrees[cNode.getAttribute('type')] = cNode
            elif node.nodeName == 'entities':
                for cNode in node.childNodes:
                    if cNode.nodeName == 'absEntity':
                        absEntObj = self.loadAbsEntity(cNode, entityInfoTrees, True)

                        if absEntObj.type == 'player':
                            self.player = absEntObj
                        self.entities.append(absEntObj)

    def loadAbsEntity(self, absNode, entityInfoTrees, activated):
        '''
            method reads an absEntity Node and returns the entityObj
            may be called from itself if a createEntity trigger occurs
            
            @return: entity obj
        '''
        entityPos = [0,0]
        for cNode in absNode.childNodes:
            if cNode.nodeName == 'position':
                for ccNode in cNode.childNodes:
                    if ccNode.nodeName == 'horizontal':
                        entityPos[0] = int(ccNode.firstChild.data)
                    elif ccNode.nodeName == 'vertical':
                        entityPos[1] = int(ccNode.firstChild.data)
            elif cNode.nodeName == 'msg':
                msg = cNode.firstChild.data
            elif cNode.nodeName == 'newEntity':
                newEntObj = self.loadAbsEntity(cNode, entityInfoTrees, False)

        #Player:
        if absNode.getAttribute('type') == 'player':
            return Player(entityPos, self.map, entityInfoTrees['player'], self.physics, self.renderer, activated)
        #Enemies:
        elif absNode.getAttribute('type') == 'grob':
            return mob.Grob(entityPos, self.map, entityInfoTrees['grob'], self.physics, self.renderer, activated)
        #Items:
        elif absNode.getAttribute('type') == 'coin':
            return item.Coin(entityPos, self.map, entityInfoTrees['coin'], self.physics, self.renderer, activated)
        #Trigger:
        elif absNode.getAttribute('type') == 't_moveLeft':
            return trigger.TmoveLeft(entityPos, self.map, entityInfoTrees['t_moveLeft'], self.physics, activated, {"player" : self.player})
        elif absNode.getAttribute('type') == 't_moveRight':
            return trigger.TmoveRight(entityPos, self.map, entityInfoTrees['t_moveRight'], self.physics, activated, {"player" : self.player})
        elif absNode.getAttribute('type') == 't_moveStop':
            return trigger.TmoveStop(entityPos, self.map, entityInfoTrees['t_moveStop'], self.physics, activated, {"player" : self.player})
        elif absNode.getAttribute('type') == 't_moveJump':
            return trigger.TmoveJump(entityPos, self.map, entityInfoTrees['t_moveJump'], self.physics, activated, {"player" : self.player})
        elif absNode.getAttribute('type') == 't_printer':
            return trigger.Tprinter(entityPos, self.map, entityInfoTrees['t_printer'], self.physics, activated, {"msg" : msg})
        elif absNode.getAttribute('type') == 't_createEntity':
            return trigger.TcreateEntity(entityPos, self.map, entityInfoTrees['t_createEntity'], self.physics, activated, {"newEntityObj" : newEntObj, "entityList" : self.entities})
        elif absNode.getAttribute('type') == 't_cutSceneStart':
            return trigger.TcutSceneStart(entityPos, self.map, entityInfoTrees['t_cutSceneStart'], self.physics, activated, {"level" : self})
        elif absNode.getAttribute('type') == 't_cutSceneEnd':
            return trigger.TcutSceneEnd(entityPos, self.map, entityInfoTrees['t_cutSceneEnd'], self.physics, activated, {"level" : self})
        elif absNode.getAttribute('type') == 't_createBubble':
            return trigger.TcreateBubble(entityPos, self.map, entityInfoTrees['t_createBubble'], self.physics, activated, {"msg" : msg})
        elif absNode.getAttribute('type') == 't_finishLvl':
            return trigger.TfinishLvl(entityPos, self.map, entityInfoTrees['t_finishLvl'], self.physics, activated, {})
        
    def updateEntities(self):
        for entity in self.entities:
            entity.update()
    
    def getPlayer(self):
        return self.player
    
    def setFinished(self):
        self.finished = True
        
    def isFinished(self):
        return self.finished
