'''
Created on 07.07.2009

@author: CaptnLenz
'''

import constants
import game

if __name__ == '__main__':

    curGame = game.StateManager(constants.RESOLUTION)
    curGame.startGame()