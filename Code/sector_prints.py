#!/usr/bin/python3

import RPi.GPIO as GPIO
import os

class Prints:
	def __init__(self, system):
		self.system = system	
		
	def getStateText(self, system):
		if system.sm.state == 1:
			return "Sommertag"
		elif system.sm.state == 2:
			return "Sommernacht"
		elif system.sm.state == 3:
			return "Wintertag"
		elif system.sm.state == 4:
			return "Winternacht"
		elif system.sm.state == 5:
			return "Automode"
		else:
			return "irgendwas is faul"
			
	def getPVText(self, system):
		if not GPIO.input(system.pvSimPin):
			return "an"
		else:
			return "aus"
			
	def getSunText(self, system):
		if not GPIO.input(system.sonnenswitchpin):
			return "an"
		else:
			return "aus"
	
	def getModeText(self, system):
		if not GPIO.input(system.switchpin):
			return "Ely"
		else:
			return "BZ"
	
	def getTempText(self):
		return os.system('vcgencmd measure_temp')
	
	def getHouseLightText(self, system):
		if system.light.lightStatus == 1:
			return ("an")
		else: 
			return ("aus")
		
	def printCurrentVoltageText(self, system):
		for ina in system.inas:
			print ("{:6} -- Strom: {:3.2f}mA | Spannung: {:3.2f}V | Leistung:{:3.2f}mW".format(ina.name, ina.getCurrent_mA(), ina.getBusVoltage_V(), ina.getPower_mW() ) )	
	
	def printAll(self, system):
		print ("{} ({}) | {}-Mode" .format(self.getStateText(system), system.sm.state, self.getModeText(system) ) )
		print ("Hauslicht: {} | Sonne: {} | PVSim: {}" .format(self.getHouseLightText(system), self.getSunText(system), self.getPVText(system) ) ) 
		self.printCurrentVoltageText(system)
		print ("Füllstand: {}" .format(system.dist) )
		self.getTempText()
		
		