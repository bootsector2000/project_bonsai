#!/usr/bin/python3

import time

# necesarry imports for the class

import sys
import spidev                     # changed from spi to spidev
from bitstring import BitArray    # https://pypi.python.org/pypi/bitstring

# necesarry initialisation of spi
spi=spidev.SpiDev()

class Tlc59711:
	"""Communicates with the TLC59711"""
	def __init__(self):
		self.outtmg = 1
		self.extgck = 0
		self.tmgrst = 1
		self.dsprpt = 1
		self.blank = 0
		self.brightness = tuple([0b0111111] * 3)  # (R, G, B) brightnes
		self.pixels = [(0, 0, 0)] * 4             # (R, G, B) 0-3

	def command(self):
		"""The bytes of the command that should update the data"""
		command = BitArray('0b100101') # magic WRITE code
		# make sure the values are single bits
		command += [BitArray(bool=bit) for bit in (self.outtmg, self.extgck, self.tmgrst,self.dsprpt, self.blank)]
		for b in self.brightness:
			command += BitArray(uint=b, length=7) 
		for rgb in self.pixels:
			for color in rgb:
				command += BitArray(uint=color, length=16)
		assert len(command) == 224
		#print (tuple([ba.uint for ba in command.cut(8)]))
		return tuple([ba.uint for ba in command.cut(8)])
		#full brightnes return tuple([150, 223, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255])
		#return tuple([150, 207, 223, 191, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255])
		#return tuple([150, 223, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 255, 255, 255, 255])
	def sendCommand(self):
		spi.open(0,0)
		spi.max_speed_hz = 1000				#slow down the speed because long cables
		spi.mode = 0b11					#works without setting spi mode
#		spi.xfer(list(self.command()) )			#can use writebytes as well
		spi.writebytes(list(self.command()))
#allon		spi.xfer([150, 223, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255])
		spi.close()

	def onUp(self):
		spi.open(0,0)
		spi.max_speed_hz = 1000
		spi.mode = 0b11
		spi.writebytes(list(tuple([150,223,255,255, 0,0,0,0,0,0,255,255,0,0,255,255,255,255,0,0,255,255,0,0,0,0] ) ) )
		spi.close()
	def onDown(self):
		pass
	def allOn(self):
		self.pixels = [tuple([65535]) * 3] * 4
		self.sendCommand()
	def allOff(self):
#		self.pixels = [tuple([0]) * 3] * 4		
		spi.open(0,0)
		spi.max_speed_hz = 1000				#slow down the speed because long cables
		spi.mode = 0b11					#works without setting spi mode
		spi.writebytes(list(tuple([150, 223, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])))
		spi.close()
		#self.sendCommand()


#if __name__ == '__main__':#
#	i = 0
#	tlc = Tlc59711()
#	while True:
#		tlc.allOn()
#		print("on")
#		input()
#		print("off")
#		tlc.allOff()
#		input()
		
