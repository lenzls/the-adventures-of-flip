'''
Created on 07.07.2009

@author: CaptnLenz
'''
import os
import interface
import intro
import levelManager
import physic
import pygame
import renderer
import menu.menu as menu
import util.constants as constants
from util.events import Event

pygame.init()

class StateManager(object):

    def __init__(self, resolution):
        '''

        @param resolution: screen resolution
        '''

        self.resolution = resolution

        pygame.display.set_caption("The Adventures of Flip")
        pygame.display.set_icon(pygame.image.load(os.path.join('..','data','icon.png')))
        if constants.FULLSCREEN:
            self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.resolution)

        self.renderManager = renderer.RenderManager(self.screen)
        self.physicManager = physic.PhysicManager()
        self.levelManager = levelManager.LevelManager(self.physicManager, self.renderManager)
        self.interface = interface.Interface()

        #=======================================================================
        # self.clock 
        #=======================================================================

        self.stateList = []
        self.stateList.append(GameState(self))
        self.stateList.append(MenuState(self))
        self.stateList.append(PauseState(self))

        self.switchToMenuState()

        self.run = True

        self.clock = pygame.time.Clock()
        
        intro.Opening().play()

    def switchToGameState(self):
        self.curState = self.stateList[0]
        
    def switchToMenuState(self):
        self.curState = self.stateList[1]
        
    def switchToPauseState(self):
        self.curState = self.stateList[2]

    def endGame(self):
        '''
            ends the game after quit events
        '''
        self.run = False

    def startGame(self):
        
        while self.run:
            pygame.display.set_caption("The Adventures of Flip -- FPS: %f" %self.clock.get_fps())
            time_passed = self.clock.tick(constants.FPS)

            self.curState.handleInput()
            self.curState.update()
            self.curState.render()
            pygame.display.update()

class State():

    def __init__(self, stateManager):
        self.stateManager = stateManager

    def handleInput(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

class GameState(State):

    def __init__(self, stateManager):
        State.__init__(self, stateManager)

        self.stateManager.levelManager.loadLevel(0)

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.endGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stateManager.endGame()

                elif event.key == pygame.K_SPACE:
                    self.stateManager.levelManager.curLevel.player.jump()
                elif event.key == pygame.K_LEFT:
                    self.stateManager.levelManager.curLevel.player.walkLeft()
                elif event.key == pygame.K_RIGHT:
                    self.stateManager.levelManager.curLevel.player.walkRight()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.stateManager.levelManager.curLevel.player.walkStop()
                elif event.key == pygame.K_RIGHT:
                    self.stateManager.levelManager.curLevel.player.walkStop()

    def update(self):
        self.stateManager.physicManager.update(self.stateManager.levelManager.curLevel)
        self.stateManager.renderManager.update(self.stateManager.levelManager.curLevel)
        self.stateManager.interface.update(self.stateManager.levelManager.curLevel.getPlayer().getScore(), self.stateManager.clock.get_fps())
        self.stateManager.levelManager.update()

    def render(self):
        self.stateManager.renderManager.renderBg(self.stateManager.levelManager.curLevel.map)
        self.stateManager.renderManager.renderMapLayer(0, self.stateManager.levelManager.curLevel.map)
        self.stateManager.renderManager.renderSprites()
        self.stateManager.renderManager.renderMapLayer(1, self.stateManager.levelManager.curLevel.map)
        self.stateManager.renderManager.renderInterface(self.stateManager.interface)

class MenuState(State):

    def __init__(self, stateManager):
        State.__init__(self, stateManager)

        self.menuList = []
        self.menuList.append(menu.MainMenu())
        
        self.curMenu = self.menuList[0]

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.endGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stateManager.endGame()
                elif event.key == pygame.K_UP:
                    self.curMenu.moveUp()
                elif event.key == pygame.K_DOWN:
                    self.curMenu.moveDown()
                elif event.key == pygame.K_RETURN:
                    self.curMenu.select()
            elif event.type == Event().NEWGAME:
                self.stateManager.switchToGameState()

    def update(self):
        print "curItem: %i" %self.curMenu.curIndex

    def render(self):
        pass

class PauseState(State):

    def __init__(self, stateManager):
        State.__init__(self, stateManager)

    def handleInput(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.endGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stateManager.endGame()

    def update(self):
        pass

    def render(self):
        pass
