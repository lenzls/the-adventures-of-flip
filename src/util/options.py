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

    @classmethod
    def getOption(Options, keyString):
        return Options.options[keyString]
    
    @classmethod
    def setOption(Options, keyString, newVal):
        Options.options[keyString] = newVal