'''
Created on 13.09.2010

@author: simon
'''

from util.vector import Vector
from util.dataStorage.rendering import Image
import util.constants as constants

class Tile(object):
    def __init__(self, name, type, graphicName, access, dangerous):
        self.name = name
        self.type = type
        self.image = Image(graphicName)
        self.accessibility = access
        self.dangerousness = dangerous

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getGraphic(self):
        return self.image.getGraphic()

    def getAccessibility(self):
        return self.accessibility

    def getDangerousness(self):
        return self.dangerousness

class BgLayer(object):
    def __init__(self, speed, graphicName):
        self.speed = Vector(speed,0)
        self.image = Image(graphicName)
        self.scrollPosition = Vector(0,0)

        #TODO: name improveable
        self.neededGraphics = 0

        self._calcGraphicCount()

        self.oldPos = Vector(0,0)

    def update(self, playerPos):

        deltaPos = playerPos - self.oldPos

        if deltaPos[0] < 0:
            self.scrollPosition -= self.speed
        elif deltaPos[0] > 0:
            self.scrollPosition += self.speed
        else:
            pass

        if self.scrollPosition[0] < 0:
            self.scrollPosition = Vector(self.getDimensions()[0], 0)
        elif self.scrollPosition[0] > self.getDimensions()[0]:
            self.scrollPosition = Vector(0, 0)

        self.oldPos = Vector(playerPos[0],playerPos[1])

    def _calcGraphicCount(self):
        self.neededGraphics = constants.RESOLUTION[0] // self.getDimensions()[0]

    def getNeededGraphics(self):
        return self.neededGraphics

    def getGraphicSize(self):
        return self.graphic.size()

    def getSpeed(self):
        return self.speed

    def getGraphic(self):
        return self.image.getGraphic()

    def getDimensions(self):
        return self.image.getDimensions()

    def getScrollPosition(self):
        return self.scrollPosition
