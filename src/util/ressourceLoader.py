import pygame
import os

class RessourceLoader():
	graphicDict = {}
	
	def __init__(self):
		pass

	def load_graphic(self, filename):

		path = os.path.join('..', 'data', 'gfx',  filename)
		try:
			if not path in RessourceLoader.graphicDict:
				RessourceLoader.graphicDict[filename] = pygame.image.load(path).convert_alpha()
		except:
			print "Error while loading graphic: ", path

		return RessourceLoader.graphicDict[filename]

	def load_sound(self, filename):
		path = os.path.join('..', 'data', 'sfx', filename)
		try:
			sound_object = pygame.mixer.Sound(path)
		except:
			print "Error while loadering sound: ", path
		return sound_object