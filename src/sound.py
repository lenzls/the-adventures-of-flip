import pygame.mixer
from util.ressourceLoader import RessourceLoader
from util.options import Options

class SoundManager():

	sounds = {}

	@classmethod
	def addSound(name, filename):
		newObj = RessourceLoader.load_sound(filename)
		sounds[name] = newObj

	@classmethod
	def playSound(name, loops=0,fade_ms=0):
		sounds[name].play(loops=loops,fade_ms=fade_ms)	#TODO: check if fade_ms == fadein

	@classmethod
	def stopSound(name, fadeOut=False):
		print "asu",fadeOut
		if fadeOut:
			sounds[name].fadeout(1500)
		else:
			sounds[name].stop()

	@classmethod
	def pauseSound(name):
		sounds[name].pause()

	@classmethod
	def resumeSound(name):
		sounds[name].unpause()

	@classmethod
	def getVolSound(name):
		return sounds[name].get_volume()

	@classmethod
	def setVolSound(name, newValue):
		sounds[name].set_volume(newValue)

	@classmethod
	def updateVolumes():
		for sound in sounds:
			sound.set_volume(Options.getOption("VOLUME"))
