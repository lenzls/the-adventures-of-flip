'''
Created on 07.07.2009

@author: CaptnLenz
'''

from util.vector import Vector
import util.constants as constants


class PhysicManager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
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
#        self.checkPlayerEntityCollision()

    def checkEntityMapCollision(self, map):
        for colShape in self.colShapeList:            
            #only the outer rect is getting checked
            
            midTop       = Vector( (colShape.entity.position[0] + (colShape.getOuterDimensions()[0] // 2) ) // constants.TILESIZE , (colShape.entity.position[1]                                           ) // constants.TILESIZE )
            midBottom    = Vector( (colShape.entity.position[0] + (colShape.getOuterDimensions()[0] // 2) ) // constants.TILESIZE , (colShape.entity.position[1] + (colShape.getOuterDimensions()[1]     ) ) // constants.TILESIZE )
            midRightSide = Vector( (colShape.entity.position[0] + (colShape.getOuterDimensions()[0]    )  ) // constants.TILESIZE , (colShape.entity.position[1] + (colShape.getOuterDimensions()[1] // 2) ) // constants.TILESIZE )
            midLeftSide  = Vector( (colShape.entity.position[0]                                           ) // constants.TILESIZE , (colShape.entity.position[1] + (colShape.getOuterDimensions()[1] // 2) ) // constants.TILESIZE )
   
#            #werdne nurnoch die mitten der Seiten getestet
#            
#            top       = Vector( (colShape.entity.position[0] + (colShape.entity.dimensions[0] // 2) ) // constants.TILESIZE , (colShape.entity.position[1]                                       ) // constants.TILESIZE )
#            bottom    = Vector( (colShape.entity.position[0] + (colShape.entity.dimensions[0] // 2) ) // constants.TILESIZE , (colShape.entity.position[1] + (colShape.entity.dimensions[1]    ) ) // constants.TILESIZE )
#            rightSide = Vector( (colShape.entity.position[0] + (colShape.entity.dimensions[0]    ) ) // constants.TILESIZE , (colShape.entity.position[1] + (colShape.entity.dimensions[1] // 2) ) // constants.TILESIZE )
#            leftSide  = Vector( (colShape.entity.position[0]                                       ) // constants.TILESIZE , (colShape.entity.position[1] + (colShape.entity.dimensions[1] // 2) ) // constants.TILESIZE )
            
            if colShape.entity.velocity[1] < 0:                     #bewegt sich nach oben
                if map.getTileDangerousness(0, midTop[0] , midTop[1]) == True:
                    colShape.entity.setDead()
                elif map.getTileAccessibility(0, midTop[0] , midTop[1]) == True:
                    colShape.entity.mapColWhileMoveUp(midTop[0], midTop[1])
                    
            elif colShape.entity.velocity[1] > 0:                   #bewegt sich nach unten
                if map.getTileDangerousness(0, midBottom[0] , midBottom[1]) == True:
                    colShape.entity.setDead()
                elif map.getTileAccessibility(0, midBottom[0] , midBottom[1]) == True:
                    colShape.entity.mapColWhileMoveDown(midBottom[0], midBottom[1])
#                for x in range(max(0, bottom[0]), min(map.getDimensions()[0], (colShape.entity.position[0] + (colShape.entity.dimensions[0] // 2 - 1) / constants.TILESIZE + 1))):
#                    y = (colShape.entity.position[1] + (colShape.entity.dimensions[1]    ) ) // constants.TILESIZE -1 / constants.TILESIZE
#                    if map.getTileDangerousness(0, bottom[0], bottom[1]) == True:
#                        colShape.entity.setDead()
#                    if map.getTileAccessibility(0, x, y) == True:
#                        colShape.entity.mapColWhileMoveDown(x, y)
            
            if colShape.entity.velocity[0] > 0:                     #Bewegung nach rechts
                if map.getTileDangerousness(0, midRightSide[0], midRightSide[1]) == True:
                    colShape.entity.setDead()
                elif map.getTileAccessibility(0, midRightSide[0], midRightSide[1]) == True:
                    colShape.entity.mapColWhileMoveRight(midRightSide[0], midRightSide[1])                      
        
            elif colShape.entity.velocity[0] < 0:                   #Bewegung nach links
                if map.getTileDangerousness(0, midLeftSide[0], midLeftSide[1]) == True:
                    colShape.entity.setDead()
                elif map.getTileAccessibility(0, midLeftSide[0], midLeftSide[1]) == True:
                    colShape.entity.mapColWhileMoveLeft(midLeftSide[0], midLeftSide[1])
                    
            
    
    def checkPlayerEntityCollision(self):
        for shapeA in self.colShapeList:
            if shapeA.entity.type == 'player':
                for shapeB in self.colShapeList:
                    self.collisionBetween2ColShapes(shapeA, shapeB)
                return
    
    def collisionBetween2ColShapes(self, a ,b): #a=player b=enemy
        for absColRectA in a.getAbsoluteColRectList():
            for absColRectB in b.getAbsoluteColRectList():
                eventCode = self.collisionBetween2ColRects(absColRectA, absColRectB)
                if eventCode == 0:
                    pass
                elif eventCode == 1:
                    a.entity.colWin(b.entity)
                    b.entity.colLose(a.entity)
                elif eventCode == 2:
                    a.entity.colLose(b.entity)
                    b.entity.colWin(a.entity)

    def collisionBetween2ColRects(self, a, b):
        if a.absPos[0] > b.absPos[0] + b.dimensions[0]:      #collides nothing: nothing happens
            return 0
        elif a.absPos[0] + a.dimensions[0] < b.absPos[0]:    #collides nothing: nothing happens
            return 0
        if a.absPos[1] > b.absPos[1] + b.dimensions[1]:      #collides nothing: nothing happens
            return 0
        elif a.absPos[1] + a.dimensions[1] < b.absPos[1]:    #collides nothing: nothing happens
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
        
        
#rectListe : (Rect1,Rect2,...) 

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
        print "calcouterrect"
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
            self.posUpperLeft = Vector(posUpperLeft[0], posUpperLeft[1])    #pos from the upperLeft corner of the rect referring to the position of the entity(it's upperLeft corner
            self.dimensions = dimensions
            self.isBody = isBody    #if true, the entity is dead when it collides with the player
            self.isSpike = isSpike    #if true, the player is dead when it collides with the player
        
            self.absPos = self.colShape.entity.getPosition() + self.posUpperLeft    #absolute position in the whole level
    
        def getAbsoluteRect(self):
            return (self.absPos[0], self.absPos[1], self.dimensions[0], self.dimensions[1])
        
        def calcAbsPos(self):
            self.absPos = self.colShape.entity.getPosition() + self.posUpperLeft 
    