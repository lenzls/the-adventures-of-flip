import pygame
import os

class RessourceLoader():
	def __init__(self):
		self.graphicDict = {}

	def load_graphic(self, filename):

		path = os.path.join('..', 'data', 'gfx',  filename)
		try:
			if not path in self.graphicDict:
				self.graphicDict[filename] = pygame.image.load(path).convert_alpha()
		except:
			print("Error while loading graphic: ", path)

		return self.graphicDict[filename]
			