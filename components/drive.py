"""
File Author: Will Hescott
File Creation Date: 1/25/2017
File Purpose: To create and run our drive functions
"""

import wpilib
import robotpy_ext
from robotpy_ext.common_drivers.navx.ahrs import AHRS
from wpilib import Encoder, Timer, RobotDrive, Spark, DigitalInput
from ctre.cantalon import CANTalon
from wpilib.interfaces import Gyro
from . import Component
import camera
from camera import Camera
import math


class driveTrain(Component):

	def __init__(self, robot):
		super().__init__()
		self.INCHES_PER_REV = 2*3.1415926*2
		self.robot = robot
		self.gyro = AHRS.create_spi()
		#self.gyro.calibrate()
		self.intakeOn = False
		self.intakeSpeed = .5
		self.i = 1
		self.lfmotor = CANTalon(7)#7#2
		self.lbmotor = CANTalon(6)#6#1
		self.rfmotor = CANTalon(1)#1#3
		self.rbmotor = CANTalon(2)
		self.rfmotor.setInverted(True)
		self.rbmotor.setInverted(True)
		self.robotDrive = RobotDrive(self.lfmotor, self.lbmotor, self.rfmotor, self.rbmotor)
		self.distanceSensor = DigitalInput(2)
		self.rfmotor.enableBrakeMode(True)
		self.rbmotor.enableBrakeMode(True)
		self.lfmotor.enableBrakeMode(True)
		self.lbmotor.enableBrakeMode(True)

		self.rfmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
		self.rbmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
		self.lfmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
		self.lbmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
		self.lfmotor.configEncoderCodesPerRev(4096)
		self.rfmotor.configEncoderCodesPerRev(4096)
		self.lbmotor.configEncoderCodesPerRev(4096)
		self.rbmotor.configEncoderCodesPerRev(4096)
		self.rfmotor.setPosition(0)
		self.lfmotor.setPosition(0)
		self.rbmotor.setPosition(0)
		self.lbmotor.setPosition(0)
		self.myInertia = 0
		self.cam = camera()

	def drive_forward(self, speed) :
		self.drive.tankDrive(speed, speed, True)

	def autonTankDrive(self, leftSpeed, rightSpeed):
		self.lfmotor.set(leftSpeed)
		self.lbmotor.set(leftSpeed)
		self.rfmotor.set(rightSpeed)
		self.rbmotor.set(rightSpeed)

	def getSensor(self):
			return self.distanceSensor.get()

	def reset(self):
		self.rfmotor.set(0)
		self.rbmotor.set(0)
		self.lfmotor.set(0)
		self.lbmotor.set(0)
		self.rfmotor.setPosition(0)
		self.rbmotor.setPosition(0)
		self.lfmotor.setPosition(0)
		self.lbmotor.setPosition(0)
		self.rfmotor.setEncPosition(0)
		self.rbmotor.setEncPosition(0)
		self.lfmotor.setEncPosition(0)
		self.lbmotor.setEncPosition(0)
		self.zeroGyro()

	def turnAngle(self, degrees, speed=0.2):
		if(self.gyro.getAngle() > degrees+0.25):
			self.autonTankDrive(-1*speed, speed)
			print(self.gyro.getAngle())
		elif(self.gyro.getAngle() < degrees-0.25):
			self.autonTankDrive(speed, -1*speed)
			print(self.gyro.getAngle())
			print('turningRight')
		elif(self.gyro.getAngle() <= degrees-0.25):
			self.autonTankDrive(-1*speed, speed)
			print('turningLeft')
			print(self.gyro.getAngle())
		else:
			return True
		return False

	def visionLineUp(self):
		self.cam.receive()
		if self.cam.centerSide():#and self.cam.centerLine() :	#this works because of short-circuiting
			print("hooboyshoot")
			self.reset()
			#oh what fun it is to ride

	def findGoal(self, moveType=True):
		x = 25
		if moveType != self.cam.CamState:
			self.cam.switch()
		self.cam.receive()
		if x < 25:
			x += 1
			self.autonTankDrive(0,0)
			return False
		if self.centerSide(moveType):#and self.cam.centerLine() :	#this works because of short-circuiting #in a one-horse open sleigh
			self.reset()
			x = 0
			return True
		return False

	def drive(self, leftX, leftY, rightX):
			self.robotDrive.mecanumDrive_Cartesian(leftX*-1, leftY*-1, rightX, self.gyro.getAngle())
	def zeroGyro(self):
		self.gyro.reset()
	def enablePIDs(self):
		'''
		#No longer required because we swapped from analog encoders to magnetic encoders
		self.pidLeftFront.enable()
		self.pidLeftBack.enable()
		self.pidRightFront.enable()
		self.pidRightBack.enable()
		'''
	# Disable PID Controllers
	def disablePIDs(self):
		'''
		#see explaination above
		self.pidLeftFront.disable()
		self.pidLeftBack.disable()
		self.pidRightFront.disable()
		self.pidRightBack.disable()
		'''
	def getGyroAngle(self):
		return self.gyro.getAngle()

	def getIntakeSpeed(self):
		return self.intakeSpeed

	def getDistance(self):
		return (self.convertEncoderRaw(abs(self.rfmotor.getPosition()))
				+ self.convertEncoderRaw(abs(self.rbmotor.getPosition()))
				+ self.convertEncoderRaw(abs(self.lfmotor.getPosition()))
				+ self.convertEncoderRaw(abs(self.lbmotor.getPosition())))/4
		#detirmines how many ticks the encoder has processed
		#converts ticks from getMotorDistance into inches
	def convertEncoderRaw(self, selectedEncoderValue):
		return selectedEncoderValue * self.INCHES_PER_REV


	def centerSide(self, moveType=True):
		if(self.cam.mid_x == None):
			self.autonTankDrive(0, 0)

			if(self.myInertia > 0):
				self.myInertia -= 1
			return False
		elif(abs(self.cam.mid_x) > camera.DDZ_ROT):	#radians, arbitrary deadzone value
			if(abs(self.cam.mid_x) > 0.15):
				spdMag = 0.15
			else:
				spdMag = 0.09
			if(self.myInertia <= 1):
				spdMag += 0.02
				print("Speed Boost")
				self.myInertia = 0
			if(self.myInertia <= 5):
				self.myInertia += 1
			spd = math.copysign(spdMag, self.cam.mid_x)#min(max(MIN_ROT_SPD, abs(self.mid_x)), MAX_ROT_SPD), self.mid_x)	#again arbitrary numbers
			if moveType:	#shooter
				self.autonTankDrive(spd, -spd)
			else:	#gears
				self.autonTankDrive(spd, spd)	#forward, back -- gear on side
			return False
		self.autonTankDrive(0, 0)
		if(self.myInertia > 0):
			self.myInertia -= 1
		return True
