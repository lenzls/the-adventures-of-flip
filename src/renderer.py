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
        ''' deletes the old spriteList and creates a new one (e.g.: to start a new level)''' 
        
        self.spriteList = []
        
    def update(self, level):
        self.updateCamera(level.player)
        self.updateSpriteList()
        self.updateBg(level.map)
        
    def updateSpriteList(self):
        ''' deletes dead entities from the spriteList'''
        self.spriteList = [sprite for sprite in self.spriteList if sprite.entity.isAlive()]
        
    def renderSprites(self):
        for sprite in self.spriteList:
            self.screen.blit(sprite.getCurFrame().getGraphic(), sprite.entity.position.getTuple())
    
    #TODO: check rendering methods
    def renderMapLayer(self, mapIndex, map):
        ''' renders map Layer
            @param mapIndex: 0 => Layer1
                   map     : 1 => Layer2
        '''
        for y in range( max(self.camera[1] // constants.TILESIZE, 0), 
                        min(map.getDimensions()[1], (self.camera[1] + constants.RESOLUTION[1]) // constants.TILESIZE + 1)):
            for x in range(max(self.camera[0] // constants.TILESIZE, 0), 
                           min(map.getDimensions()[0], (self.camera[0] + constants.RESOLUTION[0]) // constants.TILESIZE + 1)):
                if map.getMapGrid()[0][x][y] != 0:
                    self.screen.blit(map.tiles[map.getMapGrid()[0][x][y]][2], (x*constants.TILESIZE - self.camera[0],y*constants.TILESIZE - self.camera[1]))

    def renderBg(self, map):
        #TODO: change bgLayer data (new class?!)
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
        
        if (playerInstance.position[0]-self.camera[0] > (constants.RESOLUTION[0] )):
            cameraOffset = util.Vector((playerInstance.position[0]-self.camera[0])-(constants.RESOLUTION[0] ), 0)
        
        #if playerInstance.position[0] - constants.RESOLUTION[0]/2 > 0:
        #    self.camera = util.Vector(playerInstance.position[0] - constants.RESOLUTION[0]/2 , 0)


            
            
        
        
        self.camera += cameraOffset
        #print self.camera

class Sprite(object):
    ''' respresents the graphical reprentation of one entity '''
    
    def __init__(self, entity, renderer):
        self.entity = entity
        self.renderer = renderer
        
        self.animationDict = {} #{type,Animation}

        self.curAni = None

    def addAnimation(self, aniType):
        self.animationDict[aniType] = Animation(aniType, self.renderer)
    
    def addImage(self, aniType, index, path):
        self.animationDict[aniType].addImage(index, path)
    
    def setAni(self, aniType):
        self.curAni = self.animationDict[aniType]
        self.curAni.reset()
    
    def getCurFrame(self):
        ''' @return: image-object of the current frame in the current animation '''
        return self.curAni.getCurFrame()

    
    def renderGrid(self):
        ''' needed?! '''
        pass
            
    class Animation():
        ''' respresents on animation of an entity '''
        
        def __init__(self, type, renderer):
            self.type = ""
            self.imageDict = {} #{index,Image}
            self.curFrame = 0
            self.aniDelay = 3   #to switch less often(more realistic)
            self.aniDelayCounter = 0
            self.renderer = renderer
        
        def addImage(self, index, path):
            ''' adds image object to animation '''
            
            self.imageDict[index] = Image(path, self.renderer)
            
        def reset(self):
            ''' resets the Animation '''
            
            self.curFrame = 0;
            self.aniDelayCounter = 0
            
        def update(self):
            if self.aniDelayCounter < self.aniDelay:
                self.aniDelayCounter += 1
            else:
                if self.curFrame + 1 == len(self.imageDict): #TODO: check if len(dict) works as intended
                    self.curFrame = 0
                else:
                    self.curFrame += 1
                self.aniDelayCounter = 0

        def getCurFrame(self):
            ''' @return: image-object of the current frame '''
            return self.imageDict[curFrame]
            
        class Image():
            ''' respresents one Image of a animation '''
            
            def __init__(self, path, renderer):
                self.dimensions = [0,0];
                self.renderer = renderer

                if not path in self.renderer.imageList:    #if the image doesn't exist in the imageDict, it gets added
                    self.renderer.imageList[path] = util.load_image(graphicPath)

                self.image = self.renderer.imageList[path];
            
                #TODO: get dimensions from image
            
            def getGraphic(self):
                ''' 
                @return: the real grafic(pygame surface)
                '''
                
                return self.image
