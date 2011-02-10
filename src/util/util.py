'''
Created on 07.07.2009

@author: CaptnLenz
'''

from options import Options

def string2bool(inp):
    return inp.upper() in ["TRUE","1"]

def playSound(soundObject, loops=0):
    if soundObject.get_volume() != Options.getOption("VOLUME"):
        soundObject.set_volume(Options.getOption("VOLUME"))
    soundObject.play(loops)