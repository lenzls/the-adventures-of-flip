'''
Created on 07.07.2009

@author: CaptnLenz
'''

import pygame

import constants
import util

class Player():
    '''
    classdocs
    '''


    def __init__(self, position, map, infoTree, physics, renderer):
        '''
        Constructor
        '''        
        self.renderer = renderer
        self.physics = physics
        self.map = map
        self.type = 'player'
        self.life = 0
        self.isAlive = True
        self.position = util.Vector(position[0],position[1])
        self.dimensions = [0,0]
        self.velocity = util.Vector(0,0)
        self.movespeed = None   #util.Vector(3,0)
        self.jumpspeed = None   #util.Vector(0,-13)
        
        self.jumplock = False
        self.jumpSound = None   #util.load_sound('jump.wav')
        
        self.sprite     = self.renderer.createSprite(self)
        self.colShape   = self.physics.createColShape(self)
        
        self._loadInfo(infoTree)
        
        self.sprite.setAni('idle')

        
    def _loadInfo(self, infoTree):
        #animations
        for infoNode in infoTree.childNodes:
            if infoNode.nodeName == 'life':
                self.life = int(infoNode.firstChild.data)
            elif infoNode.nodeName == 'movespeed':
                self.movespeed = util.Vector(int(infoNode.firstChild.data),0)
            elif infoNode.nodeName == 'jumpspeed':
                self.jumpspeed = util.Vector(0,int(infoNode.firstChild.data))
            elif infoNode.nodeName == 'dimensions':
                for childNode in infoNode.childNodes:
                    if childNode.nodeName == 'horizontal':
                        self.dimensions[0] = int(childNode.firstChild.data)
                    elif childNode.nodeName == 'vertical':
                        self.dimensions[1] = int(childNode.firstChild.data)
            elif infoNode.nodeName == 'jumpSound':
                self.jumpSound = util.load_sound(str(infoNode.firstChild.data))
            elif infoNode.nodeName == 'sprites':
                for animationNode in infoNode.childNodes:
                    if animationNode.nodeName == 'animation':
                        animationType = animationNode.getAttribute('type')
                        animation = []
                        for spriteNode in animationNode.childNodes:
                            if spriteNode.nodeName == 'sprite':
                                for imageNode in spriteNode.childNodes:
                                    if imageNode.nodeName == 'image':
                                        animation.append(str(imageNode.firstChild.data))
                        self.sprite.addAnimation(animationType, animation)
                print 'ani Added'
            elif infoNode.nodeName == 'colShape':
                for colRectNode in infoNode.childNodes:
                    if colRectNode.nodeName == 'colRect':
                        posUpperLeft = [0,0]
                        dimensions   = [0,0]
                        isSpike      = None
                        isBody       = None
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
                                isBody  =   bool(colRectInfoNode.firstChild.data)
                            elif colRectInfoNode.nodeName == 'isSpike':
                                isSpike =   bool(colRectInfoNode.firstChild.data)
                        self.colShape.addRect(posUpperLeft, dimensions, isBody, isSpike)
                        
        print self.sprite.spriteList
        
    def update(self):
        if self.velocity[1] < 15:
            self.velocity += self.physics.gravity
        self.position += self.velocity
        self.sprite.update()
        
        self.renderer.updateCamera(self)
        
        #print 'playerAbsPos: ',self.position
        #print 'playerVel: ',self.velocity
        
    def getIsAlive(self):
        return self.isAlive
        
    def walkRight(self):
        self.velocity += self.movespeed
        self.sprite.setAni('walkRight')
        
    def walkLeft(self):
        self.velocity -= self.movespeed
        self.sprite.setAni('walkLeft')
    
    def walkStop(self):
        self.velocity.x = 0
        self.sprite.setAni('idle')
        
    def jump(self):
        """ What to do, if the space-key gets pressed """
        
        if not self.jumplock:
            self.jumpSound.play()
            self.jumplock = True
            self.velocity += self.jumpspeed
            
    def mapColWhileMoveUp(self, x, y):
        oldPosition = self.position
        oldVelocity = self.velocity
        self.position = util.Vector(oldPosition[0],((y + 1) * constants.TILESIZE) + 1)
    
    def mapColWhileMoveDown(self, x, y):
        oldPosition = self.position
        oldVelocity = self.velocity
        self.jumplock = False
        self.position = util.Vector(oldPosition[0], (((y * constants.TILESIZE)-1) - self.dimensions[1]))
        self.velocity = util.Vector(oldVelocity[0], 1)
    
    def mapColWhileMoveRight(self, x, y):
        print 'collision while right on: ',x,' ',y
        oldPosition = self.position
        oldVelocity = self.velocity
        self.position = util.Vector(((x * constants.TILESIZE) - 1) - self.dimensions[0],oldPosition[1])
    
    def mapColWhileMoveLeft(self, x, y):
        print 'collision while left on: ',x,' ',y
        oldPosition = self.position
        oldVelocity = self.velocity
        print 'old position: ',oldPosition
        self.position = util.Vector((((x + 1) * constants.TILESIZE) + 1), oldPosition[1])
        print 'new position: ',self.position
        
    def colWin(self, enemy):
        pass
    
    def colLose(self, enemy):
        pass
    
    def setDead(self):
        print 'TOoooooooooooooooooooooooooooT'
        self.isAlive = False
        
        