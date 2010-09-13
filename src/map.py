'''
Created on 07.07.2009

@author: CaptnLenz
'''

import util.util as util
import xml.dom.minidom as dom


class Map(object):
    '''
    classdocs
    '''


    def __init__(self, mapFilePath):
        '''
        Constructor
        '''
        self.mapFilePath = mapFilePath
        self.entityFilePath = ''
        self.mapTitle = ''
        self.dimensions = [0,0]
        self.tiles = []
        self.bgLayers = []
        self.bgMusic = None
        self.mapGrid = []
        self.nextLevel = ''

        
        self._loadMapFile(self.mapFilePath)
        
    def _loadMapFile(self, mapFile):
        xmlMap = dom.parse('../data/level/'+mapFile)
        for node in xmlMap.firstChild.childNodes:
            #--------mapName--------
            if node.nodeName == 'name':
                self.mapTitle = node.firstChild.data.strip()        #mapTitle
                print self.mapTitle
            #--------mapDimensions--------
            elif node.nodeName == 'dimensions':
                for childNode in node.childNodes:
                    if childNode.nodeName == 'horizontal':
                        self.dimensions[0] = int(childNode.firstChild.data.strip())     #horiz dimension
                    elif childNode.nodeName == 'vertical':
                        self.dimensions[1] = int(childNode.firstChild.data.strip())     #vert dimension
            #--------mapTiles--------
            elif node.nodeName == 'tiles':
                self.tileCount = len([cNode for cNode in node.childNodes if cNode.nodeName == 'tile']) + 1       #Anzahl der tile-nodes  (+1)wegen leerem Teil auf Platz0
                for i in range(self.tileCount):       #laenge der tile-liste wird festgelegt
                    self.tiles.append(None)
                
                for childNode in node.childNodes:
                    if childNode.nodeName == 'tile':
                        tileIndex   =   int(childNode.getAttribute('index'))
                        for childChildNode in childNode.childNodes:
                            if childChildNode.nodeName == 'name':
                                tileName    =   str(childChildNode.firstChild.data.strip())  #tileName
                            elif childChildNode.nodeName == 'type':
                                tileType    =   str(childChildNode.firstChild.data.strip())  #tileType
                            elif childChildNode.nodeName == 'image':
                                tileImage    =   util.load_image(str(childChildNode.firstChild.data.strip()))  #tileImage
                            elif childChildNode.nodeName == 'accessibility':
                                if childChildNode.firstChild.data.strip() == 'true':
                                    tileAccessibility = True
                                elif childChildNode.firstChild.data.strip() == 'false':
                                    tileAccessibility = False  
                                #tileAccessibility
                            elif childChildNode.nodeName == 'dangerousness':
                                if childChildNode.firstChild.data.strip() == 'true':
                                    tileDangerousness = True
                                elif childChildNode.firstChild.data.strip() == 'false':
                                    tileDangerousness = False 
                                #tileDangerousness
                        
                        self.tiles[tileIndex] = (tileName, tileType, tileImage, tileAccessibility, tileDangerousness)
            #--------mapBackground--------
            elif node.nodeName == 'background':
                self.bgLayerCount = len([cNode for cNode in node.childNodes if cNode.nodeName == 'bgLayer'])      #Anzahl der bgLayer-nodes
                for i in range(self.bgLayerCount):       #laenge der bgLayer-liste wird festgelegt
                    self.bgLayers.append(None)
                    
                for childNode in node.childNodes:
                    if childNode.nodeName == 'bgLayer':
                        bgLayerIndex   =   int(childNode.getAttribute('index'))
                        for childChildNode in childNode.childNodes:
                            if childChildNode.nodeName == 'speed':
                                bgLayerSpeed    =   int(childChildNode.firstChild.data.strip())  #bgLayerSpeed
                            elif childChildNode.nodeName == 'image':
                                bgLayerImage    =   util.load_image(str(childChildNode.firstChild.data.strip()))  #bgLayerImage
                        self.bgLayers[bgLayerIndex] = (bgLayerSpeed, bgLayerImage, 0)   #0=position in px
            #--------mapMusic--------
            elif node.nodeName == 'music':      
                for childNode in node.childNodes:
                    if childNode.nodeName == 'backgroundTheme':
                        for childChildNode in childNode.childNodes:
                            if childChildNode.nodeName == 'soundFile':
                                self.bgMusic = util.load_sound(str(childChildNode.firstChild.data.strip()))
            #--------mapGrid--------
            elif node.nodeName == 'grid':
                self.gridLayerCount = len([cNode for cNode in node.childNodes if cNode.nodeName == 'gridLayer'])      #Anzahl der bgLayer-nodes
                for i in range(self.gridLayerCount):       #laenge der bgLayer-liste wird festgelegt
                    self.mapGrid.append([])
                    for j in range(self.dimensions[0]):
                        self.mapGrid[-1].append([])
                        for k in range(self.dimensions[1]):
                            self.mapGrid[-1][-1].append(None)
                
                
                for childNode in node.childNodes:
                    if childNode.nodeName == 'gridLayer':
                        gridLayerIndex    =   int(childNode.getAttribute('index'))
                        for childChildNode in childNode.childNodes:
                            if childChildNode.nodeName == 'column':
                                columnIndex = int(childChildNode.getAttribute('index'))
                                for childChildChildNode in childChildNode.childNodes:
                                    if childChildChildNode.nodeName == 'row':
                                        rowIndex = int(childChildChildNode.getAttribute('index'))                
                                        for childChildChildChildNode in childChildChildNode.childNodes:
                                            if childChildChildChildNode.nodeName == 'tileIndex':  
                                                self.mapGrid[gridLayerIndex][columnIndex][rowIndex] = int(childChildChildChildNode.firstChild.data.strip())     #mapGrid
            #--------entityFile--------
            elif node.nodeName == 'entityFile':
                self.entityFilePath = node.firstChild.data.strip()      #entityFile Path
            #--------mapNextLevel--------
            elif node.nodeName == 'nextLevel':
                self.nextLevel = node.firstChild.data.strip()          #next Map 
                
        #print self.mapTitle
        #print self.dimensions
        #print self.tiles
        #print self.bgLayers
        #print self.bgMusic
        #print self.mapGrid
        #print self.nextLevel
        
    def getDimensions(self):
        return self.dimensions
    
    def getMapGrid(self):
        return self.mapGrid
    
    def getTileName(self, layer, x, y):
        if self.mapGrid[layer][y][x] != 0:
            return self.tiles[self.mapGrid[layer][y][x]][0]
        else:
            return 'blank'
    
    def getTileType(self, layer, x, y):
        if self.mapGrid[layer][y][x] != 0:
            return self.tiles[self.mapGrid[layer][y][x]][1]
        else:
            return 'blank'
    
    def getTileImage(self, layer, x, y):
        if self.mapGrid[layer][y][x] != 0:
            return self.tiles[self.mapGrid[layer][y][x]][2]
        else:
            return 'blank'
    
    def getTileAccessibility(self, layer, x, y):
        #print'tileTest bei x:',x,'/',self.dimensions[0],' y:',y,'/',self.dimensions[1]
        #print'tileIndex:',self.mapGrid[layer][y][x]
        #print'tileType:',self.getTileType(layer, x, y)
        if x < 0 or x >= self.dimensions[0] or y < 0 or y >= self.dimensions[1]:
            return True
        elif self.mapGrid[layer][x][y] != 0:
            return self.tiles[self.mapGrid[layer][x][y]][3]
        else:
            return False
        
    def getTileDangerousness(self, layer, x, y):        
        
        if x < 0 or x >= self.dimensions[0] or y < 0 or y >= self.dimensions[1]:
            return True
        elif self.mapGrid[layer][x][y] != 0: 
            return self.tiles[self.mapGrid[layer][x][y]][4]
        else:
            return False
        
    def getMapInstance(self):
        return self
    
    
    
    