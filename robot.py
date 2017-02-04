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
from ctre.cantalon import CANTalon
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from components import *

## from wpilib import USBCamera, CameraServer


controller = XboxController(0)
controller2 = XboxController(1)
gyro = wpilib.ADXRS450_Gyro(0)
gyro.calibrate()
intakeOn = False
intakeSpeed = .5
i = 1
lfmotor = CANTalon(1)
lbmotor = CANTalon(2)
rfmotor = CANTalon(3)
rbmotor = CANTalon(0)

rfmotor.enableBrakeMode(True)
rbmotor.enableBrakeMode(True)
lfmotor.enableBrakeMode(True)
lbmotor.enableBrakeMode(True)

rfmotor.setInverted(True)
rbmotor.setInverted(True)
lfmotor.setInverted(True)
lbmotor.setInverted(True)

rfmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
rbmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
lfmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
lbmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)

#setting up the distances per rotation
lfmotor.configEncoderCodesPerRev(4096)
rfmotor.configEncoderCodesPerRev(4096)
lbmotor.configEncoderCodesPerRev(4096)
rbmotor.configEncoderCodesPerRev(4096)

rfmotor.setPosition(0)
rbmotor.setPosition(0)
lfmotor.setPosition(0)
lbmotor.setPosition(0)


class MyRobot(wpilib.SampleRobot, lfmotor, lbmotor, rbmotor, rfmotor, controller, controller2):

    def robotInit(self):
        self.drive = wpilib.RobotDrive(self.lfmotor, self.lbmotor, self.rfmotor, self.rbmotor)
        self.opControl = opControl(self)

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
            wpilib.SmartDashboard.putNumber("Intake Speed",self.intakeSpeed)
            wpilib.SmartDashboard.putNumber("Left Front Encoder", self.lfmotor.getEncPosition())
            wpilib.SmartDashboard.putNumber("Right Front Encoder", self.lbmotor.getEncPosition())
            wpilib.SmartDashboard.putNumber("Left Back Encoder", self.rfmotor.getEncPosition())
            wpilib.SmartDashboard.putNumber("Right Back Encoder", self.rbmotor.getEncPosition())

            self.drive.mecanumDrive_Cartesian(self.scaleInput(self.controller.getLeftX()), self.scaleInput(self.controller.getLeftY()),self.scaleInput(self.controller.getRightX()*-1), self.gyro.getAngle())
            if(self.controller.getButtonX() == True):
                self.gyro.reset()

            self.opControl.operatorFunctions(self.controller2.getButtonA(), self.controller2.getButtonB(), self.controller2.getButtonX(), self.controller2.getLeftY(), self.controller2.getRightTrigger, self.controller2.getRightBumper)
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
