'''
Created on 17.09.2010

@author: simon
'''
from util import ressourceLoader


class Sprite(object):
    ''' respresents the graphical reprentation of one entity '''

    def __init__(self, entity):
        self.entity = entity

        #{type,Animation}
        self.animationDict = {}

        #type of the cur ani
        self.curAni = "idle"

    def addAnimation(self, aniType, graphicFilenames):
        self.animationDict[aniType] = self.Animation(aniType, graphicFilenames)

    def setAni(self, aniType):
        self.curAni = aniType
        self.animationDict[self.curAni].reset()

    def getCurFrame(self):
        ''' @return: image-object of the current frame in the current animation '''
        return self.animationDict[self.curAni].getCurFrame()

    def update(self):
        self.animationDict[self.curAni].update()

    def getImageSize(self):
        #TODO: smarter cecking and error handling
        graphicSize = None
        for ani in self.animationDict.values():
            for image in ani.getImageDict().values():
                if graphicSize == None:
                    graphicSize = image.getDimensions()
                else:
                    if graphicSize != image.getDimensions():
                        print("inconsistent graphic dimensions in Sprite of: ", self.entity)
                        return "error"
        return graphicSize

    class Animation():
        ''' respresents on animation of an entity '''

        def __init__(self, type, initGraphicFilenames):
            self.type = ""
            #{index,ImageObject}
            self.imageDict = {}
            self.curFrameIndex = 0
            #to switch less often(more realistic)
            self.aniDelay = 3
            self.aniDelayCounter = 0

            index = 0
            for filename in initGraphicFilenames:
                self.addImage(index, filename)
                index += 1

        def getImageDict(self):
            return self.imageDict

        def addImage(self, index, path):
            ''' adds image object to animation '''

            self.imageDict[index] = Image(path)
            
        def reset(self):
            ''' resets the Animation '''

            self.curFrameIndex = 0;
            self.aniDelayCounter = 0

        def update(self):
            if self.aniDelayCounter < self.aniDelay:
                self.aniDelayCounter += 1
            else:
                if self.curFrameIndex + 1 == len(self.imageDict):
                    self.curFrameIndex = 0
                else:
                    self.curFrameIndex += 1
                self.aniDelayCounter = 0

        def getCurFrame(self):
            ''' @return: image-object of the current frame '''

            return self.imageDict[self.curFrameIndex]

class Image():
    ''' respresents a graphic '''

    def __init__(self, filename):

        self.dimensions = [0,0];

        self.graphic = ressourceLoader.RessourceLoader().load_graphic(filename)

        self._calcDimensions()

    def _calcDimensions(self):
        self.dimensions = self.graphic.get_size()

    def getGraphic(self):
        ''' 
        @return: the real grafic(pygame surface)
        '''

        return self.graphic

    def getDimensions(self):
        return self.dimensions
