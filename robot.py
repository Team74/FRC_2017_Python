"""
File Author: Will Hescott
File Creation Date: 1/8/2017
File Purpose: To create our drive functions


"""
import math
import wpilib
from wpilib import RobotDrive
from wpilib import SPI
from xbox import XboxController
from wpilib.smartdashboard import SmartDashboard
from components.operatorControl import opControl
from components.drive import driveTrain
from ctre.cantalon import CANTalon
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from components import *

from tthhiinnggyy import Tthhinnggyy

## from wpilib import USBCamera, CameraServer

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        self.controller = XboxController(0)
        self.controller2 = XboxController(1)

        self.drive = driveTrain(self)
        self.drive.reset()
        self.opControl = opControl(self)
        #self.drive.reset()
        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        # Initialize Components functions
        self.components = {
                            'opControl' : self.opControl,
                            'drive' : self.drive
                          }
        # Initialize Smart Dashboard
        self.dash = SmartDashboard()
        self.autonomous_modes = AutonomousModeSelector('autonomous', self.components)

    def disabled(self):

        #self.drive.reset()
        #self.drive.disablePIDs()

        while self.isDisabled():
            wpilib.Timer.delay(0.01)              # Wait for 0.01 seconds

    def autonomous(self):

        self.drive.reset()
        self.thng = Tthhinnggyy()
        #self.drive.enablePIDs()

        while self.isAutonomous() and self.isEnabled():
            #self.autonomous_modes.run()
            self.thng.receive()
            if thng.centerSide() and thng.centerLine() :	#this works because of short-circuiting
                print("hooboyshoot")

    def operatorControl(self):
        # Resetting encoders
        #self.drive.enablePIDs()
        self.opControl.setSpeed()
        while self.isOperatorControl() and self.isEnabled():
            wpilib.SmartDashboard.putNumber("GyroAngle",self.drive.getGyroAngle())
            wpilib.SmartDashboard.putNumber("Intake Speed",self.drive.getIntakeSpeed())
            wpilib.SmartDashboard.putNumber("Distance", self.drive.getDistance())
            wpilib.SmartDashboard.putNumber("ShooterSpeed", self.opControl.getSpeed())
            self.drive.drive(self.scaleInput(self.controller.getLeftX()), self.scaleInput(self.controller.getLeftY()),self.scaleInput(self.controller.getRightX()))
            if(self.controller.getButtonX() == True):
                self.drive.zeroGyro()

            self.opControl.operatorFunctions(self.controller2.getButtonA(), self.controller2.getButtonB(), self.controller2.getButtonX(), self.controller2.getButtonY(), self.controller2.getLeftY(), self.controller2.getRightTrigger(), self.controller2.getRightBumper(), self.controller2.getLeftTrigger())
            #wpilib.SmartDashboard.putNumber("getAccumulatorValue",self.gyro.spi.getAccumulatorValue())
            #wpilib.SmartDashboard.putNumber("kDegreePerSecond",self.gyro.kDegreePerSecondPerLSB)
            #wpilib.SmartDashboard.putNumber("kSamplePeriod",self.gyro.kSamplePeriod)
            #wpilib.SmartDashboard.putNumber("GyroRate", self.gyro.getRate())

    def scaleInput(self, x):
        negativeOutput = False
        if(x<0):
            negativeOutput = True
        x = abs(x)
        x = x*math.pow(100,x-1.05)+(0.206*x)
        if(negativeOutput == True):
            return x*-1
        else:
            return x


    def test(self):

        wpilib.LiveWindow.run()

        self.drive.reset()
        #self.drive.enablePIDs()

        while self.isTest() and self.isEnabled():

            self.drive.xboxTankDrive(self.controller.getLeftY(), self.controller.getRightY())

'''
    class autonomus(lfmotor, lbmotor, rbmotor, rfmotor):
        def _autonInit_()

        def turnAngle()
            if():

'''

if __name__ == "__main__":
    wpilib.run(MyRobot)
