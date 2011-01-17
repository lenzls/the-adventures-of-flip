import pygame
import os

class RessourceLoader():
	graphicDict = {}
	basepath = os.path.join(os.path.dirname(__file__), "..", "..")

	def __init__(self, basepath):
		pass

	@classmethod
	def load_graphic(RessourceLoader, filename):
		path = os.path.join(RessourceLoader.basepath, 'data', 'gfx',  filename)
		try:
			if not path in RessourceLoader.graphicDict:
				RessourceLoader.graphicDict[filename] = pygame.image.load(path).convert_alpha()
		except:
			print "Error while loading graphic: ", filename, " in: ", path

		return RessourceLoader.graphicDict[filename]

	@classmethod
	def load_sound(RessourceLoader, filename):
		path = os.path.join(RessourceLoader.basepath, 'data', 'sfx', filename)
		try:
			sound_object = pygame.mixer.Sound(path)
		except:
			print "Error while loading sound: ", filename, " in: ", path
		return sound_object
	
	@classmethod
	def load_font(RessourceLoader, filename, size):
		path = os.path.join(RessourceLoader.basepath,'data',filename)
		try:
			font_object = pygame.font.Font(path, size)
		except:
			print "Error while loading font: ", filename, " in: ", path
			
		return font_object

	@classmethod
	def getCorrectLevelPath(RessourceLoader, filename):
		return os.path.join(RessourceLoader.basepath, 'data', 'level', filename)