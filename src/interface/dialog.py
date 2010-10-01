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
        stringList.append([""]) #add first page
        iRow = 0
        iRowChar = 0

        for char in self.msg:
            if char == "|":
                # new Page
                iRow = 0
                iRowChar = 0
                stringList.append([""])
            else:
                if iRowChar >= 42:
                    # new Row
                    stringList[-1].append("")
                    iRow += 1
                    iRowChar = 0
                    if iRow >= 4:
                        # new page
                        iRow = 0
                        iRowChar = 0
                        stringList.append([""])      

                iRowChar +=1
                stringList[-1][-1] += char
        return stringList

    #TODO improve name
    def execute(self):
        while True:
            self.curGameState.render()
            self.curGameState.gameRenderer.renderBubble(self)
            
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
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