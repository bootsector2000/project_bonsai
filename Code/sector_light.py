#!/usr/bin/python3

import RPi.GPIO as GPIO
from tlc59711 import Tlc59711

GPIO.setmode(GPIO.BOARD)


class Houselight:
	def __init__(self, lightpin1, lightpin2):
		GPIO.setup(lightpin1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.setup(lightpin2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
		
		self.light1 = lightpin1
		self.light2 = lightpin2
		self.driver = Tlc59711()
		
		self.lightStatus = 42
		
	def getLightStatus(self): #verschiedene Stellungen: 1, sonst 0 
		if ( GPIO.input(self.light1) and not GPIO.input(self.light2) ) or ( not GPIO.input(self.light1) and GPIO.input(self.light2) ):
			return 1
		else:
			return 0
	def updateLight(self):
		if GPIO.input(self.light1) or GPIO.input(self.light2): 
			self.driver.allOn()
			self.lightStatus = 1
		else:
			self.driver.allOff()
			self.lightStatus = 0