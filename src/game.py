'''
Created on 07.07.2009

@author: CaptnLenz
'''
import os
import interface.interface as interface
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

        self.gameRenderer = renderer.GameRenderer(self.stateManager.screen)
        self.physicManager = physic.PhysicManager()
        self.levelManager = levelManager.LevelManager(self.physicManager, self.gameRenderer)
        self.interface = interface.Interface()
        
        self.levelManager.loadLevel(0)

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.endGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stateManager.endGame()

                elif event.key == pygame.K_SPACE:
                    if not self.levelManager.curLevel.cutSceneState: self.levelManager.curLevel.player.jump()
                elif event.key == pygame.K_LEFT:
                    if not self.levelManager.curLevel.cutSceneState: self.levelManager.curLevel.player.walkLeft()
                elif event.key == pygame.K_RIGHT:
                    if not self.levelManager.curLevel.cutSceneState: self.levelManager.curLevel.player.walkRight()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if not self.levelManager.curLevel.cutSceneState: self.levelManager.curLevel.player.walkStop()
                elif event.key == pygame.K_RIGHT:
                    if not self.levelManager.curLevel.cutSceneState: self.levelManager.curLevel.player.walkStop()
            
            #custom events:
            elif event.type == Event().NEWTRIGGER:
                self.levelManager.curLevel.triggerManager.addTrigger(event.tObject)

        #Trigger input:
        if self.levelManager.curLevel.triggerManager.isNewEvents():
            self.levelManager.curLevel.triggerManager.next().action()

    def update(self):
        self.physicManager.update(self.levelManager.curLevel)
        self.gameRenderer.update(self.levelManager.curLevel)
        self.interface.update(self.levelManager.curLevel.getPlayer().getScore(), self.stateManager.clock.get_fps())
        self.levelManager.update()

    def render(self):
        self.gameRenderer.renderBg(self.levelManager.curLevel.map)
        self.gameRenderer.renderMapLayer(0, self.levelManager.curLevel.map)
        self.gameRenderer.renderSprites()
        self.gameRenderer.renderMapLayer(1, self.levelManager.curLevel.map)
        if constants.DEBUG: self.gameRenderer.renderGrid(self.levelManager.curLevel.map)
        self.gameRenderer.renderInterface(self.interface)

class MenuState(State):

    def __init__(self, stateManager):
        State.__init__(self, stateManager)

        self.menuRenderer = renderer.MenuRenderer(self.stateManager.screen)

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
                    self.curMenu.execute()
            
            #custom events
            elif event.type == Event().NEWGAME:
                self.stateManager.switchToGameState()

    def update(self):
        self.curMenu.update()

    def render(self):
        self.menuRenderer.renderMenu(self.curMenu)

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
