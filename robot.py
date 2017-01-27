#!/usr/bin/env python3

import wpilib
from wpilib import RobotDrive
from wpilib import SPI
from xbox import XboxController
from wpilib.smartdashboard import SmartDashboard
#from components.drive import driveTrain
from ctre.cantalon import CANTalon
from robotpy_ext.autonomous.selector import AutonomousModeSelector

## from wpilib import USBCamera, CameraServer


CONTROL_LOOP_WAIT_TIME = 0.025

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):

        self.controller = XboxController(0)
        #self.controller2 = XboxController(1)
        self.gyro = wpilib.ADXRS450_Gyro(0)
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
        #self.drive = RobotDrive()

        #self.drive.reset()

        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        # Initialize Components functions
        self.components = {
                            'drive' : self.drive,
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
            self.i +=1
            wpilib.SmartDashboard.putNumber("test",self.i)


            self.drive.mecanumDrive_Cartesian(self.controller.getLeftX(), self.controller.getLeftY(), self.controller.getRightX(), 0)

            #wpilib.SmartDashboard.putNumber("getAccumulatorValue",self.gyro.spi.getAccumulatorValue())
            #wpilib.SmartDashboard.putNumber("kDegreePerSecond",self.gyro.kDegreePerSecondPerLSB)
            #wpilib.SmartDashboard.putNumber("kSamplePeriod",self.gyro.kSamplePeriod)
            #wpilib.SmartDashboard.putNumber("GyroRate", self.gyro.getRate())

            if(self.gyro.spi == None):
                wpilib.SmartDashboard.putNumber("SPIValue", 0)
            else:
                wpilib.SmartDashboard.putNumber("SPIValue", 1)

    def test(self):

        wpilib.LiveWindow.run()

        self.drive.reset()
        #self.drive.enablePIDs()

        while self.isTest() and self.isEnabled():

            self.drive.xboxTankDrive(self.controller.getLeftY(), self.controller.getRightY())

if __name__ == "__main__":
    wpilib.run(MyRobot)
