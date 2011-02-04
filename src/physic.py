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
    
    def reset(self):
        self.resetColShapeList()

    def createColShape(self, entity):
        colShape = ColShape(entity, self)
        return colShape

    def addToColShapeList(self, colShape):
        self.colShapeList.append(colShape)

    def resetColShapeList(self):
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
            midTop       = Vector( (colShape.getOuterRect().midtop[0]		// constants.TILESIZE) , (colShape.getOuterRect().midtop[1]		// constants.TILESIZE) )
            midBottom    = Vector( (colShape.getOuterRect().midbottom[0]	// constants.TILESIZE) , (colShape.getOuterRect().midbottom[1]	// constants.TILESIZE) )
            midRightSide = Vector( (colShape.getOuterRect().midright[0]		// constants.TILESIZE) , (colShape.getOuterRect().midright[1]	// constants.TILESIZE) )
            midLeftSide  = Vector( (colShape.getOuterRect().midleft[0]		// constants.TILESIZE) , (colShape.getOuterRect().midleft[1]	// constants.TILESIZE) )

            #bewegt sich nach oben
            if colShape.entity.velocity[1] < 0:
                if map.getTileDangerousness(1, midTop) == True:
                    colShape.entity.setDead()
                if map.getTileAccessibility(1, midTop) == True:
                    colShape.entity.mapColWhileMoveUp(midTop)

            #bewegt sich nach unten
            elif colShape.entity.velocity[1] > 0:
                if map.getTileDangerousness(1, midBottom) == True:
                    colShape.entity.setDead()
                if map.getTileAccessibility(1, midBottom) == True:
                    colShape.entity.mapColWhileMoveDown(midBottom)

            #Bewegung nach rechts
            if colShape.entity.velocity[0] > 0:
                if map.getTileDangerousness(1, midRightSide) == True:
                    colShape.entity.setDead()
                if map.getTileAccessibility(1, midRightSide) == True:
                    colShape.entity.mapColWhileMoveRight(midRightSide)                      
        
            #Bewegung nach links
            elif colShape.entity.velocity[0] < 0:
                if map.getTileDangerousness(1, midLeftSide) == True:
                    colShape.entity.setDead()
                if map.getTileAccessibility(1, midLeftSide) == True:
                    colShape.entity.mapColWhileMoveLeft(midLeftSide)

    def checkPlayerEntityCollision(self):

        collisionList = []
        playerShapeLst = [shape for shape in self.colShapeList if shape.entity.type == 'player']
        if len(playerShapeLst) == 1:
            playerShape = playerShapeLst[0]
        else:
            print"more than one player defined!"

        if playerShape.entity.type == 'player':
            for shapeB in self.colShapeList:
                if shapeB.entity.type != 'player':
                    if playerShape.getOuterRect().colliderect(shapeB.getOuterRect()):
                        #TODO: translate
                        # both outer rects overlap -> check "genauer"
                        self.collisionBetween2ColShapes(playerShape, shapeB)
                        collisionList.append(shapeB.entity)

        #removes items from players collide list that were not hitten this run
        for item in playerShape.entity.collideBusyList:
            if not item in collisionList:
                playerShape.entity.collideBusyList.remove(item)

    def collisionBetween2ColShapes(self, a ,b): #a=player b=enemy
        for absColRectA in a.getAbsoluteColRectList():
            for absColRectB in b.getAbsoluteColRectList():
                eventCode = self.collisionBetween2ColRects(absColRectA, absColRectB)
                if eventCode == 0:
                    continue
                else:
                    if not b.entity in a.entity.collideBusyList:
                        a.entity.collideBusyList.append(b.entity)

                        #player win
                        if eventCode == 1:
                            a.entity.colWin(b.entity)
                            b.entity.colLose(a.entity)
                        #enemy win
                        elif eventCode == 2:
                            a.entity.colLose(b.entity)
                            b.entity.colWin(a.entity)


    def collisionBetween2ColRects(self, a, b):
        if not a.getRect().colliderect(b.getRect()):
            return 0
        if not b.isBody and not b.isSpike:
            return 0
        elif a.isSpike and b.isBody:      #collides the player-weapon with the enemy-body: player wins
            return 1
        elif a.isSpike and b.isSpike:   #collides the player-weapon with the enemy-weapon: player loses
            return 2
        elif a.isBody and b.isSpike:    #collides the player-body with the enemy-weapon: player loses
            return 2
        elif a.isBody and b.isBody:     #collides the player-body with the enemy-body: nothing happens 
            return 0
        

        #codes: 0= nothing happens| 1= enemy is dead| 2= player is dead
