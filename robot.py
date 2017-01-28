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
#from components.drive import driveTrain
from ctre.cantalon import CANTalon
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from components import *

## from wpilib import USBCamera, CameraServer


CONTROL_LOOP_WAIT_TIME = 0.025

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):

        self.controller = XboxController(0)
        self.controller2 = XboxController(1)
        self.gyro = wpilib.ADXRS450_Gyro(0)
        self.gyro.calibrate()
        self.gyroInit = False
        self.i = 1
        self.lfmotor = CANTalon(1)
        self.lbmotor = CANTalon(2)
        self.rfmotor = CANTalon(3)
        self.rbmotor = CANTalon(0)
        self.rfmotor.enableBrakeMode(True)
        self.rbmotor.enableBrakeMode(True)
        self.lfmotor.enableBrakeMode(True)
        self.lbmotor.enableBrakeMode(True)

        self.drive = wpilib.RobotDrive(self.lfmotor, self.lbmotor, self.rfmotor, self.rbmotor)
        #self.opControl = operatorControl.opControl()

        #self.drive.reset()

        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        # Initialize Components functions
        self.components = {
                            #'opControl' : self.opControl
                            }

        # Initialize Smart Dashboard
        self.dash = SmartDashboard()
        self.autonomous_modes = AutonomousModeSelector('autonomous', self.components)

        #self.drive.log()


    def disabled(self):

        #self.drive.reset()
        #self.drive.disablePIDs()

        while self.isDisabled():
            wpilib.Timer.delay(0.01)              # Wait for 0.01 seconds

    def autonomous(self):

        self.drive.reset()
        #self.drive.enablePIDs()

        while self.isAutonomous() and self.isEnabled():

            # Run the actual autonomous mode
            #self.drive.log()
            self.autonomous_modes.run()

    def operatorControl(self):
        # Resetting encoders
        #self.drive.enablePIDs()
        while self.isOperatorControl() and self.isEnabled():
            wpilib.SmartDashboard.putNumber("GyroAngle",self.gyro.getAngle())

            self.drive.mecanumDrive_Cartesian(self.scaleInput(self.controller.getLeftX()), self.scaleInput(self.controller.getLeftY()),self.scaleInput(self.controller.getRightX()), self.gyro.getAngle())
            if(self.controller.getButtonX() == True):
                self.gyro.reset()
            #self.components.opControl.operatorFunctions(self.controller2.getAButton(), self.controller2.getBButton(), self.controller2.getXButton(), self.controller2.getLeftY(), self.controller2.getRightTrigger, self.controller2.getRightBumper)
            #wpilib.SmartDashboard.putNumber("getAccumulatorValue",self.gyro.spi.getAccumulatorValue())
            #wpilib.SmartDashboard.putNumber("kDegreePerSecond",self.gyro.kDegreePerSecondPerLSB)
            #wpilib.SmartDashboard.putNumber("kSamplePeriod",self.gyro.kSamplePeriod)
            #wpilib.SmartDashboard.putNumber("GyroRate", self.gyro.getRate())

            if(self.gyro.spi == None):
                wpilib.SmartDashboard.putNumber("SPIValue", 0)
            else:
                wpilib.SmartDashboard.putNumber("SPIValue", 1)

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

if __name__ == "__main__":
    wpilib.run(MyRobot)
