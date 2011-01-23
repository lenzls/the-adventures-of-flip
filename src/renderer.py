'''
Created on 07.07.2009

@author: CaptnLenz
'''

from util.vector import Vector
from util.dataStorage.rendering import Sprite
from util.options import Options 
import util.constants as constants
import pygame
import os
from util.ressourceLoader import RessourceLoader

class Renderer(object):

    def __init__(self, screen):
        self.screen = screen
        
        self.gridFont = RessourceLoader.load_font('courier_new.ttf',15)
        
        self.fades = self.Fades(self.screen)
        
        self.resolution = Options.getOption("RESOLUTION")

    class Fades(object):
        
        def __init__(self, screen):
            self.screen = screen
            
            self.resolution = Options.getOption("RESOLUTION")
        
        def update(self):
            if self.resolution != Options.getOption("RESOLUTION"):
                self.resolution = Options.getOption("RESOLUTION")
        
        def renderFade1(self, string):
            '''
                kind of "pulsing"
            '''
            
            bg = pygame.Surface(self.resolution)
            bg.fill((0,0,0))

            font = RessourceLoader.load_font('courier_new.ttf',50)
            writing = font.render(string,1,(255,255,255),(0,0,0))

            for i in range(0,255,5):
                self.screen.blit(bg, (0,0))
                writing.set_alpha(i)
                self.screen.blit(writing,((self.resolution[0]//2 - writing.get_width()//2), (self.resolution[1]//2 - writing.get_height()//2)))
                pygame.display.update()
                pygame.time.wait(30)
            for i in range(255,0,-5):
                self.screen.blit(bg, (0,0))
                writing.set_alpha(i)
                self.screen.blit(writing,((self.resolution[0]//2 - writing.get_width()//2), (self.resolution[1]//2 - writing.get_height()//2)))
                pygame.display.update()
                pygame.time.wait(20)
    
        def renderFadeNewLvl(self, levelName):
            self.renderFade1(levelName)

            # have fun thing:
            bg = pygame.Surface(self.resolution)
            bg.fill((0,0,0))

            font = RessourceLoader.load_font('courier_new.ttf',50)
            writing = font.render("Have Fun!",1,(255,255,255),(0,0,0))
            writingRes = (writing.get_width(), writing.get_height())

            for i in range(1,4,1):
                self.screen.blit(bg, (0,0))
                writing = pygame.transform.scale(writing, (writingRes[0]*i, writingRes[1]*i))
                self.screen.blit(writing,((self.resolution[0]//2 - writing.get_width()//2), (self.resolution[1]//2 - writing.get_height()//2)))
                pygame.display.update()
                pygame.time.wait(100)
            pygame.time.wait(1000)
    

class GameRenderer(Renderer):
    def __init__(self, screen):
        Renderer.__init__(self, screen)
        self.spriteList = []
        self.camera = Vector(0,0)
        
        self.dialogFont = RessourceLoader.load_font('courier_new.ttf',15)
        self.dialogBackground =  pygame.Surface((400, 100))
        self.dialogBackground.fill((155,155,155))

        self.blackBar = pygame.Surface((self.resolution[0], 25))
        
        self.horiBorder = self.resolution[0] // 5
        self.vertiBorder = self.resolution[1] // 5


    def reset(self):
        self.resetSpriteList()
        self.camera = Vector(0,0)

    def createSprite(self, entity):
        sprite = Sprite(entity)
        return sprite

    def appendSpriteList(self, sprite):
        self.spriteList.append(sprite)

    def resetSpriteList(self):
        ''' deletes the old spriteList and creates a new one (e.g.: to start a new level)'''
        self.spriteList = []
         
    def cleanSpriteList(self):
        self.spriteList = [sprite for sprite in self.spriteList if sprite.entity.isAlive()]
        
    def update(self, level):
        if self.resolution != Options.getOption("RESOLUTION"):
            self.resolution = Options.getOption("RESOLUTION")
        self.fades.update()
        self.updateCamera(level.player)
        self.updateSpriteList()
        self.updateBg(level)

    def updateSpriteList(self):
        ''' deletes dead entities from the spriteList'''
        self.cleanSpriteList()
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
        self.screen.blit(self.blackBar, (0, self.resolution[1]- self.blackBar.get_height()))

    def renderSprites(self):
        for sprite in self.spriteList:
            self.screen.blit(sprite.getCurFrame().getGraphic(), (sprite.entity.getPosition() - self.camera).getTuple())

    def renderGrid(self, map):
        # To show the "tilegrid" change the step to 32
        for x in range(0, map.getDimensions()[0]*constants.TILESIZE,32):
            pygame.draw.line(self.screen,[255,0,255],(x-self.camera[0],0),(x-self.camera[0],self.resolution[1]))
            surface = self.gridFont.render(str(x),1,[255,0,255])
            self.screen.blit(surface,((x+2)-self.camera[0],20))
        
        for y in range(0, map.getDimensions()[1]*constants.TILESIZE,32):
            pygame.draw.line(self.screen,[255,0,255],(0,y-self.camera[1]),(self.resolution[0],y-self.camera[1]))
            surface = self.gridFont.render(str(y),1,[255,0,255])
            self.screen.blit(surface,(20,(y+2)-self.camera[1]))

    def renderMapLayer(self, layerIndex, map):
        ''' renders map Layer
            @param layerIndex: 0 => Layer1
                             : 1 => Layer2
        '''
        for y in range(max(self.camera[1] // constants.TILESIZE, 0), 
                       min(map.getDimensions()[1], (self.camera[1] + self.resolution[1]) // constants.TILESIZE + 1)):
            for x in range(max(self.camera[0] // constants.TILESIZE, 0), 
                           min(map.getDimensions()[0], (self.camera[0] + self.resolution[0]) // constants.TILESIZE + 1)):
                if map.getMapGrid()[layerIndex][x][y] != 0:
                    self.screen.blit(map.getTileGraphic(layerIndex,Vector(x,y)), (x*constants.TILESIZE - self.camera[0],y*constants.TILESIZE - self.camera[1]))

    def renderBg(self, map):
        self.screen.fill((0,0,0));
        for bgLayer in map.bgLayers.values():

            # offset left
            self.screen.blit(bgLayer.getGraphic(), 
                             (0, ((map.getDimensions()[1]*constants.TILESIZE) - bgLayer.getDimensions()[1]) - self.camera[1]), 
                             area=pygame.Rect(bgLayer.getDimensions()[0]-bgLayer.getScrollPosition()[0],0,bgLayer.getDimensions()[0],bgLayer.getDimensions()[1]))

            for i in range(bgLayer.getNeededGraphics()+2):
                self.screen.blit(bgLayer.getGraphic(), 
                             (bgLayer.getScrollPosition()[0] + i*bgLayer.getDimensions()[0], ((map.getDimensions()[1]*constants.TILESIZE) - bgLayer.getDimensions()[1]) - self.camera[1]), 
                             area=pygame.Rect(0,0,bgLayer.getDimensions()[0],bgLayer.getDimensions()[1]))
            
            #TODO add offset right instead of drawing one 'too much' in the previous loop
            #following doesn't work correct
#            # offset right
#            self.screen.blit(bgLayer.getGraphic(), 
#                             (lastPosX+bgLayer.getDimensions()[0], ((map.getDimensions()[1]*constants.TILESIZE) - bgLayer.getDimensions()[1]) - self.camera[1]), 
#                             area=pygame.Rect(0,0,(bgLayer.getDimensions()[0]-lastPosX-self.camera[0]),bgLayer.getDimensions()[1]))

    def updateBg(self, level):
        '''update method for paralax scrolling'''

        for bgLayer in level.map.bgLayers.values():
            bgLayer.update(self.camera)#level.player.getPosition())

    def getCamera(self):
        return self.camera

    def updateCamera(self, playerInstance):
        '''
        @param playerInstance: instance of the current player object
        '''

        cameraOffset = Vector(0,0)

        playerPos = playerInstance.getPosition()

        if (playerPos[0] - self.camera[0]) > (self.resolution[0] - self.horiBorder):
            cameraOffset +=  Vector((playerPos[0] - self.camera[0]) - (self.resolution[0] - self.horiBorder),0)
        elif (playerPos[0] - self.camera[0]) < (self.horiBorder):
            cameraOffset -=  Vector((self.horiBorder) - (playerPos[0] - self.camera[0]),0)

        if (playerPos[1] - self.camera[1]) < (self.vertiBorder):
            cameraOffset -=  Vector(0,(self.vertiBorder) - (playerPos[1] - self.camera[1]))

        elif (playerPos[1] - self.camera[1]) > (self.resolution[1] - self.vertiBorder):
            cameraOffset +=  Vector(0,(playerPos[1] - self.camera[1]) - (self.resolution[1] - self.vertiBorder))

        self.camera += cameraOffset

        if playerPos[0] < self.horiBorder:
            self.camera = Vector(0, self.camera[1])
        elif playerPos[0] > playerInstance.map.getDimensions()[0]*constants.TILESIZE-self.horiBorder:
            self.camera = Vector(playerInstance.map.getDimensions()[0]*constants.TILESIZE-self.resolution[0], self.camera[1])

        if playerPos[1] < self.vertiBorder:
            self.camera = Vector(self.camera[0], 0)
        elif playerPos[1] > playerInstance.map.getDimensions()[1]*constants.TILESIZE-self.vertiBorder:
            self.camera = Vector(self.camera[0], playerInstance.map.getDimensions()[1]*constants.TILESIZE-self.resolution[1])
    
    def checkGraphicSizes(self):
        for sprite in self.spriteList:
            sprite.checkimageSizes()

    def renderInterface(self, interface):
        interface.render(self.screen)
        
    def renderBubble(self, bubble):
        bgRect = pygame.Rect( (self.resolution[0]-self.dialogBackground.get_width())//2 , (self.resolution[1]-self.dialogBackground.get_height())//2 , self.dialogBackground.get_width()  , self.dialogBackground.get_height() )
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

        self.itemFont = RessourceLoader.load_font('courier_new.ttf',20)
        self.headingFont = RessourceLoader.load_font('courier_new.ttf',20)
        self.headingFont.set_bold(True)
        self.headingFont.set_underline(True)

    def renderMenu(self, menu):
        self.screen.fill((0,0,0))
        # render background
        self.screen.blit(menu.getBackground(),(0,0))

        #render heading
        self.screen.blit(self.headingFont.render(menu.getHeading(),1,[150,255,150]),(((self.resolution[0]//2)-100),100))

        # render Items
        y = 150
        for mItem in menu.getMenuItems():
            self.screen.blit(self.itemFont.render(mItem.getCaption(),1,mItem.getColor()),((self.resolution[0]//2)-100, y))
            y += 50
            
    def update(self):
        if self.resolution != Options.getOption("RESOLUTION"):
            self.resolution = Options.getOption("RESOLUTION")

class PauseRenderer(Renderer):
    def __init__(self, screen):
        Renderer.__init__(self, screen)
        
        self.pauseOverlay = pygame.Surface(self.resolution, pygame.RLEACCEL)
        self.pauseOverlay.fill((0,0,0))
        self.pauseOverlay.set_alpha(175)
        
        self.pauseFont = RessourceLoader.load_font('courier_new.ttf',50)
        self.fontSurface = self.pauseFont.render("Pause!", 1,(175,175,175))
        self.pauseOverlay.blit(self.fontSurface, ((self.resolution[0]//2)-(self.fontSurface.get_width()//2), (self.resolution[1]//2)-(self.fontSurface.get_height()//2)))
        
    def renderOverlay(self):
        self.screen.blit(self.pauseOverlay,(0,0))
    
    def update(self):
        if self.resolution != Options.getOption("RESOLUTION"):
            self.resolution = Options.getOption("RESOLUTION")

