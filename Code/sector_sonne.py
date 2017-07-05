#!/usr/bin/python3

import RPi.GPIO as GPIO

class Sonne:
	def __init__(self, sonnenswitchpin, pvSimPin):
		
		GPIO.setup(sonnenswitchpin, GPIO.OUT, initial = 0)
		GPIO.setup(pvSimPin, GPIO.OUT, initial = 0)
		
		self.sonnenswitchpin = sonnenswitchpin
		self.pvSimPin = pvSimPin
		
	def turnOn(self):
		GPIO.output(self.sonnenswitchpin, False)
		GPIO.output(self.pvSimPin, False)
		
	def turnOff(self):
		GPIO.output(self.sonnenswitchpin, True)
		GPIO.output(self.pvSimPin, True)