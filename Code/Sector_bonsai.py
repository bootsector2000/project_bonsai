#usr/bin/python3
import RPi.GPIO as GPIO
from Subfact_ina219 import INA219
import os
from Sector_VL6180 import VL6180X
from sector_light import Houselight
from sector_statemachine import Statemachine
from sector_sonne import Sonne
from sector_prints import Prints
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
import time
from threading import Thread


class Bonsai:
	def __init__(self, iniPin, switchpin, daypin, seasonpin, sonnenswitchpin, pvSimPin, light1, light2, purgepin, inabus, inaely, vldist):
		GPIO.setup(iniPin, GPIO.OUT, initial = 0)
		GPIO.setup(switchpin, GPIO.OUT, initial = 1)
		GPIO.setup(seasonpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(daypin , GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(light1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(light2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(purgepin, GPIO.OUT, initial = 1)
		
		self.inipin = iniPin
		self.switchpin = switchpin		#Ely, BZ
		self.daypin = daypin			#Tageszeit
		self.seasonpin = seasonpin		#Jahreszeit
		self.sonnenswitchpin = sonnenswitchpin
		self.pvSimPin = pvSimPin
		
		self.sun = Sonne(self.sonnenswitchpin, self.pvSimPin)
		self.light = Houselight(light1, light2)
		self.sm = Statemachine(self.daypin, self.seasonpin, self.light, self.switchpin)
		
		self.light = Houselight(light1, light2)
		
		self.VLdist = vldist 
		
		self.purgepin = purgepin
		self.inaBus = inabus
		self.inaely = inaely
		
		self.inas = (self.inaBus, self.inaely)
		
		self.dist = self.getDistance()
		self.FullDist = 20
		self.EmptyDist = 100
		
	
	def startSystem(self, iniPin):
		while True: #Init
			GPIO.output(iniPin, not GPIO.input(iniPin) )
			self.updateAll()
			time.sleep(0.2)
			os.system('clear')
			self.updateAll()
#			GPIO.output(self.purgepin, True)
			
			print ("wait for init")
			if self.state == 1:
				print ("initialisiere")
				
				purging = Thread(target = self.purge, args=( ) )
				purging.start()
				print ("Thread Purge gestartet") 
				
				GPIO.output(iniPin, True)
				time.sleep(10)
				print ("initDone")
#				runThread = Thread(target = isRunning, args = (isRunningPin,) )
#				runThread.start()
#				print ("isRunningLED gestartet")
				GPIO.output(iniPin, False)
				break
	
	def purge(self):
		while True:
			if not (self.state == 1 or self.state == 2) and (self.inaBus.getBusVoltage_V() < 3.7) and self.dist < 100:
				print ("volt: {} | state: {}". format(self.inaBus.getBusVoltage_V(), self.state) ) 
				GPIO.output(self.purgepin, False)
				time.sleep(1)
				GPIO.output(self.purgepin, True)
				time.sleep(12)
			else:
				GPIO.output(self.purgepin, True)
	
	def getDistance(self):
		self.dist = self.VLdist.get_distance()
		return self.dist
	
	def getCurrent(self, ina):
		return ina.getCurrent_mA()
		
	def getVoltage(self, ina):
		return ina.getBusVoltage_V()
		
	def getPower(self, ina):
		return ina.getPower_mW()
			
	def relaisSchalten(self) :
		if self.sm.state == 1: 			#sommertag: ely läuft, sonne an, strom an
			self.sun.turnOn()
			
			if self.dist < self.FullDist: 
				self.sm.setMode(1)			#BZ-Mode
			elif self.dist > (self.FullDist + 10) :
				self.sm.setMode(0)			#Ely-Mode
			
		elif self.sm.state == 2:			#sommernacht: ely-mode, strom aus, sonne aus (superCap - Mode)
			self.sun.turnOff()
			self.sm.setMode (0)
			
		elif self.sm.state == 3:				#Wintertag: BZ an, Sonne an, Strom aus
			self.sun.turnOn()
			if self.dist > self.EmptyDist : 	#wenn tank leer, schalte auf ely 
				self.sm.setMode(0)
			elif self.dist < self.EmptyDist - 10:
				self.sm.setMode(1)
				
		elif self.sm.state == 4:				#Winternacht: BZ an, Sonne aus, Strom aus
			self.sun.turnOff()
			if self.dist > self.EmptyDist : #wenn tank leer, schalte auf ely 
				self.sm.setMode(0)
			elif self.dist < self.EmptyDist - 10:
				self.sm.setMode(1)
		
		elif self.sm.state == 5:
			if GPIO.input(self.switchpin) :	# BZ - Mode, Sonne aus, Strom aus

				if self.dist < self.EmptyDist :
					self.sun.turnOff()
				elif self.dist > self.EmptyDist - 5 :

					GPIO.output(self.switchpin, False)	#Ely
				
			else :
				if self.dist > self.FullDist :
					self.sun.turnOn()
				elif self.dist < self.FullDist + 5:
					GPIO.output(self.switchpin, True)
		
	def updateAll(self):
		self.sm.updateState()
		self.state = self.sm.state
		self.light.updateLight()
		self.getDistance()
		self.relaisSchalten()
		