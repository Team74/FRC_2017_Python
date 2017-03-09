#Will your code should be at the bottom. Fill in the stuff in HooBoyShoot. Also I think the calls to AutonTankDrive are wrong.

import math
import serial
from time import sleep

TARGET = 0.07

DDZ_ROT = 0.03
#MIN_ROT_SPD = 0.04
#MAX_ROT_SPD = 0.3

DDZ_MOV = 0.1
#MIN_MOV_SPD = 0.05

FOV_X = 61
REF_THETA = 35
REF_TOW_H = 84
REF_CAM_H = 9.5
REF_DIST = (REF_TOW_H - REF_CAM_H) / math.tan(REF_THETA)

#MUZZLE_VELOCITY = 30	#meters/second
#COMPLETELY_ARBITRARY_CONSTANT = 1

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
		self.ser = serial.Serial("/dev/ttyS1", 115200, timeout=0.05)
		pass
	def receive(self, moveType=True):
		self.ser.write(("shooter\n" if moveType else "gears\n").encode())
		ans = self.ser.readline()
		#ans = self.ser.read(100)
		if ans:
			ans = self.uncode(ans.decode())
			if ans[0] != "" and self.old_x != float(ans[0]):
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

'''	def ShootDistance(self):	#I *guarantee* this does *not* work
		MUZZLE_VELOCITY = ((REF_TOW_H - REF_CAM_H)/self.distance+4.9*self.distance)/math.sin(angle)
		#MAGIC -- set the shooting apparatus angle
		#MAGIC -- call a function that spins the shooting wheels

		#note that this function may not work on the grounds of returning angles beyond our operational capabilities
		#it can be changed, but it's not important anyway
'''
