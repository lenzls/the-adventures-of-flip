'''
Created on 13.09.2010

should be only classes with members and getter/setters pure data storage

@author: simon
'''
from util.vector import Vector



class Tile(object):
    def __init__(self, name, type, graphic, access, dangerous):
        self.name = name
        self.type = type
        self.graphic = graphic
        self.accessibility = access
        self.dangerousness = dangerous
        
    def getName(self):
        return self.name
        
    def getType(self):
        return self.type
        
    def getGraphic(self):
        return self.graphic
        
    def getAccessibility(self):
        return self.accessibility
        
    def getDangerousness(self):
        return self.dangerousness

class BgLayer(object):
    def __init__(self, speed, graphic):
        self.speed = speed
        self.graphic = graphic
        self.position = Vector(0,0)
    
    def getGraphicSize(self):
        return self.graphic.size()
    
    def getSpeed(self):
        return self.speed
    
    def getGraphic(self):
        return self.graphic

    def getPosition(self):
        return self.position