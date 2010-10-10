'''
Created on 10.10.2010

@author: simon
'''



class Options(object):
    options = {}
    
    #def __init__(self, **kwargs):
#        Options.options = kwargs

#        self.resolution = kwargs["RESOLUTION"]
#        self.isFullScr = kwargs["ISFULLSCR"]
#        self.isSound = kwargs["ISSOUND"]
#        self.isDebug = kwargs["ISDEBUG"]

    def getOption(self, keyString):
        return Options.options[keyString]
    
    def setOption(self, keyString, newVal):
        Options.options[keyString] = newVal