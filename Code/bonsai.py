from Sector_bonsai import *
#from Sector_VL53L0X import VL53L0X
from Sector_VL6180 import VL6180X
from threading import Thread
import time
import RPi.GPIO as GPIO
from tlc59711 import Tlc59711
from Subfact_ina219 import INA219

GPIO.setmode(GPIO.BOARD)

iniPin 	= 		33
switchpin = 	8
daypin = 		38
seasonPin = 	32
sonnenSwitchPin = 15
pvSimPin = 		29
light1 = 		11
light2 = 		13
purgePin = 		35

isRunningPin	= 37

inaBus 	= INA219(0x40, "inaBus")
inaEly 	= INA219(0x41, "inaEly")

VLdist = VL6180X()

distanceAddr = 0x29 #i2c addresse Abstandssensor)

bonsai = Bonsai(iniPin,
				switchpin,
				daypin,
				seasonPin,
				sonnenSwitchPin,
				pvSimPin,
				light1,
				light2,
				purgePin, 
				inaBus, inaEly, 
				VLdist)

screenOutput = Prints(bonsai)
					
#========== Ausführung ====================================================
			
# === Statuslämpchen PV Ausrichtung ===
#PVthread = Thread(target = PVstatus, args=(PVpins, inaBus) )
#PVthread.start()

# === Initialisierung ===

bonsai.startSystem(iniPin)

# === Hauptprogramm ===

while True: 
	os.system('clear')
	bonsai.updateAll()
#	bonsai.purge()
	screenOutput.printAll(bonsai)

	time.sleep(0.5)
