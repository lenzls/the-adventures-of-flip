'''
Created on 07.07.2009

@author: CaptnLenz
'''

from util.dataStorage.map import Tile, BgLayer
import xml.dom.minidom as minidom
from util import ressourceLoader

class Map(object):

    def __init__(self, mapFilePath):
        self.mapFilePath = mapFilePath
        self.entityFilePath = ''
        self.mapTitle = ''
        self.dimensions = [0,0]
        #{index, Tileobject}
        self.tiles = {}
        #{index, bglayer}
        self.bgLayers = {}
        self.bgMusic = None
        self.mapGrid = []

        self._loadMapFile(self.mapFilePath)

    def _loadMapFile(self, mapFile):
        xmlMapTree = minidom.parse('../data/level/'+mapFile)
        docRoot = xmlMapTree.firstChild

        for node in docRoot.childNodes:
            #--------mapName--------
            if node.nodeName == "name":
                self.mapTitle = node.firstChild.data.strip()

            #--------mapTiles--------
            elif node.nodeName == 'tiles':
                self.tileCount = len([cNode for cNode in node.childNodes if cNode.nodeName == 'tile'])
                for cNode in node.childNodes:
                    if cNode.nodeName == "tile":
                        tileIndex   =   int(cNode.getAttribute('index'))
                        for ccNode in cNode.childNodes:
                            if ccNode.nodeName == "name":
                                tileName    =   str(ccNode.firstChild.data.strip())
                            elif ccNode.nodeName == 'type':
                                tileType    =   str(ccNode.firstChild.data.strip())
                            elif ccNode.nodeName == 'graphic':
                                tileGraphic    =   str(ccNode.firstChild.data.strip())
                            elif ccNode.nodeName == 'accessibility':
                                if ccNode.firstChild.data.strip() == 'true':
                                    tileAccessibility = True
                                elif ccNode.firstChild.data.strip() == 'false':
                                    tileAccessibility = False
                            elif ccNode.nodeName == 'dangerousness':
                                if ccNode.firstChild.data.strip() == 'true':
                                    tileDangerousness = True
                                elif ccNode.firstChild.data.strip() == 'false':
                                    tileDangerousness = False
                        self.tiles[tileIndex] = Tile(tileName, tileType, tileGraphic, tileAccessibility, tileDangerousness)
            #--------mapBackground--------
            elif node.nodeName == 'background':
                self.bgLayerCount = len([cNode for cNode in node.childNodes if cNode.nodeName == 'bgLayer'])      #Anzahl der bgLayer-nodes

                for cNode in node.childNodes:
                    if cNode.nodeName == 'bgLayer':
                        bgLayerIndex   =   int(cNode.getAttribute('index'))
                        for ccNode in cNode.childNodes:
                            if ccNode.nodeName == 'speed':
                                bgLayerSpeed    =   int(ccNode.firstChild.data.strip())  #bgLayerSpeed
                            elif ccNode.nodeName == 'graphic':
                                bgLayerGraphic    =   str(ccNode.firstChild.data.strip())  #bgLayerImage

                        self.bgLayers[bgLayerIndex] = BgLayer(bgLayerSpeed, bgLayerGraphic)   #0=position in px

            #--------mapMusic--------
            elif node.nodeName == 'music':      
                for cNode in node.childNodes:
                    if cNode.nodeName == 'backgroundTheme':
                        for ccNode in cNode.childNodes:
                            if ccNode.nodeName == 'soundFile':
                                self.bgMusic = ressourceLoader.RessourceLoader().load_sound(str(ccNode.firstChild.data.strip()))

            #--------mapGrid--------
            elif node.nodeName == 'grid':
                self.gridLayerCount = len([cNode for cNode in node.childNodes if cNode.nodeName == 'gridLayer'])      #Anzahl der gridlayer-nodes                

                self.dimensions = [0,0] #start counting from 1 not 0!!
                #TODO: filter NOT rectangular grids and raise exception!

                for cNode in node.childNodes:
                    if cNode.nodeName == 'gridLayer':
                        gridLayerIndex    =   int(cNode.getAttribute('index'))

                        self.mapGrid.append([])

                        for colNode in cNode.childNodes:
                            if colNode.nodeName == 'column':
                                columnIndex = int(colNode.getAttribute('index'))

                                if columnIndex+1 > self.dimensions[0]: self.dimensions[0] = columnIndex+1

                                self.mapGrid[gridLayerIndex].append([])

                                for rowNode in colNode.childNodes:
                                    if rowNode.nodeName == 'row':
                                        rowIndex = int(rowNode.getAttribute('index'))

                                        if rowIndex+1 > self.dimensions[1]: self.dimensions[1] = rowIndex+1

                                        self.mapGrid[gridLayerIndex][columnIndex].append(None)                
                                        for tileIndex in rowNode.childNodes:
                                            if tileIndex.nodeName == 'tileIndex':  
                                                self.mapGrid[gridLayerIndex][columnIndex][rowIndex] = int(tileIndex.firstChild.data.strip())     #mapGrid
            #--------entityFile--------
            elif node.nodeName == 'entityFile':
                self.entityFilePath = node.firstChild.data.strip()      #entityFile Path

    def getDimensions(self):
        return self.dimensions

    def getMapGrid(self):
        return self.mapGrid

    def getTileName(self, layer, x, y):
        if self.mapGrid[layer][x][y] != 0:
            return self.tiles[self.mapGrid[layer][x][y]].getName()
        else:
            return 'blank'

    def getTileType(self, layer, x, y):
        if self.mapGrid[layer][x][y] != 0:
            return self.tiles[self.mapGrid[layer][x][y]].getType()
        else:
            return 'blank'

    def getTileGraphic(self, layer, x, y):
        if self.mapGrid[layer][x][y] != 0:
            return self.tiles[self.mapGrid[layer][x][y]].getGraphic()
        else:
            return 'blank'

    def getTileAccessibility(self, layer, x, y):
        if x < 0 or x >= self.dimensions[0] or y < 0 or y >= self.dimensions[1]:
            return True
        elif self.mapGrid[layer][x][y] != 0:
            return self.tiles[self.mapGrid[layer][x][y]].getAccessibility()
        else:
            return False

    def getTileDangerousness(self, layer, x, y):
        if x < 0 or x >= self.dimensions[0] or y < 0 or y >= self.dimensions[1]:
            print "Entity falls out of the map!"
            return True
        elif self.mapGrid[layer][x][y] != 0: 
            return self.tiles[self.mapGrid[layer][x][y]].getDangerousness
        else:
            return False

    def getMapInstance(self):
        return self
