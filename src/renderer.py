'''
Created on 07.07.2009

@author: CaptnLenz
'''

import pygame
import util
import constants

class RenderManager(object):
    '''
    classdocs
    '''

    def __init__(self, screen):
        '''
        Constructor
        '''
        self.screen = screen
        self.spriteList = []
        self.imageList = {} #list where all images stored(to avoid loading 2 times the same picture)
        self.camera = util.Vector(0,0)
        
    def createSprite(self, entity):
        sprite = Sprite(entity, self)
        self.appendSpriteList(sprite)
        return sprite
        
    def appendSpriteList(self, sprite):
        self.spriteList.append(sprite)
    
    def cleanSpriteList(self):
        ''' deletes the old spriteList and creates a new one (e.g.: 2 start a new level)''' 
        
        self.spriteList = []
        
    def update(self, level):
        self.updateCamera(level.player)
        self.updateSpriteList()
        self.updateBg(level.map)
        
    def updateSpriteList(self):
        ''' deletes dead entities from the spriteList'''
        self.spriteList = [sprite for sprite in self.spriteList if sprite.entity.getIsAlive()]
        
    def renderSprites(self):
        for sprite in self.spriteList:
            self.screen.blit(sprite.getCurFrameGraphic(), sprite.entity.position.getTuple())
    
    def renderMapLayer1(self, map):
        for y in range(max(self.camera[1] // constants.TILESIZE, 0), min(map.getDimensions()[1], (self.camera[1] + constants.RESOLUTION[1]) // constants.TILESIZE + 1)):
            for x in range(max(self.camera[0] // constants.TILESIZE, 0), min(map.getDimensions()[0], (self.camera[0] + constants.RESOLUTION[0]) // constants.TILESIZE + 1)):
                if map.getMapGrid()[0][x][y] != 0:
                    self.screen.blit(map.tiles[map.getMapGrid()[0][x][y]][2], (x*constants.TILESIZE - self.camera[0],y*constants.TILESIZE - self.camera[1]))
    
    def renderMapLayer2(self, map):
        for y in range(max(self.camera[1] // constants.TILESIZE, 0), min(map.getDimensions()[1], (self.camera[1] + constants.RESOLUTION[1]) // constants.TILESIZE + 1)):
            for x in range(max(self.camera[0] // constants.TILESIZE, 0), min(map.getDimensions()[0], (self.camera[0] + constants.RESOLUTION[0]) // constants.TILESIZE + 1)):
                if map.getMapGrid()[1][x][y] != 0:
                    self.screen.blit(map.tiles[map.getMapGrid()[1][x][y]][2], (x*constants.TILESIZE - self.camera[0],y*constants.TILESIZE - self.camera[1]))
    
    def renderBg(self, map):
        self.screen.fill((0,0,0));
        for bgLayer in map.bgLayers:
            self.screen.blit(bgLayer[1], (bgLayer[2] - self.camera[0], 0))
    
    def updateBg(self, map):
        '''update method for paralax scrolling'''
        pass
    
    def getCamera(self):
        return self.camera
    
    def updateCamera(self, playerInstance): #TODO:bad name
        '''
        
        @param playerInstance: instance of the current player object
        '''
        cameraOffset = util.Vector(0,0)
        
        #if (playerInstance.position[0] > (constants.RESOLUTION[0] - 100)) or (playerInstance.position[1] > (constants.RESOLUTION[1] - 100)):
        #    cameraOffset = util.Vector(playerInstance.position[0]-(constants.RESOLUTION[0] - 100),playerInstance.position[1]-(constants.RESOLUTION[1] - 100))
        #elif  (playerInstance.position[0] < (100)) or (playerInstance.position[1] < (100)):
        #    cameraOffset = util.Vector(100-playerInstance.position[0],100-playerInstance.position[1])
        if (playerInstance.position[0]-self.camera[0] > (constants.RESOLUTION[0] - 100)):
            print "rechts draussen", (playerInstance.position[0]-self.camera[0])-(constants.RESOLUTION[0] - 100), 0
            cameraOffset = util.Vector((playerInstance.position[0]-self.camera[0])-(constants.RESOLUTION[0] - 100), 0)
        #if (playerInstance.position[1]-self.camera[0] > (constants.RESOLUTION[1] - 100)):
        #    print "unten draussen", 0, (playerInstance.position[1]-self.camera[1])-(constants.RESOLUTION[1] - 100)
        #    cameraOffset = util.Vector(0, (playerInstance.position[1]-self.camera[1])-(constants.RESOLUTION[1] - 100))

            
            
        
        
        self.camera += cameraOffset
        print self.camera
     
class Sprite(object):
    '''respresents all sprites(animation(s)) of an entity '''
    
    def __init__(self, entity, renderer):
        self.entity = entity
        self.renderer = renderer
        
        self.spriteList = {}
        
        self.curFrame = 0
        self.curAni = None
        self.aniDelay = 3   #to switch less often(more realistic)
        self.aniDelayCounter = 0
        
    def addAnimation(self, aniType, graphicPaths):
        """ Add an animation to the animation list.
        
        This animation could be a single image or a sequence of images.
        graphicPaths: list of strings(Paths)"""
        
        self.spriteList[aniType] = []
        for graphicPath in graphicPaths:
            if not graphicPath in self.renderer.imageList:    #if the image doesn't exist in the imageDict, it gets added
                self.renderer.imageList[graphicPath] = util.load_image(graphicPath)
            self.spriteList[aniType].append(self.renderer.imageList[graphicPath])
    
    def setAni(self, aniType):
        self.curAni = self.spriteList[aniType]
        self.curFrame = 0
        
    def update(self):
        if self.aniDelayCounter < self.aniDelay:
            self.aniDelayCounter += 1
        else:
            if self.curFrame + 1 == len(self.curAni) :
                self.curFrame = 0
            else:
                self.curFrame += 1
            self.aniDelayCounter = 0
    
    def getCurFrameGraphic(self):
        return self.curAni[self.curFrame]
