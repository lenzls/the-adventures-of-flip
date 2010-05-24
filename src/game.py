'''
Created on 07.07.2009

@author: CaptnLenz
'''

import constants
import interface
import intro
import levelManager
import map
import physic
import pygame
import renderer
import util


pygame.init()

class StateManager(object):
    '''
    classdocs
    '''


    def __init__(self, resolution):
        '''
        Constructor
        '''
        
        '''parameter2attribute'''
        self.resolution = resolution
        '''-------------------'''
        '''initialize screen'''
        
        pygame.display.set_caption("The Adventures of Flip")  
        pygame.display.set_icon(pygame.image.load('../data/icon.png'))
        self.screen = pygame.display.set_mode(self.resolution)
        #self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)   #For Fullscreen!!
        '''-----------------'''
        
        self.renderManager = renderer.RenderManager(self.screen)
        self.physicManager = physic.PhysicManager()
        self.levelManager = levelManager.LevelManager(self.physicManager, self.renderManager)
        self.interface = interface.Interface()
        
        '''initialize Gamestates'''
        self.stateList = []
        self.stateList.append(GameState(self))
        self.stateList.append(MenuState(self))
        self.stateList.append(PauseState(self))
        '''---------------------'''
        
        self.isSound = True
        self.curState = self.stateList[0]
        
        self.run = True
    
        
        intro.Opening().play()
        
    def endGame(self):
        self.run = False
        
    def startGame(self):
        
        '''set the starting time; set the first update times'''
        curMilliseconds = pygame.time.get_ticks()
        nextRenderMilliseconds = curMilliseconds
        nextTickMilliseconds = curMilliseconds
        '''-------------------------------------------------'''
        
        '''main loop:'''
        while self.run:
            '''update everything'''
            while nextTickMilliseconds <= curMilliseconds:
                
                self.curState.handleInput()
                self.curState.update()
                
                nextTickMilliseconds += (1000 // constants.LOGIC_FPS)
            '''------'''
            
            '''only the rendering'''       
            if nextRenderMilliseconds <= curMilliseconds:
                while nextRenderMilliseconds <= curMilliseconds:
                    
                    self.curState.render()
                    
                    nextRenderMilliseconds += (1000 // constants.RENDER_FPS)
            '''------------------'''
            pygame.time.wait(min(nextTickMilliseconds, nextRenderMilliseconds) - curMilliseconds) #let the process sleep until the next sheduled update
            curMilliseconds = pygame.time.get_ticks()
            pygame.display.update()
        '''----------'''
        
class GameState(object):
    def __init__(self, stateManager):
        
        self.stateManager = stateManager
        
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
        self.stateManager.physicManager.update(self.stateManager.levelManager.curLevel.map)
        self.stateManager.renderManager.update(self.stateManager.levelManager.curLevel.map)
        self.stateManager.levelManager.update()
        #print(self.stateManager.levelManager.curLevel.player.position)
    
    def render(self):
        self.stateManager.renderManager.renderBg(self.stateManager.levelManager.curLevel.map)
        self.stateManager.renderManager.renderMapLayer1(self.stateManager.levelManager.curLevel.map)
        self.stateManager.renderManager.renderSprites()
        self.stateManager.renderManager.renderMapLayer2(self.stateManager.levelManager.curLevel.map)
    
class MenuState(object):
    def __init__(self, stateManager):
        
        self.stateManager = stateManager
        
        
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
    
class PauseState(object):
    def __init__(self, stateManager):
        
        self.stateManager = stateManager
        
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