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

    volumeList = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1,0]
    resolutionList =[(400,240),(800,480),(800,600),(1024,615),(1024,768)]

    @classmethod
    def getOption(Options, keyString):
        return Options.options[keyString]
    
    @classmethod
    def setOption(Options, keyString, newVal):
        Options.options[keyString] = newVal