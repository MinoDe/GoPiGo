#!/usr/bin/python
import serial, time
import smbus
import math
import RPi.GPIO as GPIO
import struct
ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)
ser.flush()
class GPS:
	inp=[""]*7
	# Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
	GGA=[]
	GSA=[]
	GSV=[]
	RMC=[]

	def read(self):
		start=0
		for i in range(7):
			GPS.inp[i]=ser.readline()
		for i in range(7):
			if GPS.inp[i][:6] =='$GPGGA': # GGA data , packet 1
				start=i
				
				break
		GPS.GGA=GPS.inp[start].split(",")
		GPS.GSA=GPS.inp[start+1].split(",")
		GPS.GSV=GPS.inp[start+2].split(",")
		GPS.RMC=GPS.inp[start+3].split(",")
		
		for i in range(4):
			print GPS.inp[i+start]
		#print GPS.GGA,GPS.GSA,GPS.GSV,GPS.RMC
		return [GPS.GGA,GPS.GSA,GPS.GSV,GPS.RMC]
		
	def vals(self):
		time=GPS.GGA[1]
		lat=GPS.GGA[2]
		lat_ns=GPS.GGA[3]
		long=GPS.GGA[4]
		long_ew=GPS.GGA[5]
		fix=GPS.GGA[6]
		sats=GPS.GGA[7]
		alt=GPS.GGA[9]
		return [time,fix,sats,alt,lat,lat_ns,long,long_ew]

g=GPS()
while True:
	try:
		x=g.read()
		#for i in range (4):
		#	print x[i]
		print g.vals()
	except IndexError:
		print "Unable to read"
	time.sleep(2)
