'''
Created on 07.07.2009

@author: CaptnLenz
'''

import pygame
import os

def load_tile(filename):
    path = os.path.join('..', 'data', 'tiles',  filename)
    try:
        surface = pygame.image.load(path)
    except:
        print(path)
        print("Grafik: ",path," kann nicht geladen werden!")
    return surface.convert_alpha()

def load_sound(filename):
    path = os.path.join('..', 'data', 'sfx', filename)
    try:
        sound_object = pygame.mixer.Sound(path)
    except:
        print("Sound: ",path," kann nicht geladen werden!")
    return sound_object

class Vector():
    
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    # + operator
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    # - operator
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    # * operator (used for resizing the vector)
    def __mul__(self, factor):
        return Vector(self.x * factor, self.y * factor)
    
    # / operator (used for resizing the vector)
    def __div__(self, factor):
        return Vector(self.x / factor, self.y / factor)
    
    # += operator
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    
    # -= operator
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise Exception('Invalid Key!') 
        
    def __setitem__(self, index, other):
        if index == 0:
            self.x = other
        elif index == 1:
            self.y = other
        else:
            raise Exception('Invalid Key!') 
    
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False
        
    def getTuple(self):
        return (self.x, self.y)
    
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'