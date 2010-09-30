'''
Created on 29.09.2010

@author: simon
'''
import pygame

class SpeechBubble(object):
    def __init__(self, msg, curGameState):
        self.msg = msg
        self.lineStringList = self.calcLineString()
        self.curLineC = 0
        self.curLineString = self.lineStringList[self.curLineC]
        self.curGameState = curGameState
        self.isFinished = False

	def calcLineString(self):
		return self.msg.split(',')

    #TODO improve name
    def execute(self):
        print "execute ", self.msg
        while True:
            self.curGameState.render()
            self.update()
            self.curGameState.gameRenderer.renderBubble(self)
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.next_row()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.isFinished = True

            if self.isFinished == True:
                break
    
    def update(self):
		try:
			self.curLineString = self.lineStringList[self.curLineC]
		except:
			self.isFinished = True

    def next_row(self):
        self.curLine += 1
