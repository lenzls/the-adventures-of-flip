'''
Created on 09.07.2009

@author: CaptnLenz
'''

import os
import pygame
import util.constants as constants
from dialog import SpeechBubble 
from util.options import Options
from util.ressourceLoader import RessourceLoader

class Interface(object):

    def __init__(self):
        self.dialogManager = self.DialogManager()
        self.schriftart = RessourceLoader.load_font("courier_new.ttf", 15)
        self.bar = pygame.Surface((Options.getOption("RESOLUTION")[0],17))
        self.bar.fill((130,130,130))
        
        self.score = 0
        self.fps = 0

    def update(self, score, fps):
        self.score = score
        self.fps = fps

    def render(self, screen):
        screen.blit(self.bar,(0,0))
        screen.blit(self.schriftart.render('Score:' + str(self.score),1,[0,0,0]),(0+20,0))
        screen.blit(self.schriftart.render('FPS:' + str(round(self.fps,2)),1,[0,0,0]),(Options.getOption("RESOLUTION")[0]-100,0))

    class DialogManager(object):
        def __init__(self):
            self.dialogQueue = []
        
        def addDialog(self, msg, curGameState):
            self.dialogQueue.append(SpeechBubble(msg, curGameState))

        def isNewDialog(self):
            if len(self.dialogQueue) > 0 : return True
            else: return False
            
        def next(self):
            next = self.dialogQueue[0]
            del(self.dialogQueue[0])
            return next
