'''
Created on 17.09.2010

@author: simon
'''
from util.vector import Vector
import pygame

class ColShape(object):

    def __init__(self, entity, physics):
        self.entity = entity
        self.physics = physics
        self.outerRect = None
        self.innerRectsDict = {}
        self.colRectList = []

    def calcOuterRect(self):
        width = 0
        height = 0
        for colRect in self.colRectList:
            if colRect.posUpperLeft[0] + colRect.getRect().width > width:
                width = colRect.posUpperLeft[0] + colRect.getRect().width
            if colRect.posUpperLeft[1] + colRect.getRect().height > height:
                height = colRect.posUpperLeft[1] + colRect.getRect().height
        self.outerRect = pygame.Rect(self.entity.getPosition().getTuple(), (width, height))

    def addRect(self, posUpperLeft, dimensions, isBody, isSpike):
        self.colRectList.append(self.ColRect(self, posUpperLeft, dimensions, isBody, isSpike))
        self.calcOuterRect()

    def getAbsoluteColRectList(self):
        return [colRect for colRect in self.colRectList]

    def getEntity(self):
        return self.entity

    def update(self):
        self.outerRect.topleft = self.entity.getPosition().getTuple()
        for colRect in self.colRectList:
            colRect.update();

    def getOuterDimensions(self):
        return (self.outerRect.width, self.outerRect.height)
        
    def getOuterRect(self):
        return self.outerRect

    class ColRect(object):

        def __init__(self, colShape, posUpperLeft, dimensions, isBody, isSpike):
            self.colShape = colShape
            #pos from the upperLeft corner of the rect referring to the position of the entity(it's upperLeft corner
            self.posUpperLeft = Vector(posUpperLeft[0], posUpperLeft[1])
            self.dimensions = dimensions
            #if true, the entity is dead when it collides with the player
            self.isBody = isBody
            #if true, the player is dead when it collides with the player
            self.isSpike = isSpike
            #absolute position in the whole level
            self.absPos = self.colShape.entity.getPosition() + self.posUpperLeft

            self.rect = pygame.Rect(self.absPos.getTuple(), self.dimensions)

        def update(self):
            self.calcAbsPos()
            self.rect.topleft = self.absPos.getTuple()

        def getRect(self):
            return self.rect

        def calcAbsPos(self):
            self.absPos = self.colShape.entity.getPosition() + self.posUpperLeft
