'''
Created on 07.07.2009

@author: CaptnLenz
'''

import util.constants as constants
from util.vector import Vector
import util.util as util
from util import ressourceLoader
from util.options import Options
import pygame
from util.ressourceLoader import RessourceLoader
from util.events import Event
from sound import SoundManager

class Player():

    def __init__(self, position, map, infoTree, physics, renderer, activated):

        self.renderer = renderer
        self.physics = physics
        self.map = map
        self.activated = activated
        self.type = 'player'
        self.life = 0 #0-100
        self.score = 0
        self.alive = True
        self.position = Vector(position[0],position[1])
        self.dimensions = [0,0]
        self.velocity = Vector(0,0)
        self.movespeed = None   #util.Vector(3,0)
        self.jumpspeed = None   #util.Vector(0,-13)

        self.woundingLock = False
        self.woundTimer = 0
        self.jumplock = False

        self.wLeft = False
        self.wRight = False

        self.sprite     = self.renderer.createSprite(self)
        self.colShape   = self.physics.createColShape(self)

        if self.activated:
            self.activate()

        self._loadInfo(infoTree)

        self.sprite.setAni('idle')
        
        #includes all objects, that collides at the moment with the player
        self.collideBusyList = []

    def getPosition(self):
        return self.position
    
    def activate(self):
        self.renderer.appendSpriteList(self.sprite)
        self.physics.addToColShapeList(self.colShape)

    def _loadInfo(self, infoTree):
        for infoNode in infoTree.childNodes:
            if infoNode.nodeName == 'type':
                pass
            elif infoNode.nodeName == "points":
                pass
            elif infoNode.nodeName == "life":
                self.life = int(infoNode.firstChild.data)
            elif infoNode.nodeName == 'movespeed':
                self.movespeed = Vector(int(infoNode.firstChild.data),0)
            elif infoNode.nodeName == 'jumpspeed':
                self.jumpspeed = Vector(0,int(infoNode.firstChild.data))
            elif infoNode.nodeName == 'jumpSound':
                for cNode in infoNode.childNodes:
                    if cNode.nodeName == "soundFile":
                        SoundManager.addSound("player_jump",str(cNode.firstChild.data))

            elif infoNode.nodeName == 'sprite':
                for animationNode in infoNode.childNodes:
                    if animationNode.nodeName == 'animation':
                        animationIndex = animationNode.getAttribute('index')
                        animationGraphics = []
                        for cNode in animationNode.childNodes:
                            if cNode.nodeName == 'type':
                                animationType = str(cNode.firstChild.data)
                            elif cNode.nodeName == "image":
                                for ccNode in cNode.childNodes:
                                    if ccNode.nodeName  == "graphic":
                                        animationGraphics.append(str(ccNode.firstChild.data))
                        self.sprite.addAnimation(animationType, animationGraphics)

            elif infoNode.nodeName == 'colShape':
                for colRectNode in infoNode.childNodes:
                    if colRectNode.nodeName == 'colRect':
                        posUpperLeft = [0,0]
                        dimensions   = [0,0]
                        isSpike      = None
                        isBody       = None
                        colRectIndex = int(colRectNode.getAttribute("index"))
                        for colRectInfoNode in colRectNode.childNodes:
                            if colRectInfoNode.nodeName == 'posUpperLeft':
                                for posUpperLeftNode in colRectInfoNode.childNodes:
                                    if posUpperLeftNode.nodeName == 'horizontal':
                                        posUpperLeft[0] = int(posUpperLeftNode.firstChild.data)
                                    elif posUpperLeftNode.nodeName == 'vertical':
                                        posUpperLeft[1] = int(posUpperLeftNode.firstChild.data)
                            elif colRectInfoNode.nodeName == 'dimensions':
                                for dimensionsNode in colRectInfoNode.childNodes:
                                    if dimensionsNode.nodeName == 'horizontal':
                                        dimensions[0] = int(dimensionsNode.firstChild.data)
                                    elif dimensionsNode.nodeName == 'vertical':
                                        dimensions[1] = int(dimensionsNode.firstChild.data)
                            elif colRectInfoNode.nodeName == 'isBody':
                                isBody  =   util.string2bool(colRectInfoNode.firstChild.data)
                            elif colRectInfoNode.nodeName == 'isSpike':
                                isSpike =   util.string2bool(colRectInfoNode.firstChild.data)
                        self.colShape.addRect(posUpperLeft, dimensions, isBody, isSpike)

        self._calcDimensions()

    def _calcDimensions(self):
        if self.sprite.getImageSize() == self.colShape.getOuterDimensions():
            self.dimensions = self.sprite.getImageSize()
        elif self.sprite.getImageSize() > self.colShape.getOuterDimensions():
            print"colRects of:%s are not big enough" % self
            print"colRects: %s graphics: %s" % (self.colShape.getOuterDimensions(),self.sprite.getImageSize())
            self.dimensions = self.sprite.getImageSize()
        elif self.sprite.getImageSize() < self.colShape.getOuterDimensions():
            print "colRects of:%s are too big" % self
            print"colRects: %s graphics: %s" % (self.colShape.getOuterDimensions(),self.sprite.getImageSize())

            self.dimensions = self.colShape.getOuterDimensions()
    
    def update(self):
        
        if self.velocity[1] < 15:
            self.velocity += self.physics.gravity
        self.position += self.velocity
        #check if better here or in renderer class
#        self.sprite.update()

        if self.woundingLock:
            self.woundTimer += 1
        if self.woundTimer >= 10:
            self.woundingLock = False
            self.woundTimer = 0

    def isAlive(self):
        return self.alive

    def walkRight(self, useWflag = True):
        if useWflag:
            self.wRight = True

        self.velocity.x = self.movespeed.x
        self.sprite.setAni('walkRight')

    def walkLeft(self, useWflag = True):
        if useWflag:
            self.wLeft = True
        
        self.velocity.x = -self.movespeed.x
        self.sprite.setAni('walkLeft')

    def walkStop(self, dir = 0):
        self.velocity.x = 0
        self.sprite.setAni('idle')
        if dir == 0:
            self.wLeft = False
            self.wRight = False
        elif dir > 0:
            self.wRight = False
            if self.wLeft:
                self.walkLeft(useWflag = False)
        elif dir < 0:
            self.wLeft = False
            if self.wRight:
                self.walkRight(useWflag = False)

    def getVelocity(self):
        return self.velocity

    def jump(self, ignoreJumpLock = False):
        if not self.jumplock or ignoreJumpLock:
            SoundManager.playSound("player_jump")
            self.jumplock = True
            self.velocity.y = self.jumpspeed.y

    def mapColWhileMoveUp(self, tilePos):
        oldPosition = self.position
        oldVelocity = self.velocity
        self.position = Vector(oldPosition[0],((tilePos.y + 1) * constants.TILESIZE) + 1)
        #when reaching the roof, instantly move downwards
        self.velocity.y = 0

    def mapColWhileMoveDown(self, tilePos):
        oldPosition = self.position
        oldVelocity = self.velocity
        self.jumplock = False
        self.position = Vector(oldPosition[0], (((tilePos.y * constants.TILESIZE)-1) - self.dimensions[1]))
        self.velocity = Vector(oldVelocity[0], 1)

    def mapColWhileMoveRight(self, tilePos):
        oldPosition = self.position
        oldVelocity = self.velocity
        self.position = Vector(((tilePos.x * constants.TILESIZE) - 1) - self.dimensions[0],oldPosition[1])

    def mapColWhileMoveLeft(self, tilePos):
        oldPosition = self.position
        oldVelocity = self.velocity
        self.position = Vector((((tilePos.x + 1) * constants.TILESIZE) + 1), oldPosition[1])

    def colWin(self, enemy):
        print "Player win against:", enemy.type
        self.score += enemy.getPoints()
        # no jumping after colliding with triggers!
        if not enemy.type.startswith("t_") and not enemy.type.startswith("coin"):
            self.jump(ignoreJumpLock = True)

    def colLose(self, enemy):
        print "Player loses against:", enemy.type
        if not self.woundingLock:
            #player wounded -> recoll
            self.woundingLock = True
            if enemy.velocity.x > 0:
                self.position.x += 10
            elif enemy.velocity.x < 0:
                self.position.x -= 10
            else:   
                if self.velocity.x > 0:
                    self.position.x -= 10
                elif self.velocity.x < 0:
                    self.position.x += 10
                else:
                    self.position.x += 0
            self.velocity.y = -5

            self.life -= 10
            if self.life <= 0:
                self.setDead()

    def setDead(self):
        pygame.time.wait(500)
        print 'TooooooooooooooooooooooooooooT'
        self.alive = False
        self.renderer.fades.renderDeathAnimation()
        from game import StateManager
        Event().raiseCstmEvent(Event.SWITCHSTATE, argDict={"state" : StateManager.MENUSTATE})
    
    def getScore(self):
        return self.score
    
    def getLife(self):
        return self.life
