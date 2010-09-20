'''
Created on 17.09.2010

@author: simon
'''
from util.vector import Vector

class ColShape(object):

    def __init__(self, entity, physics):
        self.entity = entity
        self.physics = physics
        self.outerRect = None
        self.innerRectsDict = {}
        self.rectList = []

    def calcOuterRect(self):
        width = 0
        height = 0
        for rect in self.rectList:
            if (rect.posUpperLeft[0] + rect.dimensions[0]) > width:
                width = (rect.posUpperLeft[0] + rect.dimensions[0])
            if (rect.posUpperLeft[1] + rect.dimensions[1]) > height:
                height = (rect.posUpperLeft[1] + rect.dimensions[1])
        self.outerRect = (self.entity.getPosition()[0], self.entity.getPosition()[1], width, height)

    def addRect(self, posUpperLeft, dimensions, isBody, isSpike):
        self.rectList.append(self.ColRect(self, posUpperLeft, dimensions, isBody, isSpike))
        self.calcOuterRect()

    def getAbsoluteColRectList(self):
        return [rect.getAbsoluteRect() for rect in self.rectList]

    def getEntity(self):
        return self.entity

    def update(self):
        for rect in self.rectList:
            rect.calcAbsPos();

    def getOuterDimensions(self):
        return (self.outerRect[2], self.outerRect[3])

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

        def getAbsoluteRect(self):
            return (self.absPos[0], self.absPos[1], self.dimensions[0], self.dimensions[1])

        def calcAbsPos(self):
            self.absPos = self.colShape.entity.getPosition() + self.posUpperLeft
