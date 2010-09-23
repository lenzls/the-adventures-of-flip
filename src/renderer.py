'''
Created on 07.07.2009

@author: CaptnLenz
'''

from util.vector import Vector
from util.dataStorage.rendering import Sprite
import util.constants as constants
import pygame

class RenderManager(object):

    def __init__(self, screen):
        self.screen = screen
        self.spriteList = []
        self.camera = Vector(0,0)

    def createSprite(self, entity):
        sprite = Sprite(entity)
        self.appendSpriteList(sprite)
        return sprite

    def appendSpriteList(self, sprite):
        self.spriteList.append(sprite)

    def cleanSpriteList(self):
        ''' deletes the old spriteList and creates a new one (e.g.: to start a new level)''' 

        self.spriteList = []

    def update(self, level):
        self.updateCamera(level.player)
        self.updateSpriteList()
        self.updateBg(level)

    def updateSpriteList(self):
        ''' deletes dead entities from the spriteList'''
        self.spriteList = [sprite for sprite in self.spriteList if sprite.entity.isAlive()]
        for sprite in self.spriteList:
            sprite.update()

    def renderSprites(self):
        for sprite in self.spriteList:
            self.screen.blit(sprite.getCurFrame().getGraphic(), (sprite.entity.getPosition() - self.camera).getTuple())

    def renderMapLayer(self, layerIndex, map):
        ''' renders map Layer
            @param layerIndex: 0 => Layer1
                             : 1 => Layer2
        '''
        for y in range(max(self.camera[1] // constants.TILESIZE, 0), 
                       min(map.getDimensions()[1], (self.camera[1] + constants.RESOLUTION[1]) // constants.TILESIZE + 1)):
            for x in range(max(self.camera[0] // constants.TILESIZE, 0), 
                           min(map.getDimensions()[0], (self.camera[0] + constants.RESOLUTION[0]) // constants.TILESIZE + 1)):
                if map.getMapGrid()[layerIndex][x][y] != 0:
                    self.screen.blit(map.getTileGraphic(layerIndex,x,y), (x*constants.TILESIZE - self.camera[0],y*constants.TILESIZE - self.camera[1]))

    def renderBg(self, map):
        self.screen.fill((0,0,0));
        for bgLayer in map.bgLayers.values():

            # scrolling offset
            self.screen.blit(bgLayer.getGraphic(), 
                             (0, ((map.getDimensions()[1]*constants.TILESIZE) - bgLayer.getDimensions()[1]) - self.camera[1]), 
                             area=pygame.Rect(bgLayer.getDimensions()[0]-bgLayer.getScrollPosition()[0],0,bgLayer.getDimensions()[0],bgLayer.getDimensions()[1]))

            for i in range(bgLayer.getNeededGraphics()):
                self.screen.blit(bgLayer.getGraphic(), 
                             (bgLayer.getScrollPosition()[0] + i*bgLayer.getDimensions()[0], ((map.getDimensions()[1]*constants.TILESIZE) - bgLayer.getDimensions()[1]) - self.camera[1]), 
                             area=pygame.Rect(0,0,bgLayer.getDimensions()[0],bgLayer.getDimensions()[1]))

    def updateBg(self, level):
        '''update method for paralax scrolling'''

        for bgLayer in level.map.bgLayers.values():
            bgLayer.update(level.player.getPosition())

    def getCamera(self):
        return self.camera

    def updateCamera(self, playerInstance): #TODO:bad name
        '''
        @param playerInstance: instance of the current player object
        '''

        cameraOffset = Vector(0,0)

        horiBorder = constants.RESOLUTION[0] // 5
        vertiBorder = constants.RESOLUTION[1] // 5

        playerPos = playerInstance.getPosition()

        if (playerPos[0] - self.camera[0]) > (constants.RESOLUTION[0] - horiBorder):
            cameraOffset +=  Vector((playerPos[0] - self.camera[0]) - (constants.RESOLUTION[0] - horiBorder),cameraOffset[1])
        elif (playerPos[0] - self.camera[0]) < (horiBorder):
            cameraOffset -=  Vector((horiBorder) - (playerPos[0] - self.camera[0]),cameraOffset[1])

        if (playerPos[1] - self.camera[1]) < (vertiBorder):
            cameraOffset -=  Vector(cameraOffset[0],(horiBorder) - (playerPos[1] - self.camera[1]))
        elif (playerPos[1] - self.camera[1]) > (constants.RESOLUTION[1] - vertiBorder):
            cameraOffset +=  Vector(cameraOffset[0],(playerPos[1] - self.camera[1]) - (constants.RESOLUTION[1] - vertiBorder))
        self.camera += cameraOffset

        if playerPos[0] < horiBorder:
            self.camera = Vector(0, self.camera[1])
        elif playerPos[0] > playerInstance.map.getDimensions()[0]*constants.TILESIZE-horiBorder:
            self.camera = Vector(playerInstance.map.getDimensions()[0]*constants.TILESIZE-constants.RESOLUTION[0], self.camera[1])

        if playerPos[1] < vertiBorder:
            self.camera = Vector(self.camera[0], 0)
        elif playerPos[1] > playerInstance.map.getDimensions()[1]*constants.TILESIZE-vertiBorder:
            self.camera = Vector(self.camera[0], playerInstance.map.getDimensions()[1]*constants.TILESIZE-constants.RESOLUTION[1])

    def checkGraphicSizes(self):
        for sprite in self.spriteList:
            sprite.checkimageSizes()
