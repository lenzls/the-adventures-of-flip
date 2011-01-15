'''
Created on 27.09.2010

@author: simon
'''
from util.vector import Vector
from util import ressourceLoader, events
import util.util as util
from util.options import Options

class TriggerManager(object):
    # TODO:maybe move to another module
    def __init__(self):
        self.triggerQueue = []
        
    def addTrigger(self, trigger):
        self.triggerQueue.append(trigger)

    def isNewEvents(self):
        if len(self.triggerQueue) > 0:
            return True
        else:
            return False

    def next(self):
        next = self.triggerQueue[0]
        del(self.triggerQueue[0])
        return next

class Trigger(object):
    '''
    classdocs
    '''


    def __init__(self, position, map, infoTree, physics, activated):

        self.physics = physics
        self.map = map
        self.type = None
        self.activated = activated
        self.life = 0   # 0-100?!
        self.points = 0 #for highscore
        self.alive = True
        self.position = Vector(position[0],position[1])
        self.dimensions = [0,0]
        self.velocity = Vector(0,0)
        self.movespeed = None   #util.Vector(3,0)
        self.jumpspeed = None   #util.Vector(0,-13)

        self.jumplock = False
        self.jumpSound = None   #util.load_sound('jump.wav')

        self.colShape   = self.physics.createColShape(self)

        if self.activated:
            self.activate()

        self._loadInfo(infoTree)

    def activate(self):
        self.physics.addToColShapeList(self.colShape)

    def _loadInfo(self, infoTree):
        self.type = str(infoTree.getAttribute("type"))
        for infoNode in infoTree.childNodes:
            if infoNode.nodeName == "points":
                self.points = int(infoNode.firstChild.data)
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
        self.dimensions = self.colShape.getOuterDimensions()

    def getPosition(self):
        return self.position

    def update(self):

        self.position += self.velocity
        
        self.ki()

    def ki(self):
        pass

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

    def jump(self):
        if not self.jumplock:
            if Options.getOption("RESOLUTION"): self.jumpSound.play()
            self.jumplock = True
            self.velocity += self.jumpspeed

    def mapColWhileMoveUp(self, tilePos):
        pass

    def mapColWhileMoveDown(self, tilePos):
        pass

    def mapColWhileMoveRight(self, tilePos):
        pass

    def mapColWhileMoveLeft(self, tilePos):
        pass

    def colWin(self, enemy):
        print "Enemy win against:", enemy.type

    def colLose(self, enemy):
        print "Enemy loses against:", enemy.type
        events.Event().raiseCstmEvent(events.Event.ACTIVATETRIGGER, {"tObject":self})
        self.setDead()

    def setDead(self):
        self.alive = False

    def getVelocity(self):
        return self.velocity
    
    def getPoints(self):
        return self.points
    
    def action(self):
        '''
            should be overridden
        '''
        pass
    
class TmoveLeft(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        self.player = argDict["player"]
        
    def action(self):
        self.player.walkLeft()

class TmoveRight(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        self.player = argDict["player"]
        
    def action(self):
        self.player.walkRight()
        
class TmoveStop(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        self.player = argDict["player"]
        
    def action(self):
        self.player.walkStop()

class TmoveJump(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        self.player = argDict["player"]
        
    def action(self):
        self.player.jump()
        
class TcreateEntity(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        self.newEntity = argDict["newEntityObj"]
        self.lvlEntityList = argDict["entityList"]

    def action(self):
        self.lvlEntityList.append(self.newEntity)
        self.newEntity.activate()
        
class Tprinter(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        self.msg = argDict["msg"]

    def action(self):
        print self.msg
        
class TcutSceneStart(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        self.level = argDict["level"]

    def action(self):
        self.level.player.walkStop()
        self.level.startCutScene()
        
class TcutSceneEnd(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        self.level = argDict["level"]

    def action(self):
        self.level.endCutScene()
        
class TcreateBubble(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        self.msg = argDict["msg"]
        
    def action(self):
        events.Event().raiseCstmEvent(events.Event.NEWDIALOG, {"msg" : self.msg})

class TfinishLvl(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        
    def action(self):
        events.Event().raiseCstmEvent(events.Event.LEVELFINISHED, {})
        
class TcreateFade(Trigger):
    def __init__(self, position, map, infoTree, physics, activated, argDict):
        Trigger.__init__(self, position, map, infoTree, physics, activated)
        self.msg = argDict["msg"]
        self.fades = argDict["fades"]
        
    def action(self):
        self.fades.renderFade1(self.msg)
