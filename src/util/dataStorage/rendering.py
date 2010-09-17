'''
Created on 17.09.2010

@author: simon
'''

class Sprite(object):
    ''' respresents the graphical reprentation of one entity '''
    
    
    def __init__(self, entity, renderer):
        self.entity = entity
        self.renderer = renderer
        
        self.animationDict = {} #{type,Animation}

        self.curAni = "idle" #type of the cur ani

    def addAnimation(self, aniType, graphicFilenames):
        self.animationDict[aniType] = self.Animation(aniType, self.renderer, graphicFilenames)

    def setAni(self, aniType):
        self.curAni = aniType
        self.animationDict[self.curAni].reset()
    
    def getCurFrame(self):
        ''' @return: image-object of the current frame in the current animation '''
        return self.animationDict[self.curAni].getCurFrame()
    
    def update(self):
        self.animationDict[self.curAni].update()

    def renderGrid(self):
        ''' needed?! '''
        pass

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
        
        def __init__(self, type, renderer, initGraphicFilenames):
            self.type = ""
            self.imageDict = {} #{index,ImageObject}
            self.curFrameIndex = 0
            self.aniDelay = 3   #to switch less often(more realistic)
            self.aniDelayCounter = 0
            self.renderer = renderer
            
            index = 0
            for filename in initGraphicFilenames:
                self.addImage(index, filename)
                index += 1
    
        def getImageDict(self):
            return self.imageDict
        
        def addImage(self, index, path):
            ''' adds image object to animation '''
            
            self.imageDict[index] = Image(path, self.renderer)
            
        def reset(self):
            ''' resets the Animation '''
            
            self.curFrameIndex = 0;
            self.aniDelayCounter = 0
            
        def update(self):
            if self.aniDelayCounter < self.aniDelay:
                self.aniDelayCounter += 1
            else:
                if self.curFrameIndex + 1 == len(self.imageDict): #TODO: check if len(dict) works as intended
                    self.curFrameIndex = 0
                else:
                    self.curFrameIndex += 1
                self.aniDelayCounter = 0
    
        def getCurFrame(self):
            ''' @return: image-object of the current frame '''
            return self.imageDict[self.curFrameIndex]
        
class Image():
    ''' respresents a graphic '''
    
    def __init__(self, filename, renderer):
        self.dimensions = [0,0];
        self.renderer = renderer
 

        self.graphic = self.renderer.ressourceLoader.load_graphic(filename)

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