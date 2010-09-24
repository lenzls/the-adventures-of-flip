'''
Created on 07.07.2009

@author: CaptnLenz
'''

from util.vector import Vector
import util.constants as constants
from util.dataStorage.collision import ColShape

class PhysicManager(object):

    def __init__(self):
        self.gravity = Vector(0,1)
        self.colShapeList = []

    def createColShape(self, entity):
        colShape = ColShape(entity, self)
        self.addToColShapeList(colShape)
        return colShape

    def addToColShapeList(self, colShape):
        self.colShapeList.append(colShape)

    def clearColShapeList(self):
        ''' deletes the old colShapeList and creates a new one(e.g.: 2 start a new level)''' 
        
        self.colShapeList = []

    def updateColShapes(self):
        for colShape in self.colShapeList:
            colShape.update()

    def cleanColShapeList(self):
        ''' deletes dead entities from the colShapeList'''
        self.colShapeList = [colShape for colShape in self.colShapeList if colShape.getEntity().isAlive()]

    def update(self, level):
        self.updateColShapes()
        self.checkCols(level.map)
        self.cleanColShapeList()

    def checkCols(self, map):
        self.checkEntityMapCollision(map)
        self.checkPlayerEntityCollision()

    def checkEntityMapCollision(self, map):
        for colShape in self.colShapeList:            
            #only the outer rect is getting checked
            
            #TODDO: check if rect.x or rect.left is the right
            midTop       = Vector( (colShape.getOuterRect().midTop[0]		// constants.TILESIZE) , (colShape.getOuterRect().midTop[1]		// constants.TILESIZE) )
            midBottom    = Vector( (colShape.getOuterRect().midBottom[0]	// constants.TILESIZE) , (colShape.getOuterRect().midBottom[1]	// constants.TILESIZE) )
            midRightSide = Vector( (colShape.getOuterRect().midRight[0]		// constants.TILESIZE) , (colShape.getOuterRect().midRight[1]	// constants.TILESIZE) )
            midLeftSide  = Vector( (colShape.getOuterRect().midLeft[0]		// constants.TILESIZE) , (colShape.getOuterRect().midLeft[1]	// constants.TILESIZE) )

            #bewegt sich nach oben
            if colShape.entity.velocity[1] < 0:
                if map.getTileDangerousness(0, midTop) == True:
                    colShape.entity.setDead()
                if map.getTileAccessibility(0, midTop) == True:
                    colShape.entity.mapColWhileMoveUp(midTop)

            #bewegt sich nach unten
            elif colShape.entity.velocity[1] > 0:
                if map.getTileDangerousness(0, midBottom) == True:
                    colShape.entity.setDead()
                if map.getTileAccessibility(0, midBottom) == True:
                    colShape.entity.mapColWhileMoveDown(midBottom)

            #Bewegung nach rechts
            if colShape.entity.velocity[0] > 0:
                if map.getTileDangerousness(0, midRightSide) == True:
                    colShape.entity.setDead()
                if map.getTileAccessibility(0, midRightSide) == True:
                    colShape.entity.mapColWhileMoveRight(midRightSide)                      
        
            #Bewegung nach links
            elif colShape.entity.velocity[0] < 0:
                if map.getTileDangerousness(0, midLeftSide) == True:
                    colShape.entity.setDead()
                if map.getTileAccessibility(0, midLeftSide) == True:
                    colShape.entity.mapColWhileMoveLeft(midLeftSide)

    def checkPlayerEntityCollision(self):
        for shapeA in self.colShapeList:
            if shapeA.entity.type == 'player':
                for shapeB in self.colShapeList:
                    if shapeB.entity.type != 'player':
                        if shapeA.getOuterRect().colliderect(shapeB.getOuterRect()):
                            #TODO: translate
                            # both outer rects overlap -> check "genauer"
                            self.collisionBetween2ColShapes(shapeA, shapeB)
                return

    def collisionBetween2ColShapes(self, a ,b): #a=player b=enemy        
        for absColRectA in a.getAbsoluteColRectList():
            for absColRectB in b.getAbsoluteColRectList():
                eventCode = self.collisionBetween2ColRects(absColRectA, absColRectB)
                if eventCode == 0:
                    continue
                #player win
                elif eventCode == 1:
                    a.entity.colWin(b.entity)
                    b.entity.colLose(a.entity)
                #enemy win
                elif eventCode == 2:
                    a.entity.colLose(b.entity)
                    b.entity.colWin(a.entity)

    def collisionBetween2ColRects(self, a, b):
        if not a.getRect().colliderect(b.getRect()):
            return 0 

        if a.isSpike and b.isBody:      #collides the player-weapon with the enemy-body: player wins
            return 1
        elif a.isSpike and b.isSpike:   #collides the player-weapon with the enemy-weapon: player loses
            return 2
        elif a.isBody and b.isSpike:    #collides the player-body with the enemy-weapon: player loses
            return 2
        elif a.isBody and b.isBody:     #collides the player-body with the enemy-body: nothing happens 
            return 0

        #codes: 0= nothing happens| 1= enemy is dead| 2= player is dead
