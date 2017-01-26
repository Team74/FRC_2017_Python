"""
File Author: Will Lowry, Will Hescott
File Creation Date: 1/28/2015
File Purpose: To create our drive functions

Transmission gear ratio: 18.74/1

"""

import wpilib

from wpilib import Encoder, Timer, RobotDrive
from ctre.cantalon import CANTalon
from wpilib.interfaces import Gyro
from . import Component


class driveTrain(Component) :

    def __init__(self, robot):
        super().__init__()

        # Constants
        WHEEL_DIAMETER = 8
        PI = 3.1415
        ENCODER_TICK_COUNT_250 = 250
        ENCODER_TICK_COUNT_360 = 360
        ENCODER_GOAL = 0 # default
        ENCODER_TOLERANCE = 1 # inch0
        self.RPM = 4320/10.7
        self.INCHES_PER_REV = WHEEL_DIAMETER * 3.1415
        self.INCHES_PER_DEGREE = (24 * PI)/360
        self.CONTROL_TYPE = False # False = disable PID components
        self.LEFTFRONTCUMULATIVE = 0
        self.LEFTBACKCUMULATIVE = 0
        self.RIGHTFRONTCUMULATIVE = 0
        self.RIGHTBACKCUMULATIVE = 0

        self.rfmotor = CANTalon(2)#2
        self.rbmotor = CANTalon(1)#1
        self.lfmotor = CANTalon(0)#0
        self.lbmotor = CANTalon(3)#3

        #self.lfmotor.reverseOutput(True)#leftback
        self.lbmotor.reverseOutput(True)#rightfront
        self.rfmotor.reverseOutput(True)#leftBack
        self.rbmotor.reverseOutput(True)#left front

        self.rfmotor.enableBrakeMode(True)
        self.rbmotor.enableBrakeMode(True)
        self.lfmotor.enableBrakeMode(True)
        self.lbmotor.enableBrakeMode(True)

        absolutePosition = self.lbmotor.getPulseWidthPosition() & 0xFFF; # mask out the bottom12 bits, we don't care about the wrap arounds use the low level API to set the quad encoder signal
        self.lbmotor.setEncPosition(absolutePosition)
        absolutePosition = self.lfmotor.getPulseWidthPosition() & 0xFFF; # mask out the bottom12 bits, we don't care about the wrap arounds use the low level API to set the quad encoder signal
        self.lfmotor.setEncPosition(absolutePosition)
        absolutePosition = self.rbmotor.getPulseWidthPosition() & 0xFFF; # mask out the bottom12 bits, we don't care about the wrap arounds use the low level API to set the quad encoder signal
        self.rbmotor.setEncPosition(absolutePosition)
        absolutePosition = self.rfmotor.getPulseWidthPosition() & 0xFFF; # mask out the bottom12 bits, we don't care about the wrap arounds use the low level API to set the quad encoder signal
        self.rfmotor.setEncPosition(absolutePosition)

        self.rfmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
        self.rbmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
        self.lfmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
        self.lbmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)

        #setting up the distances per rotation
        self.lfmotor.configEncoderCodesPerRev(4096)
        self.rfmotor.configEncoderCodesPerRev(4096)
        self.lbmotor.configEncoderCodesPerRev(4096)
        self.rbmotor.configEncoderCodesPerRev(4096)

        self.lfmotor.setPID(0.0005, 0, 0.0, profile=0)
        self.rfmotor.setPID(0.0005, 0, 0.0, profile=0)
        self.lbmotor.setPID(0.0005, 0, 0.0, profile=0)
        self.rbmotor.setPID(0.0005, 0, 0.0, profile=0)

        self.lbmotor.configNominalOutputVoltage(+0.0, -0.0)
        self.lbmotor.configPeakOutputVoltage(+12.0, -12.0)
        self.lbmotor.setControlMode(CANTalon.ControlMode.Speed)

        self.lfmotor.configNominalOutputVoltage(+0.0, -0.0)
        self.lfmotor.configPeakOutputVoltage(+12.0, -12.0)
        self.lfmotor.setControlMode(CANTalon.ControlMode.Speed)

        self.rbmotor.configNominalOutputVoltage(+0.0, -0.0)
        self.rbmotor.configPeakOutputVoltage(+12.0, -12.0)
        self.rbmotor.setControlMode(CANTalon.ControlMode.Speed)

        self.rfmotor.configNominalOutputVoltage(+0.0, -0.0)
        self.rfmotor.configPeakOutputVoltage(+12.0, -12.0)
        self.rfmotor.setControlMode(CANTalon.ControlMode.Speed)

        self.rfmotor.setPosition(0)
        self.rbmotor.setPosition(0)
        self.lfmotor.setPosition(0)
        self.lbmotor.setPosition(0)

        self.lfmotor.reverseSensor(True)
        self.lbmotor.reverseSensor(True)

        if self.CONTROL_TYPE:

            # Initializing PID Controls
            self.pidRightFront = wpilib.PIDController(0.002, 0.8, 0.005, 0, self.rfmotor.feedbackDevice, self.rfmotor, 0.02)
            self.pidLeftFront = wpilib.PIDController(0.002, 0.8, 0.005, 0, self.lfmotor.feedbackDevice, self.lfmotor, 0.02)
            self.pidRightBack = wpilib.PIDController(0.002, 0.8, 0.005, 0, self.rbmotor.feedbackDevice, self.rbmotor, 0.02)
            self.pidLeftBack = wpilib.PIDController(0.002, 0.8, 0.005, 0, self.lbmotor.feedbackDevice, self.lbmotor, 0.02)

            # PID Absolute Tolerance Settings
            self.pidRightFront.setAbsoluteTolerance(0.05)
            self.pidLeftFront.setAbsoluteTolerance(0.05)
            self.pidRightBack.setAbsoluteTolerance(0.05)
            self.pidLeftBack.setAbsoluteTolerance(0.05)

            # PID Output Range Settings
            self.pidRightFront.setOutputRange(-1, 1)
            self.pidLeftFront.setOutputRange(-1, 1)
            self.pidRightBack.setOutputRange(-1, 1)
            self.pidLeftBack.setOutputRange(-1, 1)

            # Enable PID
            #self.enablePIDs()


        self.dashTimer = Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        #def log(self):
        #The log method puts interesting information to the SmartDashboard. (like velocity information)
        # Turns out none of that worked, life is meaningless, the universe is a hologram, nothing matters.
        # drive forward function

    def drive_forward(self, speed) :
        #self.drive.tankDrive(speed, speed, True)
        pass
        # manual drive function for Tank Drive

    def xboxTankDrive(self, leftY, leftX, rightX):
            # Creating margin for error when using the joysticks, as they're quite sensitive
        '''
        if abs(rightSpeed) < 0.04 :
            rightSpeed = 0
        if abs(leftSpeed) < 0.04 :
            leftSpeed = 0
        '''
        if (self.CONTROL_TYPE):
            self.pidRightFront.setSetpoint(rightSpeed)
            self.pidRightBack.setSetpoint(rightSpeed)
            self.pidLeftFront.setSetpoint(leftSpeed)
            self.pidLeftBack.setSetpoint(leftSpeed)
        elif(abs(rightX) > abs(leftX) and abs(rightX) > abs(leftY)):
            if(rightX > abs(.1)):
                self.rfmotor.set(-1*abs(rightX)*300)
                self.rbmotor.set(-1*abs(rightX)*300)
                self.lfmotor.set(abs(rightX)*300)
                self.lbmotor.set(abs(rightX)*300)
            elif(rightX < abs(.1)):
                self.rfmotor.set(abs(rightX)*300)
                self.rbmotor.set(abs(rightX)*300)
                self.lfmotor.set(-1*abs(rightX)*300)
                self.lbmotor.set(-1*abs(rightX)*300)
            else:
                self.rfmotor.set(0)
                self.rbmotor.set(0)
                self.lfmotor.set(0)
                self.lbmotor.set(0)

        elif(abs(leftX) > abs(leftY) and abs(leftX) > abs(.04)):
            self.rfmotor.set((leftX)*512)
            self.rbmotor.set((leftX)*(-1)*512)
            self.lfmotor.set((leftX)*(-1)*512)
            self.lbmotor.set((leftX)*512)
        elif(abs(leftY) > abs(leftX) and abs(leftY) > abs(.04)):
            self.rfmotor.set(leftY*512)
            self.rbmotor.set(leftY*512)
            self.lfmotor.set(leftY*512)
            self.lbmotor.set(leftY*512)

        else:
            self.rfmotor.set(0)
            self.rbmotor.set(0)
            self.lfmotor.set(0)
            self.lbmotor.set(0)




            '''
            self.lfmotor.set(leftSpeed*512)#512 relates to the gear ratio on the motors
            self.rfmotor.set(rightSpeed*512)
            self.lbmotor.set(leftSpeed*512)
            self.rbmotor.set(rightSpeed*512)
            '''
            #autononmous tank drive (to remove a need for a slow, striaght, or fast button)
    def autonStraightDrive(self, leftSpeed, rightSpeed):

        self.log()
        #self.drive.tankDrive(leftSpeed, rightSpeed, True)
        self.rfmotor.set(rightSpeed)# was multiplying final by -512
        self.rbmotor.set(rightSpeed)#^
        self.lfmotor.set(leftSpeed)#^
        self.lbmotor.set(leftSpeed)#^


        # stop function
    def drive_stop(self) :
        self.drive.tankDrive(0,0)

# function to reset the PID's and encoder values
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

        if self.CONTROL_TYPE:
            self.pidLeftBack.setSetpoint(0)
            self.pidLeftFront.setSetpoint(0)
            self.pidRightBack.setSetpoint(0)
            self.pidRightFront.setSetpoint(0)

        # def getDistance(self)
        #    return (abs(self.convertEncoderRaw(LEFTFRONTCUMULATIVE) + abs(self.convertEncoderRaw(LEFTBACKCUMULATIVE)) + abs(self.convertEncoderRaw(RIGHTFRONTCUMULATIVE)) + abs(self.convertEncoderRaw(RIGHTBACKCUMULATIVE)))

    def turn_angle(self, degrees):

        desired_inches = self.INCHES_PER_DEGREE * abs(degrees)
        wpilib.SmartDashboard.putNumber("Auton Distance", self.getAutonDistance()/2)
        if degrees < 0:
            if(self.getAutonDistance()/2 <= desired_inches):
                self.autonTankDrive(-0.4, 0.4)
        elif degrees > 0:
            if (self.getAutonDistance()/2 <= desired_inches):
                self.autonTankDrive(0.4, -0.4)

        return (self.getAutonDistance()/2 <= desired_inches)


    def getAutonDistance(self):

        return (self.convertEncoderRaw(abs(self.rfmotor.getPosition()*0.57))
                + self.convertEncoderRaw(abs(self.rbmotor.getPosition()*0.57))
                + self.convertEncoderRaw(abs(self.lfmotor.getPosition()*0.57))
                + self.convertEncoderRaw(abs(self.lbmotor.getPosition()*0.57)))/4

        #converts ticks from getMotorDistance into inches
    def convertEncoderRaw(self, selectedEncoderValue):
        return selectedEncoderValue * self.INCHES_PER_REV