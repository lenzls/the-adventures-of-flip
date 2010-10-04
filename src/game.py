'''
Created on 07.07.2009

@author: CaptnLenz
'''
import os
import interface.interface as interface
import intro
import levelManager
from menu import menuManager
import physic
import pygame
import renderer
import menu.menu as menu
import util.constants as constants
from util.events import Event

from util.vector import Vector
from butterfly.util.decorator import deprecated

pygame.init()

class StateManager(object):
    
    GAMESTATE = 0
    MENUSTATE = 1
    PAUSESTATE = 2

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

        self.switchState(self.MENUSTATE)

        self.run = True

        self.clock = pygame.time.Clock()
        
        intro.Opening().play()
        
    def getGameState(self):
        return self.stateList[self.GAMESTATE]

    def getMenuState(self):
        return self.stateList[self.MENUSTATE]
    
    def getPauseState(self):
        return self.stateList[self.PAUSESTATE]
    
    def switchState(self, stateI):
        self.curState = self.stateList[stateI]

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
                elif event.key == pygame.K_p:
                    Event().raiseCstmEvent(Event.SWITCHSTATE, argDict={"state" : StateManager.PAUSESTATE})
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if not self.levelManager.curLevel.cutSceneState: self.levelManager.curLevel.player.walkStop()
                elif event.key == pygame.K_RIGHT:
                    if not self.levelManager.curLevel.cutSceneState: self.levelManager.curLevel.player.walkStop()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if constants.DEBUG: print "The current cursor position is: ", Vector(event.pos[0],event.pos[1])+self.gameRenderer.getCamera()

            #custom events:
            elif event.type == Event().ACTIVATETRIGGER:
                self.levelManager.curLevel.triggerManager.addTrigger(event.tObject)
            elif event.type == Event().NEWDIALOG:
                self.interface.dialogManager.addDialog(event.msg, self)
            elif event.type == Event().LEVELFINISHED:
                self.levelManager.curLevel.setFinished()
            elif event.type == Event().SWITCHSTATE:
                self.stateManager.switchState(event.state)

        #Trigger input:
        if self.levelManager.curLevel.triggerManager.isNewEvents():
            self.levelManager.curLevel.triggerManager.next().action()

    def update(self):
        self.physicManager.update(self.levelManager.curLevel)
        self.gameRenderer.update(self.levelManager.curLevel)
        self.interface.update(self.levelManager.curLevel.getPlayer().getScore(), self.stateManager.clock.get_fps())
        self.levelManager.update()

    def render(self):
        #TODO: maybe move other another place
        if self.interface.dialogManager.isNewDialog():
            self.interface.dialogManager.next().execute()

        self.gameRenderer.renderBg(self.levelManager.curLevel.map)
        self.gameRenderer.renderMapLayer(0, self.levelManager.curLevel.map)
        self.gameRenderer.renderSprites()
        self.gameRenderer.renderMapLayer(1, self.levelManager.curLevel.map)
        if constants.DEBUG: 
            self.gameRenderer.renderGrid(self.levelManager.curLevel.map)
            self.gameRenderer.renderBoundingBoxes(self.physicManager.colShapeList)
        self.gameRenderer.renderInterface(self.interface)
        
        if self.levelManager.curLevel.cutSceneState: self.gameRenderer.renderBlackBars()

class MenuState(State):

    def __init__(self, stateManager):
        State.__init__(self, stateManager)

        self.menuRenderer = renderer.MenuRenderer(self.stateManager.screen)

        self.menuManager = menuManager.MenuManager()

    def handleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.endGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stateManager.endGame()
                elif event.key == pygame.K_UP:
                    self.menuManager.curMenu.moveUp()
                elif event.key == pygame.K_DOWN:
                    self.menuManager.curMenu.moveDown()
                elif event.key == pygame.K_RETURN:
                    self.menuManager.curMenu.execute()
            
            #custom events
            elif event.type == Event().NEWGAME:
                self.stateManager.switchState(self.stateManager.GAMESTATE)
                gameState = self.stateManager.getGameState()
                gameState.levelManager.loadLevel(gameState.levelManager.FIRSTLEVEL)
            elif event.type == Event().SWITCHMENU:
                self.menuManager.loadMenu(event.mIndex)

    def update(self):
        self.menuManager.curMenu.update()

    def render(self):
        self.menuRenderer.renderMenu(self.menuManager.curMenu)

class PauseState(State):

    def __init__(self, stateManager):
        State.__init__(self, stateManager)
        
        self.pauseRenderer = renderer.PauseRenderer(self.stateManager.screen)
        

    def handleInput(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stateManager.endGame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stateManager.endGame()
                elif event.key == pygame.K_p:
                    self.stateManager.switchState(self.stateManager.GAMESTATE)

    def update(self):
        pass

    def render(self):
        self.stateManager.getGameState().render()
        self.pauseRenderer.renderOverlay()
