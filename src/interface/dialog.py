'''
Created on 29.09.2010

@author: simon
'''
import pygame

class SpeechBubble(object):
    def __init__(self, msg, curGameState):
        self.msg = msg

        self.pagesC = 0

        self.stringList = self.calcStringList()
        self.curPageList = self.stringList[self.pagesC]
        self.curGameState = curGameState
        self.isFinished = False

    def calcStringList(self):
        #[page[line,line],page[line]]
        stringList = []
        iRow = 0
        iRowChar = 0
        iPage = -1
        

        for item in self.msg.split("|"):
            #new Page
            iPage += 1
            iRow = 0
            iRowChar = 0
            stringList.append([""])

            words = item.split()
            for word in words:
                if iRowChar + len(word) > 42:
                    if iRow+1 >= 4:
                        #new Page
                        iPage += 1
                        iRow = 0
                        iRowChar = 0
                        stringList.append([""])
                    else:
                        iRowChar = 0
                        iRow += 1
                        stringList[iPage].append("")
                iRowChar += len(word)+1
                stringList[iPage][iRow] += word +" "        

        return stringList

    #TODO improve name
    def execute(self):
        while True:
            self.curGameState.render()
            self.curGameState.gameRenderer.renderBubble(self)
            
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.next_Page()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.isFinished = True

            if self.isFinished == True:
                break
            pygame.display.update()

    def next_Page(self):
        self.pagesC += 1
        
        try:
            self.curPageList = self.stringList[self.pagesC]
        except IndexError:
            self.isFinished = True