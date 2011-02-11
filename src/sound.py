
from util.ressourceLoader import RessourceLoader
from util.options import Options

class SoundManager():

	sounds = {}

	@classmethod
	def addSound(SoundManager, name, filename):
		if SoundManager.sounds.__contains__(name):
			SoundManager.stopSound(name, fade_ms=100)
		newObj = RessourceLoader.load_sound(filename)
		SoundManager.sounds[name] = newObj
		print SoundManager.sounds

	@classmethod
	def playSound(SoundManager, name, loops=0,fade_ms=0):
		try:
			SoundManager.sounds[name].play(loops=loops,fade_ms=fade_ms)
		except KeyError:
			print "Sound: %s not Found" %name

	@classmethod
	def stopSound(SoundManager, name, fade_ms=0):
		try:
			SoundManager.sounds[name].fadeout(fade_ms)
		except KeyError:
			print "Sound: %s not Found" %name

	@classmethod
	def pauseSound(SoundManager, name):
		try:
			SoundManager.sounds[name].pause()
		except KeyError:
			print "Sound: %s not Found" %name


	@classmethod
	def resumeSound(SoundManager, name):
		try:
			SoundManager.sounds[name].unpause()
		except KeyError:
			print "Sound: %s not Found" %name


	@classmethod
	def getVolSound(SoundManager, name):
		try:
			return SoundManager.sounds[name].get_volume()
		except KeyError:
			print "Sound: %s not Found" %name


	@classmethod
	def setVolSound(SoundManager, name, newValue):
		try:
			SoundManager.sounds[name].set_volume(newValue)
		except KeyError:
			print "Sound: %s not Found" %name


	@classmethod
	def updateVolumes(SoundManager):
		for sound in SoundManager.sounds:
			print sound
			SoundManager.setVolSound(sound, Options.getOption("VOLUME"))
