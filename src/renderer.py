'''
Created on 07.07.2009

@author: CaptnLenz
'''

from util.vector import Vector
from util.dataStorage.rendering import Sprite
import util.constants as constants
import pygame
import os

class Renderer(object):

    def __init__(self, screen):
        self.screen = screen
        
        self.gridFont = pygame.font.Font(os.path.join('..','data','courier_new.ttf'),15)

    

class GameRenderer(Renderer):
    def __init__(self, screen):
        Renderer.__init__(self, screen)
        self.spriteList = []
        self.camera = Vector(0,0)
        
        self.dialogFont = pygame.font.Font(os.path.join('..','data','courier_new.ttf'),15)
        self.dialogBackground =  pygame.Surface((400, 100))
        self.dialogBackground.fill((155,155,155))
        
        self.blackBar = pygame.Surface((constants.RESOLUTION[0], 25))

    def createSprite(self, entity):
        sprite = Sprite(entity)
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
            
    def renderBoundingBoxes(self, colShapeList):
        for cShape in colShapeList:
            pygame.draw.rect(self.screen, (0,0,255), cShape.getOuterRect().move(-self.camera[0],-self.camera[1]), 1)
            for cRect in cShape.getAbsoluteColRectList():
                if cRect.isSpike:
                    color = (255,255,255)
                else:
                    color = (255,0,255)
                pygame.draw.rect(self.screen, color, cRect.getRect().move(-self.camera[0], -self.camera[1]), 1)

    def renderBlackBars(self):
        '''black bars for cutscenes'''
        self.screen.blit(self.blackBar, (0,0))
        self.screen.blit(self.blackBar, (0, constants.RESOLUTION[1]- self.blackBar.get_height()))

    def renderSprites(self):
        for sprite in self.spriteList:
            self.screen.blit(sprite.getCurFrame().getGraphic(), (sprite.entity.getPosition() - self.camera).getTuple())

    def renderGrid(self, map):
        # To show the "tilegrid" change the step to 32
        for x in range(0, map.getDimensions()[0]*constants.TILESIZE,32):
            pygame.draw.line(self.screen,[255,0,255],(x-self.camera[0],0),(x-self.camera[0],constants.RESOLUTION[1]))
            surface = self.gridFont.render(str(x),1,[255,0,255])
            self.screen.blit(surface,((x+2)-self.camera[0],20))
        
        for y in range(0, map.getDimensions()[1]*constants.TILESIZE,32):
            pygame.draw.line(self.screen,[255,0,255],(0,y-self.camera[1]),(constants.RESOLUTION[0],y-self.camera[1]))
            surface = self.gridFont.render(str(y),1,[255,0,255])
            self.screen.blit(surface,(20,(y+2)-self.camera[1]))

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
                    self.screen.blit(map.getTileGraphic(layerIndex,Vector(x,y)), (x*constants.TILESIZE - self.camera[0],y*constants.TILESIZE - self.camera[1]))

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

    def updateCamera(self, playerInstance):
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

    def renderInterface(self, interface):
        interface.render(self.screen)
        
    def renderBubble(self, bubble):
        bgRect = pygame.Rect( (constants.RESOLUTION[0]-self.dialogBackground.get_width())//2 , (constants.RESOLUTION[1]-self.dialogBackground.get_height())//2 , self.dialogBackground.get_width()  , self.dialogBackground.get_height() )
        padding = [10,5]
        
        self.screen.blit(self.dialogBackground,(bgRect.topleft[0], bgRect.topleft[1]))
        pygame.draw.rect(self.screen,[50,50,50], bgRect, 5)
        iRow = 0
        for line in bubble.curPageList:
            surface = self.dialogFont.render(line,1,[0,0,0])
            self.screen.blit(surface, ((bgRect.topleft[0]+padding[0], bgRect.topleft[1]+padding[1] + (iRow*25))))
            iRow += 1

class MenuRenderer(Renderer):
    def __init__(self, screen):
        Renderer.__init__(self, screen)

        self.itemFont = pygame.font.Font(os.path.join('..','data','courier_new.ttf'),20)
        self.headingFont = pygame.font.Font(os.path.join('..','data','courier_new.ttf'),20)

    def renderMenu(self, menu):
        # render background
        self.screen.blit(menu.getBackground(),(0,0))

        #render heading
        self.screen.blit(self.headingFont.render(menu.getHeading(),1,[255,255,255]),(((constants.RESOLUTION[0]//2)-100),100))

        # render Items
        y = 150
        for mItem in menu.getMenuItems():
            self.screen.blit(self.itemFont.render(mItem.getCaption(),1,mItem.getColor()),((constants.RESOLUTION[0]//2)-100, y))
            y += 50
