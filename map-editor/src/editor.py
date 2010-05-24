import sys
sys.path.insert(0, '..')


import pygame
import constants
import util
import os
import xml.dom.minidom as dom
from pgu import gui
from pgu import tilevid


class MapEditor():
    def __init__(self):
        self.firstPress = False
        self.secPress = False
        
        self.firstVar = ()
        self.secVar = ()
                            
        #map Vars
        self.name = "iii"
        self.dimensions = [0,0]
        self.tiles = {}
        #background (wird manuell eingefuegt erstmal
        self.music = ""
        self.grid = []
        self.entityFile = ""
        self.nextLevel = ""
        #END map Vars
        
        self.cur_Tile = 1
        self.camera = util.Vector(0,0)
     
        
        self.screen = pygame.display.set_mode((1280,720))
        
        self.mapSurface = pygame.Surface((930,570))

        self.layerMenuBG = pygame.Surface((150,720))
        self.layerMenuBG.fill((0,200,200))
        self.tilesMenuBG = pygame.Surface((200,720))
        self.tilesMenuBG.fill((200,200,0))
        self.topMenuBG = pygame.Surface((930,150))
        self.topMenuBG.fill((155,0,155))
        
        
        
        self.editApp = gui.App()
        self.editApp.connect(gui.QUIT,self.editApp.quit,None)
        
        self.Bt_applyOpt = gui.Button("Apply Options")
        self.Bt_applyOpt.connect(gui.CLICK, self.BUTTONapplyOpt,None)
        self.Bt_newMap = gui.Button("New Map")
        self.Bt_newMap.connect(gui.CLICK, self.BUTTONnewMap, None)
        self.Bt_loadMap = gui.Button("Load Map")
        self.Bt_loadMap.connect(gui.CLICK, self.BUTTONloadMap, None)
        self.Bt_saveMap = gui.Button("Save Map")
        self.Bt_saveMap.connect(gui.CLICK, self.BUTTONsaveMap, None)
        
        
        self.Lb_Layer_Topic = gui.Label("Layer-Menu")
        self.Lb_layer1 = gui.Label("Layer 1 visible?: ")
        self.Lb_layer2 = gui.Label("Layer 2 visible?: ")
        self.Lb_Tiles_Topic = gui.Label("Tiles-Menu")
        self.Lb_Tiles = gui.Label("Tiles: ")
        self.Lb_curT_index = gui.Label("Index: ")
        self.Lb_curT_name = gui.Label("Name: ")
        self.Lb_curT_type = gui.Label("Type: ")
        self.Lb_curT_image = gui.Label("Image: ")
        self.Lb_curT_access = gui.Label("Access.: ")
        self.Lb_curT_danger = gui.Label("Dangerous.: ")
        self.Lb_map_name = gui.Label("Map-Name: ")
        self.Lb_map_dimH = gui.Label("dimH: ")
        self.Lb_map_dimV = gui.Label("dimV: ")
        self.Lb_map_bgMusic = gui.Label("bgMusic: ")
        self.Lb_map_entityFile = gui.Label("entityFile: ")
        self.Lb_map_nextLvl = gui.Label("nextLvl: ")
        
        
        self.Inp_map_name = gui.Input(size=8)
        self.Inp_map_dimH = gui.Input(size=8)
        self.Inp_map_dimV = gui.Input(size=8)
        self.Inp_map_bgMusic = gui.Input(size=8)
        self.Inp_map_entityFile = gui.Input(size=8)
        self.Inp_map_nextLvl = gui.Input(size=8)
        
        
        self.Se_Tile_Select = gui.Select(value=1)
        #Selectbos Tilelabels
        for i in range(len(self.tiles)):
            self.Se_Tile_Select.add(gui.Label(self.tiles[i][0]),value=i)

        self.Sw_layer1_vis = gui.Switch(True)
        self.Sw_layer2_vis = gui.Switch(True)
        
        
        self.container = gui.Container(width=1280, height=720)   #muss man schauen ob in der mitte dann noch pygame fenster aktiv ist
        
        
        self.layerTable = gui.Table(width=150,height=720,align=-1)
        self.tilesTable = gui.Table(width=200,height=720,align= 1)
        self.topTable = gui.Table(width=30)
        
        
        
        
        
        self.container.add(self.layerTable, 0, 0)
        self.container.add(self.tilesTable, 1080,0)
        self.container.add(self.topTable, 150,0)
        
        
        
        self.editApp.init(self.container, self.screen)
        self.running = True
        
        self.initNewMap()

        self.loadMap()
    
    def loadMap(self):
        
        xmlMap = dom.parse('./data/save.xml')
        for node in xmlMap.firstChild.childNodes:
            #--------mapName--------
            if node.nodeName == 'name':
                self.name = node.firstChild.data.strip()        #mapTitle

            #--------mapDimensions--------
            elif node.nodeName == 'dimensions':
                for childNode in node.childNodes:
                    if childNode.nodeName == 'horizontal':
                        self.dimensions[0] = int(childNode.firstChild.data.strip())     #horiz dimension
                    elif childNode.nodeName == 'vertical':
                        self.dimensions[1] = int(childNode.firstChild.data.strip())     #vert dimension
            #--------mapTiles--------
            elif node.nodeName == 'tiles':
                #tileCount = len([cNode for cNode in node.childNodes if cNode.nodeName == 'tile']) + 1       #Anzahl der tile-nodes  (+1)wegen leerem Teil auf Platz0
                #for i in range(tileCount):       #laenge der tile-liste wird festgelegt
                #    tiles.append(None)
                self.tiles.clear()
                self.tiles[0] = ["blank","blank","blank.png","false","false"]
                for childNode in node.childNodes:
                    if childNode.nodeName == 'tile':
                        tileIndex   =   int(childNode.getAttribute('index'))
                        for childChildNode in childNode.childNodes:
                            if childChildNode.nodeName == 'name':
                                tileName    =   str(childChildNode.firstChild.data.strip())  #tileName
                            elif childChildNode.nodeName == 'type':
                                tileType    =   str(childChildNode.firstChild.data.strip())  #tileType
                            elif childChildNode.nodeName == 'image':
                                tileImage    =   str(childChildNode.firstChild.data.strip())  #tileImage
                            elif childChildNode.nodeName == 'accessibility':
                                tileAccessibility = childChildNode.firstChild.data.strip()
                            elif childChildNode.nodeName == 'dangerousness':
                                tileDangerousness = childChildNode.firstChild.data.strip()
                        
                        self.tiles[tileIndex] = (tileName, tileType, tileImage, tileAccessibility, tileDangerousness)

            #--------mapBackground--------
            #elif node.nodeName == 'background':
            #    self.bgLayerCount = len([cNode for cNode in node.childNodes if cNode.nodeName == 'bgLayer'])      #Anzahl der bgLayer-nodes
            #    for i in range(self.bgLayerCount):       #laenge der bgLayer-liste wird festgelegt
            #        self.bgLayers.append(None)
            #        
            #    for childNode in node.childNodes:
            #        if childNode.nodeName == 'bgLayer':
            #            bgLayerIndex   =   int(childNode.getAttribute('index'))
            #            for childChildNode in childNode.childNodes:
            #                if childChildNode.nodeName == 'speed':
            #                    bgLayerSpeed    =   int(childChildNode.firstChild.data)  #bgLayerSpeed
            #                elif childChildNode.nodeName == 'image':
            #                    bgLayerImage    =   util.load_image(str(childChildNode.firstChild.data))  #bgLayerImage
            #            self.bgLayers[bgLayerIndex] = (bgLayerSpeed, bgLayerImage, 0)   #0=position in px
            #--------mapMusic--------
            elif node.nodeName == 'music':      
                for childNode in node.childNodes:
                    if childNode.nodeName == 'backgroundTheme':
                        for childChildNode in childNode.childNodes:
                            if childChildNode.nodeName == 'soundFile':
                                self.music = str(childChildNode.firstChild.data.strip())
            #--------mapGrid--------
            elif node.nodeName == 'grid':
                self.grid = []
                gridLayerCount = len([cNode for cNode in node.childNodes if cNode.nodeName == 'gridLayer'])      #Anzahl der bgLayer-nodes
                for i in range(gridLayerCount):       #laenge der bgLayer-liste wird festgelegt
                    self.grid.append([])
                    for j in range(self.dimensions[0]):
                        self.grid[-1].append([])
                        for k in range(self.dimensions[1]):
                            self.grid[-1][-1].append(None)
                
                
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
                                                self.grid[gridLayerIndex][columnIndex][rowIndex] = int(childChildChildChildNode.firstChild.data.strip())     #mapGrid
            #--------entityFile--------
            elif node.nodeName == 'entityFile':
                self.entityFile = node.firstChild.data.strip()      #entityFile Path
            #--------mapNextLevel--------
            
            elif node.nodeName == 'nextLevel':
                self.nextLevel = node.firstChild.data.strip()           #next Map 

        self.Se_Tile_Select.clear()
        self.Se_Tile_Select = gui.Select(value=1)
        #Selectbos Tilelabels

        for i in range(len(self.tiles)):
            self.Se_Tile_Select.add(gui.Label(self.tiles[i][0]),value=i)
        
        self.Inp_map_name = gui.Input(value=self.name,size=8)    
        self.Inp_map_dimH = gui.Input(value=self.dimensions[0],size=8)
        self.Inp_map_dimV = gui.Input(value=self.dimensions[1],size=8)
        self.Inp_map_bgMusic = gui.Input(value=self.music,size=8)
        self.Inp_map_entityFile = gui.Input(value=self.entityFile,size=8)
        self.Inp_map_nextLevel = gui.Input(value=self.nextLevel,size=8)
            
    def initNewMap(self,tilesFromIni=True): #arg ob ini oder xml!
        if tilesFromIni == True:
            self.tiles.clear()
            file = open('./tiles.ini',"r")
            
            tileIndex = 0
            tileName = ""
            tileType = ""
            tileImage = ""
            tileAccessibility = True
            tileDangerousness = True
            
            self.tiles[0] = ["blank","blank","blank.png","false","false"]
            for line in file:
                if line.strip().startswith('index') == True:
                    (category,ind) = line.strip().split('=')
                    tileIndex = int(ind)
                    self.tiles[tileIndex] = [tileName,tileType,tileImage,tileAccessibility,tileDangerousness]
                elif line.strip().startswith('name') == True:
                    (category,nam) = line.strip().split('=')
                    tileName = nam
                    self.tiles[tileIndex][0] = tileName            
                elif line.strip().startswith('type') == True:
                    (category,typ) = line.strip().split('=')
                    tileType = typ
                    self.tiles[tileIndex][1] = tileType
                elif line.strip().startswith('image') == True:
                    (category,img) = line.strip().split('=')
                    tileImage = img
                    self.tiles[tileIndex][2] = tileImage
                elif line.strip().startswith('accessibility') == True:
                    (category,acc) = line.strip().split('=')
                    tileAccessibility = acc
                    self.tiles[tileIndex][3] = tileAccessibility
                elif line.strip().startswith('dangerousness') == True:
                    (category,dan) = line.strip().split('=')
                    tileDangerousness = dan
                    self.tiles[tileIndex][4] = tileDangerousness
                else:
                    print 'ERROR:Fehler in der Highscore-Datei'
                    sys.exit()
            file.close()
            
            self.name = "NewMap"
            self.dimensions = [10,10]
            #background (wird manuell eingefuegt erstmal
            self.music = ""
            self.grid = []
            self.entityFile = ""
            self.nextLevel = ""
            
            self.Se_Tile_Select.clear()
            self.Se_Tile_Select = gui.Select(value=1)
            #Selectbos Tilelabels

            for i in range(len(self.tiles)):
                self.Se_Tile_Select.add(gui.Label(self.tiles[i][0]),value=i)
            
            self.Inp_map_name = gui.Input(value=self.name,size=8)    
            self.Inp_map_dimH = gui.Input(value=self.dimensions[0],size=8)
            self.Inp_map_dimV = gui.Input(value=self.dimensions[1],size=8)
            self.Inp_map_bgMusic = gui.Input(value=self.music,size=8)
            self.Inp_map_entityFile = gui.Input(value=self.entityFile,size=8)
            self.Inp_map_nextLevel = gui.Input(value=self.nextLevel,size=8)

    def BUTTONloadMap(self,arg):
        self.loadMap()

    def BUTTONapplyOpt(self,arg):
        '''sollte alles gehn bis auf zuerst x erhoehen und dann y verringern'''

        self.name = self.Inp_map_name.value
        newDimensions = (int(self.Inp_map_dimH.value), int(self.Inp_map_dimV.value))
        
        #x Richtung
        if newDimensions[0] > self.dimensions[0]:   #neue koords groesser alte koords            
            for i in range(0,newDimensions[0]-self.dimensions[0]):
                standardCol = []
                for j in range(0,self.dimensions[1]):
                    standardCol.append(0)
                self.grid[0].append(standardCol)
                self.grid[1].append(standardCol)

        elif newDimensions[0] < self.dimensions[0]: #neue koords kleiner alte koords
            for i in range(self.dimensions[0]-1, newDimensions[0]-1,-1):
                self.grid[0].pop(i)
                self.grid[1].pop(i)
        self.dimensions[0] = newDimensions[0]
        
        #y-Richtung
        if newDimensions[1] > self.dimensions[1]:   #neue koords groesser alte koords
            for x in range(0,self.dimensions[0]):
                for i in range(self.dimensions[1], newDimensions[1]):
                    self.grid[0][x].append(0)
                    self.grid[1][x].append(0)
        elif newDimensions[1] < self.dimensions[1]: #neue koords kleiner alte koords
            for x in range(0,self.dimensions[0]):
                for i in range(self.dimensions[1]-1, newDimensions[1]-1, -1):
                    self.grid[0][x].pop(i)
                    self.grid[1][x].pop(i)

   
        
        self.dimensions[1] = newDimensions[1]
        
        self.music = str(self.Inp_map_bgMusic.value)
        self.entityFile = str(self.Inp_map_entityFile.value)
        self.nextLevel = str(self.Inp_map_nextLevel.value)
            
    def BUTTONnewMap(self,arg):
        self.initNewMap()
        
    def BUTTONsaveMap(self,arg):
        print "saveMap!!"
        
        # Dokument erzeugen
        implement = dom.getDOMImplementation()
        doc = implement.createDocument(None, "Map", None)
        
        #Name
        nameElement = doc.createElement("name")
        nameText = doc.createTextNode(self.name)
        nameElement.appendChild(nameText)
        
        #Dimensionen
        dimensionsElement = doc.createElement("dimensions")
        dimensionsHorizontalElement = doc.createElement("horizontal")
        dimensionsVerticalElement = doc.createElement("vertical")
        dimensionsHorizontalText = doc.createTextNode(str(self.dimensions[0]))
        dimensionsVerticalText = doc.createTextNode(str(self.dimensions[1]))
        dimensionsHorizontalElement.appendChild(dimensionsHorizontalText)
        dimensionsVerticalElement.appendChild(dimensionsVerticalText)
        dimensionsElement.appendChild(dimensionsHorizontalElement)
        dimensionsElement.appendChild(dimensionsVerticalElement)
        
        #Tiles
        tilesElement = doc.createElement("tiles")
        for i in range(1,len(self.tiles)):
            tileElement = doc.createElement("tile")
            tileElement.setAttribute('index',str(i))
            
            tileNameElement = doc.createElement("name")
            tileTypeElement = doc.createElement("type")
            tileImageElement = doc.createElement("image")
            tileAccessibilityElement = doc.createElement("accessibility")
            tileDangerousnessElement = doc.createElement("dangerousness")
            
            tileNameText = doc.createTextNode(str(self.tiles[i][0]))
            tileTypeText = doc.createTextNode(str(self.tiles[i][1]))
            tileImageText = doc.createTextNode(str(self.tiles[i][2]))
            tileAccessibilityText = doc.createTextNode(str(self.tiles[i][3]))
            tileDangerousnessText = doc.createTextNode(str(self.tiles[i][4]))
            
            tileNameElement.appendChild(tileNameText)
            tileTypeElement.appendChild(tileTypeText)
            tileImageElement.appendChild(tileImageText)
            tileAccessibilityElement.appendChild(tileAccessibilityText)
            tileDangerousnessElement.appendChild(tileDangerousnessText)
            
            tileElement.appendChild(tileNameElement)
            tileElement.appendChild(tileTypeElement)
            tileElement.appendChild(tileImageElement)
            tileElement.appendChild(tileAccessibilityElement)
            tileElement.appendChild(tileDangerousnessElement)
            
            tilesElement.appendChild(tileElement)
        
        #BackgroundLayer
        backgroundElement = doc.createElement("background")
        for i in range(0,len(self.tiles)):
            bgLayerElement = doc.createElement("bgLayer")
            bgLayerElement.setAttribute('index',str(i))
            
            bgLayerSpeedElement = doc.createElement("speed")
            bgLayerImageElement = doc.createElement("image")
            
            if i == 0:
                bgLayerSpeedText = doc.createTextNode('0')
            else:
                bgLayerSpeedText = doc.createTextNode(str(4-i))
            bgLayerImageText = doc.createTextNode("bg_test_"+str(i)+".png")
            
            bgLayerSpeedElement.appendChild(bgLayerSpeedText)
            bgLayerImageElement.appendChild(bgLayerImageText)
            
            bgLayerElement.appendChild(bgLayerSpeedElement)
            bgLayerElement.appendChild(bgLayerImageElement)
            
            backgroundElement.appendChild(bgLayerElement)
        
        #Music
        musicElement = doc.createElement("music")
        musicBackgroundThemeElement = doc.createElement("backgroundTheme")
        musicBackgroundThemeSoundFileElement = doc.createElement("soundFile")
        musicBackgroundThemeSoundFileText = doc.createTextNode(self.music)
        musicElement.appendChild(musicBackgroundThemeElement)
        musicBackgroundThemeElement.appendChild(musicBackgroundThemeSoundFileElement)
        musicBackgroundThemeSoundFileElement.appendChild(musicBackgroundThemeSoundFileText)        
        
        #Grid
        gridElement = doc.createElement("grid")
        for i in range(0,len(self.grid)):
            gridLayerElement = doc.createElement("gridLayer")
            gridLayerElement.setAttribute('index',str(i))
            
            for j in range(0,len(self.grid[i])):
                gridLayerColumnElement = doc.createElement("column")
                gridLayerColumnElement.setAttribute('index',str(j))
                
                for k in range(0,len(self.grid[i][j])):
                    gridLayerColumnRowElement = doc.createElement("row")
                    gridLayerColumnRowElement.setAttribute('index',str(k))
                    
                    gridLayerColumnRowTileIndexElement = doc.createElement("tileIndex")
                    gridLayerColumnRowTileIndexText = doc.createTextNode(str(self.grid[i][j][k]))
                    gridLayerColumnRowTileIndexElement.appendChild(gridLayerColumnRowTileIndexText)
                    gridLayerColumnRowElement.appendChild(gridLayerColumnRowTileIndexElement)
                    
                    gridLayerColumnElement.appendChild(gridLayerColumnRowElement)
                    
                gridLayerElement.appendChild(gridLayerColumnElement)
            
            gridElement.appendChild(gridLayerElement)
            
        #entityFile
        entityFileElement = doc.createElement("entityFile")
        entityFileText = doc.createTextNode(self.entityFile)
        entityFileElement.appendChild(entityFileText)
        
        #nextLvl
        nextLevelElement = doc.createElement("nextLevel")
        nextLevelText = doc.createTextNode(self.nextLevel)
        nextLevelElement.appendChild(nextLevelText)
        
        # Child an Dokument anhaengen
        doc.documentElement.appendChild(nameElement)
        doc.documentElement.appendChild(dimensionsElement)
        doc.documentElement.appendChild(tilesElement)
        doc.documentElement.appendChild(backgroundElement)
        doc.documentElement.appendChild(musicElement)
        doc.documentElement.appendChild(gridElement)
        doc.documentElement.appendChild(entityFileElement)
        doc.documentElement.appendChild(nextLevelElement)

        # Ausgeben
        datei = open(os.path.join('.','data',"save.xml"), "w")
        doc.writexml(datei, "\n", "  ")
        datei.close()

    def renderMap(self):   
        if self.layerVis[0] == True:
            for y in range(max(self.camera[1] / constants.TILESIZE, 0), min(self.dimensions[1], (self.camera[1] + constants.RESOLUTION[1]) / constants.TILESIZE + 1)):
                for x in range(max(self.camera[0] / constants.TILESIZE, 0), min(self.dimensions[0], (self.camera[0] + constants.RESOLUTION[0]) / constants.TILESIZE + 1)):
                    #print 'dim X: ',self.dimensions[0],'=',len(self.grid[0])
                    #print 'dim Y: ',self.dimensions[1],'=',len(self.grid[0][0])
                    #print 'x: ',x,'y: ',y
                    if self.grid[0][x][y] != 0:
                        self.mapSurface.blit(util.load_image(self.tiles[self.grid[0][x][y]][2]), (x*constants.TILESIZE - self.camera[0],y*constants.TILESIZE - self.camera[1]))
        if self.layerVis[1] == True:
            for y in range(max(self.camera[1] / constants.TILESIZE, 0), min(self.dimensions[1], (self.camera[1] + constants.RESOLUTION[1]) / constants.TILESIZE + 1)):
                for x in range(max(self.camera[0] / constants.TILESIZE, 0), min(self.dimensions[0], (self.camera[0] + constants.RESOLUTION[0]) / constants.TILESIZE + 1)):
                    if self.grid[1][x][y] != 0:
                        self.mapSurface.blit(util.load_image(self.tiles[self.grid[1][x][y]][2]), (x*constants.TILESIZE - self.camera[0],y*constants.TILESIZE - self.camera[1]))
        
    def replaceTile(self, screenPos):
        if screenPos[0] >= 150 and screenPos[0] <= 1080:
            if screenPos[1] >= 150 and screenPos[1] <= 720:
                mapSurfacePos = ((screenPos[0]-150)-self.camera[0],(screenPos[1]-150)-self.camera[1])
                if mapSurfacePos[0] >= 0 and mapSurfacePos[0] <= self.dimensions[0]*constants.TILESIZE:
                    if mapSurfacePos[1] >= 0 and mapSurfacePos[1] <= self.dimensions[1]*constants.TILESIZE:
                        tilePosition = self.getCurTilePos(mapSurfacePos)
                        
                        if self.layerVis[0] and self.layerVis[1]:
                            topLayer = 1
                        elif self.layerVis[0] and not self.layerVis[1]:
                            topLayer = 0
                        elif not self.layerVis[0] and self.layerVis[1]:
                            topLayer = 1
                        elif not self.layerVis[0] and not self.layerVis[1]:
                            return
                        print 'prev: ',self.grid[topLayer][tilePosition[0]][tilePosition[1]]
                        self.grid[topLayer][tilePosition[0]][tilePosition[1]] = self.cur_Tile
                        print 'replace at: ',topLayer,' ',tilePosition[0],' ',tilePosition[1]
                        print 'after: ',self.grid[topLayer][tilePosition[0]][tilePosition[1]]
                        print self.grid[0]
                        print self.grid[1]
               
    def getCurTilePos(self, surfacePos):    #returns current Tile after click
        curTilePos = (surfacePos[0]/constants.TILESIZE,surfacePos[1]/constants.TILESIZE)
        return curTilePos

    def start(self):
        while self.running:
            #update
            self.editApp.update(self.screen)
            
            self.cur_Tile = self.Se_Tile_Select.value
            
            self.layerVis = [self.Sw_layer1_vis.value, self.Sw_layer2_vis.value]
            
            #update linke Seite
            self.layerTable.clear()
            self.layerTable.td(self.Lb_Layer_Topic,0,0,collspan=2)
            self.layerTable.td(self.Lb_layer1,0,1)
            self.layerTable.td(self.Sw_layer1_vis, 1, 1)
            self.layerTable.td(self.Lb_layer2,0,2)
            self.layerTable.td(self.Sw_layer2_vis, 1, 2)
            #---------
            
            #update rechte Seite (wg. TileBild
            self.tilesTable.clear()
            self.tilesTable.td(self.Lb_Tiles_Topic,0,0,colspan=2)
            self.tilesTable.td(self.Lb_curT_index,0,1)
            self.tilesTable.td(gui.Label(str(self.cur_Tile)),1,1)
            self.tilesTable.td(self.Lb_curT_name,0,2)
            self.tilesTable.td(gui.Label(self.tiles[self.cur_Tile][0]),1,2)
            self.tilesTable.td(self.Lb_curT_type,0,3)
            self.tilesTable.td(gui.Label(self.tiles[self.cur_Tile][1]),1,3)
            self.tilesTable.td(self.Lb_curT_image,0,4)
            self.tilesTable.td(gui.Image(os.path.join('.', 'data',  self.tiles[self.cur_Tile][2])),1,4)
            self.tilesTable.td(self.Lb_curT_access,0,5)
            self.tilesTable.td(gui.Label(self.tiles[self.cur_Tile][3]),1,5)
            self.tilesTable.td(self.Lb_curT_danger,0,6)
            self.tilesTable.td(gui.Label(self.tiles[self.cur_Tile][4]),1,6)
            self.tilesTable.td(self.Lb_Tiles,0,7)
            
            self.tilesTable.td(self.Se_Tile_Select,1,7)
            #------
            
            #update oben
            self.topTable.clear()
            self.topTable.td(self.Lb_map_name, 0, 0)
            self.topTable.td(self.Inp_map_name,1,0)                 
            self.topTable.td(self.Lb_map_dimH,0,1)
            self.topTable.td(self.Inp_map_dimH,1,1)
            self.topTable.td(self.Lb_map_dimV,0,2)
            self.topTable.td(self.Bt_applyOpt,0,3)
            self.topTable.td(self.Inp_map_dimV,1,2)
            self.topTable.td(self.Lb_map_bgMusic,2,0)
            self.topTable.td(self.Inp_map_bgMusic,3,0)
            self.topTable.td(self.Lb_map_entityFile,2,1)
            self.topTable.td(self.Inp_map_entityFile,3,1)
            self.topTable.td(self.Lb_map_nextLvl,2,2)
            self.topTable.td(self.Inp_map_nextLevel,3,2)
            self.topTable.td(self.Bt_newMap,4,0)
            self.topTable.td(self.Bt_loadMap,4,1)
            self.topTable.td(self.Bt_saveMap,4,2)
            #-----------
        
            
            
            #render
            self.mapSurface.fill((0,0,0))
            self.renderMap()
            self.screen.blit(self.mapSurface,(150,150))
            self.screen.blit(self.layerMenuBG,(0,0))
            self.screen.blit(self.tilesMenuBG,(1080,0))
            self.screen.blit(self.topMenuBG,(150,0))
            self.editApp.paint(self.screen)
            
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0] == 1:      #Linke Maustaste
                            self.replaceTile(pygame.mouse.get_pos())
                            
                        elif pygame.mouse.get_pressed()[2] == 1:    #Rechte Maustaste

                            if self.firstPress == False:
                                self.firstVar = pygame.mouse.get_pos()
                                self.firstPress = True
                            elif self.firstPress == True:
                                self.secVar = pygame.mouse.get_pos()
                                self.secPress = True
                            
                            if self.secPress == True:
                                self.camera += util.Vector(self.secVar[0] - self.firstVar[0], self.secVar[1] - self.firstVar[1])
                                self.firstPress = False
                                self.secPress = False
                            
                                
                    self.editApp.event(event)
            
            pygame.display.update()

    
MapEditor().start()




