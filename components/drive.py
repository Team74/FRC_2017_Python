"""
File Author: Will Hescott
File Creation Date: 1/25/2017
File Purpose: To create and run our drive functions
"""

import wpilib
from wpilib import Encoder, Timer, RobotDrive, Spark, DigitalOutput
from ctre.cantalon import CANTalon
from wpilib.interfaces import Gyro
from . import Component
from tthhiinnggyy import Tthhinnggyy


class driveTrain(Component):

    def __init__(self, robot):
        super().__init__()
        self.INCHES_PER_REV = 18.849
        self.robot = robot
        self.gyro = wpilib.ADXRS450_Gyro(0)
        self.gyro.calibrate()
        self.intakeOn = False
        self.intakeSpeed = .5
        self.i = 1
        self.lfmotor = CANTalon(1)
        self.lbmotor = CANTalon(2)
        self.rfmotor = CANTalon(3)
        self.rbmotor = CANTalon(0)

        self.robotDrive = RobotDrive(self.lfmotor, self.lbmotor, self.rfmotor, self.rbmotor)
        self.rfmotor.enableBrakeMode(True)
        self.rbmotor.enableBrakeMode(True)
        self.lfmotor.enableBrakeMode(True)
        self.lbmotor.enableBrakeMode(True)
        #self.rfmotor.setInverted(True)
        #self.lfmotor.setInverted(False)
        #self.rbmotor.setInverted(True)
        #self.lbmotor.setInverted(False)
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

        self.thng = Tthhinnggyy(self.drive)

    def drive_forward(self, speed) :
        self.drive.tankDrive(speed, speed, True)
    def autonTankDrive(self, leftSpeed, rightSpeed):
        self.lfmotor.set(leftSpeed)
        self.lbmotor.set(leftSpeed)
        self.rfmotor.set(rightSpeed)
        self.rbmotor.set(rightSpeed)
    def drive_stop(self):
        self.drive.tankDrive(0,0)
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

    def turnAngle(self, degrees):

        if(self.gyro.getAngle() > degrees+1):
            self.autonTankDrive(-0.2, 0.2)
            print(self.gyro.getAngle())
        elif(self.gyro.getAngle() < degrees-1):
            self.autonTankDrive(0.2, -0.2)
            print(self.gyro.getAngle())
        else:
            return True
        return False

    def visionLineUp(self):
        self.thng.receive()
        if self.thng.centerSide():#and self.thng.centerLine() :	#this works because of short-circuiting
            print("hooboyshoot")

    def drive(self, leftX, leftY, rightX):
            self.robotDrive.mecanumDrive_Cartesian(leftX*.75, leftY*.75, rightX*.75, self.gyro.getAngle())

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
        wpilib.SmartDashboard.putNumber("rf",self.rfmotor.getPosition())
        wpilib.SmartDashboard.putNumber("rb",self.rbmotor.getPosition())
        wpilib.SmartDashboard.putNumber("lf",self.lfmotor.getPosition()*-1)
        wpilib.SmartDashboard.putNumber("lb",self.lbmotor.getPosition()*-1)
        return (self.convertEncoderRaw(self.rfmotor.getPosition())
                + self.convertEncoderRaw(self.rbmotor.getPosition())
                + self.convertEncoderRaw(self.lfmotor.getPosition()*-1)
                + self.convertEncoderRaw(self.lbmotor.getPosition()*-1))/4
        #detirmines how many ticks the encoder has processed
        #converts ticks from getMotorDistance into inches

    def convertEncoderRaw(self, selectedEncoderValue):
        return selectedEncoderValue * self.INCHES_PER_REV
