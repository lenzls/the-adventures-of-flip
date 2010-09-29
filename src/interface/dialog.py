'''
Created on 29.09.2010

@author: simon
'''
import pygame

class SpeechBubble(object):
    def __init__(self, msg, curGameState):
        self.msg = msg
        self.curGameState = curGameState
        self.isFinished = False

    #TODO improve name
    def execute(self):
        print "execute ", self.msg
        while True:
            self.curGameState.render()
            self.update()
            self.render(self.curGameState.gameRenderer.screen)
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.next_row()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.isFinished = True

            if self.isFinished == True:
                break
    
    def update(self):
        pass
    
    def render(self, screen):
        pass
    
    #TODO: check if needed
    def next_row(self):
        pass