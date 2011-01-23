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

class Player():

    def __init__(self, position, map, infoTree, physics, renderer, activated):

        self.renderer = renderer
        self.physics = physics
        self.map = map
        self.activated = activated
        self.type = 'player'
        self.life = 0   # 0-100?!
        self.score = 0
        self.alive = True
        self.position = Vector(position[0],position[1])
        self.dimensions = [0,0]
        self.velocity = Vector(0,0)
        self.movespeed = None   #util.Vector(3,0)
        self.jumpspeed = None   #util.Vector(0,-13)

        self.jumplock = False
        self.jumpSound = None

        self.sprite     = self.renderer.createSprite(self)
        self.colShape   = self.physics.createColShape(self)

        if self.activated:
            self.activate()

        self._loadInfo(infoTree)

        self.sprite.setAni('idle')

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
                        self.jumpSound = ressourceLoader.RessourceLoader.load_sound(str(cNode.firstChild.data))

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

    def isAlive(self):
        return self.alive

    def walkRight(self):
        self.velocity += self.movespeed
        self.sprite.setAni('walkRight')

    def walkLeft(self):
        self.velocity -= self.movespeed
        self.sprite.setAni('walkLeft')

    def walkStop(self):
        self.velocity.x = 0
        self.sprite.setAni('idle')

    def getVelocity(self):
        return self.velocity

    def jump(self, ignoreJumpLock = False):
        if not self.jumplock or ignoreJumpLock:
            if Options.getOption("ISSOUND"): self.jumpSound.play()
            self.jumplock = True
            self.velocity += self.jumpspeed

    def mapColWhileMoveUp(self, tilePos):
        oldPosition = self.position
        oldVelocity = self.velocity
        self.position = Vector(oldPosition[0],((tilePos.y + 1) * constants.TILESIZE) + 1)

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
        if not enemy.type.startswith("t_"):
            self.jump(ignoreJumpLock = True)

    def colLose(self, enemy):
        print "Player loses against:", enemy.type
        self.setDead()

    def setDead(self):
        print 'TooooooooooooooooooooooooooooT'
        self.alive = False
        self.deathAnimation()
        from game import StateManager
        Event().raiseCstmEvent(Event.SWITCHSTATE, argDict={"state" : StateManager.MENUSTATE})
    
    def deathAnimation(self):
        olscreen = self.renderer.screen.copy()
        
        resolution = self.renderer.resolution
        halfX = resolution[0]/2
        halfY = resolution[1]/2
        for i in range(0,halfX,5):
            font = RessourceLoader.load_font('courier_new.ttf',i)
            writing = font.render("-1",1,(255,0,0),(0,0,0))
            
            areal00 = (0,0,halfX,halfY)
            areal01 = (0,halfY,halfX,halfY)
            areal10 = (halfX,0,halfX,halfY)
            areal11 = (halfX,halfY,halfX,halfY)
            self.renderer.screen.fill((0,0,0))
            self.renderer.screen.blit(olscreen, (-i,-i), area=areal00)
            self.renderer.screen.blit(olscreen, (-i,halfY+i), area=areal01)
            self.renderer.screen.blit(olscreen, (halfX+i,0-i), area=areal10)
            self.renderer.screen.blit(olscreen, (halfX+i,halfY+i), area=areal11)
            self.renderer.screen.blit(writing, (halfX-(writing.get_width()/2),halfY-(writing.get_height()/2)))
            pygame.display.update()
            pygame.time.wait(30)
        pygame.time.wait(1000)
    
    def getScore(self):
        return self.score
