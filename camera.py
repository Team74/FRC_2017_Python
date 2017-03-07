#Will your code should be at the bottom. Fill in the stuff in HooBoyShoot. Also I think the calls to AutonTankDrive are wrong.

import math
import serial
from time import sleep

TARGET = 0.07

DDZ_ROT = 0.03
MIN_ROT_SPD = 0.04
MAX_ROT_SPD = 0.3

DDZ_MOV = 0.1
MIN_MOV_SPD = 0.05

REF_THETA = 45
REF_TOW_H = 2.38
REF_CAM_H = .8
REF_DIST = (REF_TOW_H - REF_CAM_H) / math.tan(REF_THETA)

MUZZLE_VELOCITY = 30	#meters/second
COMPLETELY_ARBITRARY_CONSTANT = 1

class Camera:
	old_x = 0
	mid_x = None
	mid_y = None
	theta = None
	distance = None
	ser = None
	driveDelay = 0
	CamState = True	#default, shooter / false = gears

	def __init__(self):
		#self.ser = serial.Serial("/dev/ttyS1", 115200, timeout=0.05)
		pass
	def receive(self, moveType=True):
		print("yo 1")
		self.ser.write("boom ya got waffles\n".encode())
		print("yo 1.5")
		#ans = self.ser.readline()
		ans = self.ser.read(100)
		print("yo 2")
		print("yoyette: " + ans.decode())
		if ans:
			ans = self.uncode(ans.decode())
			if self.old_x != float(ans[0]):
				self.old_x = self.mid_x
				self.mid_x = float(ans[0])
				self.mid_y = float(ans[1])
				self.theta = float(ans[2])
				self.distance = float(ans[3])*39.37#camera returns distance values in meters, converting to inches to preserve continuity and readability.
				print(str(self.mid_x))			   #This also allows it to work with all other movement functions, which require a desired distance variable
				return
			else:
				print("no new")
		else:
			print("no response")
		self.mid_x = None
		self.mid_y = None
		self.theta = None
		self.distance = None
		#print("skip")

	def uncode(self, string):
		stuff = []
		number = ""
		state = "previous"
		for char in string:
			if state == "previous":
				if char == "s":
					state = "start"
			elif state == "start":
				if char == "m":
					state = "read"
			elif state == "read":
				if char == "m":
					stuff.append(number)
					number = ""
				elif char == "e":
					stuff.append(number)
					number = ""
					state == "previous"
				else:
					number += char
		return stuff


	def centerLine(self):
		if(abs(self.distance - REF_DIST) > DDZ_MOV):	#meters, arbitrary deadzone value
			spd = math.copysign(0.1, self.distance - REF_DIST)#max(MIN_MOV_SPD, abs(distance))*math.copysign(1.0, distance)
			self.autonTankDrive(spd,spd)
			return False
		return True

	def switch(self):
		self.CamState = not self.CamState
		self.ser.write("the times they are\n".encode())
		self.ser.readline()


#max(MIN_ROT_SPD, min(MAX_ROT_SPD, abs(self.theta - REF_THETA)))
'''	def ShootDistance(self):	#I *guarantee* this does *not* work
		angle = math.arcsin(((REF_TOW_H - REF_CAM_H)/self.distance+4.9*self.distance)/MUZZLE_VELOCITY)
		#MAGIC -- set the shooting apparatus angle
		#MAGIC -- call a function that spins the shooting wheels

		#note that this function may not work on the grounds of returning angles beyond our operational capabilities
		#it can be changed, but it's not important anyway
'''
'''
thng.receive()
if thng.centerSide() and thng.centerLine() :	#this works because of short-circuiting
	HooBoyShoot()
'''
