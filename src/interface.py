'''
Created on 09.07.2009

@author: CaptnLenz
'''

import os
import pygame
import util.constants as constants

class Interface(object):

    def __init__(self):
        self.schriftart = pygame.font.Font(os.path.join('..','data','courier_new.ttf'),15)
        self.bar = pygame.Surface((constants.RESOLUTION[0],17))
        self.bar.fill((130,130,130))
        
        self.score = 0
        self.fps = 0

    def update(self, score, fps):
        self.score = score
        self.fps = fps

    def render(self, screen):
        screen.blit(self.bar,(0,0))
        screen.blit(self.schriftart.render('Score:' + str(self.score),1,[0,0,0]),(0+20,0))
        screen.blit(self.schriftart.render('FPS:' + str(round(self.fps,2)),1,[0,0,0]),(constants.RESOLUTION[0]-100,0))