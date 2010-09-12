'''
Created on 09.07.2009

@author: CaptnLenz
'''

import pygame
import constants

class Interface(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.schriftart = pygame.font.Font('../data/courier_new.ttf',15)
        self.bar = pygame.Surface((constants.RESOLUTION[0],17))
        self.bar.fill((0,0,0))
        
    def update(self, score):
        self.score = score  #TODO: score auf levelebene!!!!
        
    def render(self, screen):
        screen.blit(self.bar,(0,600))
        screen.blit(self.schriftart.render('Score:' + str(self.score),1,[255,0,0]),(screen.get_width()-100,224))
        