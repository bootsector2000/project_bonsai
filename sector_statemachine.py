#!/usr/bin/python3

import RPi.GPIO as GPIO

class Statemachine:
	def __init__(self, daypin, seasonpin, light, switchpin):
		GPIO.setup(daypin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(seasonpin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		
		self.daypin = daypin
		self.seasonpin = seasonpin
		self.switchpin = switchpin
		self.light = light
		
		self.state = self.getState(self.light)
	
	def getSeason(self):		# 0: Sommer | 1: Winter
		return not GPIO.input(self.seasonpin)
		
	def getDayTime(self): 		# 0: Tag | 1: Nacht
		return not GPIO.input(self.daypin)
	
	def setMode(self, mode):	# 0: Ely | 1: BZ
		self.mode = mode
		if mode == 0:
			GPIO.output(self.switchpin, False)
		else:
			GPIO.output(self.switchpin, True)
			
	def getMode(self):	
		if not GPIO.input(self.switchpin):
			mode = "Ely"
		else:
			mode = "BZ"
		return mode
		
	def getState(self, light):			# 1: Sommertag | 2: Sommernacht | 3: Wintertag | 4: Winternacht | 5: Automatic
		if not self.getDayTime() and not self.getSeason():
			if not light.getLightStatus():
				return 1
			else:
				return 5
		elif self.getDayTime() and not self.getSeason():
			return 2
		elif not self.getDayTime() and self.getSeason():
			return 3
		elif self.getDayTime() and self.getSeason():
			return 4
	
	def updateState(self):
		self.state = self.getState(self.light)