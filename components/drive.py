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
		self.MAX_RANGE = 126
		self.MIN_RANGE = 77
		self.INCHES_PER_REV = 2*3.1415926*2
		self.robot = robot
		self.gyro = AHRS.create_spi()
		#self.gyro.calibrate()
		self.intakeOn = False
		self.intakeSpeed = .5
		self.i = 1
		self.savedDistance = 0

		self.lfmotor = CANTalon(7)#7#2
		self.lbmotor = CANTalon(6)#6#1
		self.rfmotor = CANTalon(1)#1#3
		self.rbmotor = CANTalon(2)#2

		self.rfmotor.setInverted(True)
		self.rbmotor.setInverted(True)

		self.robotDrive = RobotDrive(self.lfmotor, self.lbmotor, self.rfmotor, self.rbmotor)

		self.distanceSensor = DigitalInput(0)

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

		self.initialAngle=0
		self.myInertia = 0
		self.cam = Camera()
		self.curSearch = False #Represents whether we are currently using shooter vision; used to trigger on-presss and -release
		self.curSearch_center = False #Reps. whether we are centered; resets on release of vision button (right trigger)

	def drive_forward(self, speed) :
		self.drive.tankDrive(speed, speed, True)

	def autonTankDrive(self, leftSpeed, rightSpeed):
		self.lfmotor.set(leftSpeed)
		self.lbmotor.set(leftSpeed)
		self.rfmotor.set(rightSpeed)
		self.rbmotor.set(rightSpeed)

	def autonStrafe(self, strafeSpeed):
			self.rfmotor.set(strafeSpeed*-1)
			self.lbmotor.set(strafeSpeed*-1*0.925)
			self.rbmotor.set(strafeSpeed*0.925)
			#			self.rfmotor.set(strafeSpeed*-1*min(1+self.gyro.getAngle()/150, 1))
			#			self.lbmotor.set(strafeSpeed*-1*min(1-self.gyro.getAngle()/150, 1))
			#			self.rbmotor.set(strafeSpeed*min(1-self.gyro.getAngle()/150, 1))
			#			self.lfmotor.set(strafeSpeed*min(1+self.gyro.getAngle()/150, 1))
			self.lfmotor.set(strafeSpeed)
	def getSensor(self):
		return self.distanceSensor.get()

	def strafe2(self, speed, desiredAngle):
		if speed > 0.8:
			speed = 0.8
		#speed = 0
		compensateAngle=True
		compensateDrift=False
		compensateCam=False
		autonOffset = -.47
		FOVVar = .05
		aVariable = 0.0375
		deadzone = .01
		lfmotorSpeed = speed
		lbmotorSpeed = -speed
		rfmotorSpeed = -speed
		rbmotorSpeed = speed
		if compensateAngle:
			if self.gyro.getAngle() > desiredAngle+1 :
				lfmotorSpeed -= aVariable
				lbmotorSpeed -= aVariable
				rfmotorSpeed += aVariable
				rbmotorSpeed += aVariable
			elif self.gyro.getAngle() < desiredAngle-1 :
				lfmotorSpeed += aVariable
				lbmotorSpeed += aVariable
				rfmotorSpeed -= aVariable
				rbmotorSpeed -= aVariable
		if compensateDrift:
			print (self.gyro.getDisplacementX())

			if self.gyro.getDisplacementX() < -deadzone:
				lfmotorSpeed += aVariable
				lbmotorSpeed += aVariable
				rfmotorSpeed += aVariable
				rbmotorSpeed += aVariable
			elif self.gyro.getDisplacementX() > deadzone:
				lfmotorSpeed -= aVariable
				lbmotorSpeed -= aVariable
				rfmotorSpeed -= aVariable
				rbmotorSpeed -= aVariable

		if compensateCam:
			try:
				self.cam.recieve()
				if (self.cam.mid_x != None and abs(self.cam.mid_x - autonOffset) > FOVVar):
					if self.cam.mid_x - autonOffset > 1:
						lfmotorSpeed += aVariable
						lbmotorSpeed += aVariable
						rfmotorSpeed -= aVariable
						rbmotorSpeed -= aVariable
					else:
						lfmotorSpeed -= aVariable
						lbmotorSpeed -= aVariable
						rfmotorSpeed += aVariable
						rbmotorSpeed += aVariable

			except:
				pass
		self.rfmotor.set(rfmotorSpeed)
		self.rbmotor.set(rbmotorSpeed)
		self.lfmotor.set(lfmotorSpeed)
		self.lbmotor.set(lbmotorSpeed)


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

	def rampByRange(self):
		pass


	def turnAngle(self, degrees, speed):
		if(self.gyro.getAngle() > degrees+0.25):
			self.autonTankDrive(-1*speed, speed)
			print(self.gyro.getAngle())
		elif(self.gyro.getAngle() < degrees-0.25):
			self.autonTankDrive(speed, -1*speed)
			print(self.gyro.getAngle())
		elif(self.gyro.getAngle() <= degrees-0.25):
			self.autonTankDrive(-1*speed, speed)
			print(self.gyro.getAngle())
		else:
			return True
		return False

	def visionLineUp(self):	# I don't think we use this method. See findGoal.
		if self.cam.centerSide():#and self.cam.centerLine() :	#this works because of short-circuiting
			self.reset()

	def findGoal(self, moveType=True):
		print("haha 2")
		if self.centerSide(moveType):#and self.cam.centerLine() :	#this works because of short-circuiting #in a one-horse open sleigh
			print("haha 3")
			self.reset()
			x = 0
			return True
		print("haha 4")
		return False

	def drive(self, leftX, leftY, rightX):
			self.robotDrive.mecanumDrive_Cartesian(leftX*-1, leftY*-1, rightX, self.gyro.getAngle())
			print(self.convertEncoderRaw(abs(self.rfmotor.getPosition())))
			print(self.convertEncoderRaw(abs(self.rbmotor.getPosition())))
			print(self.convertEncoderRaw(abs(self.lfmotor.getPosition())))
			print(self.convertEncoderRaw(abs(self.lbmotor.getPosition())))
	def driveWithoutGyro(self, leftX, leftY, rightX):
				self.robotDrive.mecanumDrive_Cartesian(leftX*-1, leftY*-1, rightX, 0)

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

	def getEncoder(self):#function used in shooter testing, obselete on main robot but useful elsewhere
			return self.lfmotor.getPosition()

	def getInRange(self):
		if(self.cam.distance>self.MAX_RANGE):
			self.autonTankDrive(0.75, 0.75)
		elif(self.cam.distance<self.MIN_RANGE):
			self.autonTankDrive(-0.75,-0.75)
		else:
			self.autonTankDrive(0,0)
			return True

	def centerSide(self, moveType=True):
		try:
			self.cam.receive(moveType)
		except Exception as err:
			print("hufdhsjl: " + str(type(err)) + str(err))
			return False
		print("Distance" + str(self.cam.distance))
		camMidVar=.05	#a deadzone for boosting
		boost=.4 if moveType else .2 #had .25
		boostInertia=.2
		if(self.cam.mid_x == None or self.cam.noNew >= 5):
			self.autonTankDrive(0, 0)
			if(self.myInertia > 0):
				self.myInertia -= 1
			return False
		elif(abs(self.cam.mid_x - camera.TARGET) > camera.DDZ_ROT):	#radians, arbitrary deadzone value
			spdMag = boost
			if(self.myInertia <= 1):
				spdMag += boostInertia
				print("Speed Boost")
				self.myInertia = 0
			if(self.myInertia <= 5):
				self.myInertia += 1
			spd = math.copysign(spdMag, self.cam.mid_x - camera.TARGET)#min(max(MIN_ROT_SPD, abs(self.mid_x)), MAX_ROT_SPD), self.mid_x)	#again arbitrary numbers
			if moveType:	#shooter
				self.autonTankDrive(spd, -spd)
			else:	#gears
				self.autonTankDrive(spd, spd)	#forward, back -- gear on side
			return False
		self.autonTankDrive(0, 0)
		if(self.myInertia > 0):
			self.myInertia -= 1
		self.savedDistance = self.cam.distance
		return True

	def getCamDistance(self):
		return self.savedDistance

	def offsetRotate(self, dist_HG, dist_CYBRG=12, dist_OFF=5.125):
		theta = math.atan(dist_OFF/(dist_CYBRG + dist_HG))
		return theta + math.atan( (dist_OFF*math.cos(theta) - dist_CYBRG*math.sin(theta) ) / (dist_CYBRG + dist_HG - dist_OFF*math.sin(theta) - dist_CYBRG*math.cos(theta)) )
		#So this is actually BS, it returns the angle the camera should see -- NOT the angle the robot should turn, that's just theta alone.
