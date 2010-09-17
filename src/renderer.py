'''
Created on 07.07.2009

@author: CaptnLenz
'''

from util.vector import Vector
import util.constants as constants


class RenderManager(object):
    '''
    classdocs
    '''

    def __init__(self, screen, ressourceLoader):
        '''
        Constructor
        '''
        self.ressourceLoader = ressourceLoader
        self.screen = screen
        self.spriteList = []
        self.camera = Vector(0,0)
        
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
            print (sprite.entity.getPosition() - self.camera)
            self.screen.blit(sprite.getCurFrame().getGraphic(), (sprite.entity.getPosition() - self.camera).getTuple())
    
    #TODO: check rendering methods
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
            self.screen.blit(bgLayer.getGraphic(), (bgLayer.getPosition()[0] - self.camera[0], 0))
    
    def updateBg(self, map):
        '''update method for paralax scrolling'''
        pass
    
    def getCamera(self):
        return self.camera
    
    def updateCamera(self, playerInstance): #TODO:bad name
        '''
        
        @param playerInstance: instance of the current player object
        '''
#        print "vorher", self.camera
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

class Sprite(object):
    ''' respresents the graphical reprentation of one entity '''
    
    
    def __init__(self, entity, renderer):
        self.entity = entity
        self.renderer = renderer
        
        self.animationDict = {} #{type,Animation}

        self.curAni = "idle" #type of the cur ani

    def addAnimation(self, aniType, graphicFilenames):
        self.animationDict[aniType] = self.Animation(aniType, self.renderer, graphicFilenames)

    def setAni(self, aniType):
        self.curAni = aniType
        self.animationDict[self.curAni].reset()
    
    def getCurFrame(self):
        ''' @return: image-object of the current frame in the current animation '''
        return self.animationDict[self.curAni].getCurFrame()
    
    def update(self):
        self.animationDict[self.curAni].update()

    def renderGrid(self):
        ''' needed?! '''
        pass

    def getImageSize(self):
        #TODO: smarter cecking and error handling
        graphicSize = None
        for ani in self.animationDict.values():
            for image in ani.getImageDict().values():
                if graphicSize == None:
                    graphicSize = image.getDimensions()
                else:
                    if graphicSize != image.getDimensions():
                        print("inconsistent graphic dimensions in Sprite of: ", self.entity)
                        return "error"
        return graphicSize

            
    class Animation():
        ''' respresents on animation of an entity '''
        
        def __init__(self, type, renderer, initGraphicFilenames):
            self.type = ""
            self.imageDict = {} #{index,ImageObject}
            self.curFrameIndex = 0
            self.aniDelay = 3   #to switch less often(more realistic)
            self.aniDelayCounter = 0
            self.renderer = renderer
            
            index = 0
            for filename in initGraphicFilenames:
                self.addImage(index, filename)
                index += 1

        def getImageDict(self):
            return self.imageDict
        
        def addImage(self, index, path):
            ''' adds image object to animation '''
            
            self.imageDict[index] = self.Image(path, self.renderer)
            
        def reset(self):
            ''' resets the Animation '''
            
            self.curFrameIndex = 0;
            self.aniDelayCounter = 0
            
        def update(self):
            if self.aniDelayCounter < self.aniDelay:
                self.aniDelayCounter += 1
            else:
                if self.curFrameIndex + 1 == len(self.imageDict): #TODO: check if len(dict) works as intended
                    self.curFrameIndex = 0
                else:
                    self.curFrameIndex += 1
                self.aniDelayCounter = 0

        def getCurFrame(self):
            ''' @return: image-object of the current frame '''
            return self.imageDict[self.curFrameIndex]
            
        class Image():
            ''' respresents one Image of a animation '''
            
            def __init__(self, filename, renderer):
                self.dimensions = [0,0];
                self.renderer = renderer
         

                self.graphic = self.renderer.ressourceLoader.load_graphic(filename)

                self._calcDimensions()

            def _calcDimensions(self):
                self.dimensions = self.graphic.get_size()
            
            def getGraphic(self):
                ''' 
                @return: the real grafic(pygame surface)
                '''
                
                return self.graphic

            def getDimensions(self):
                return self.dimensions