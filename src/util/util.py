'''
Created on 07.07.2009

@author: CaptnLenz
'''

import pygame
import os

#moved to ressourceLoader
#===============================================================================
# def load_image(filename):
#    path = os.path.join('..', 'data', 'gfx',  filename)
#    try:
#        surface = pygame.image.load(path)
#    except:
#        print path
#        print "Grafik: ",path," kann nicht geladen werden!"
#    return surface.convert_alpha()
#===============================================================================

def load_sound(filename):
    path = os.path.join('..', 'data', 'sfx', filename)
    try:
        sound_object = pygame.mixer.Sound(path)
    except:
        print "Sound: ",path," kann nicht geladen werden!"
    return sound_object