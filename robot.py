#!/usr/bin/env python3
import wpilib
from xbox import XboxController
from wpilib.smartdashboard import SmartDashboard
from components.drive import driveTrain
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import USBCamera, CameraServer

CONTROL_LOOP_WAIT_TIME = 0.025

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        self.controller = XboxController(0)
        self.controller2 = XboxController(1)

        #self.lmotor = wpilib.CANTalon(1)
        #self.rmotor = wpilib.CANTalon(0)

        self.drive = driveTrain(self)

        self.drive.reset()

        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        # Initialize Components functions
        self.components = {
                            'drive' : self.drive,
                            }

        # Initialize Smart Dashboard
        self.dash = SmartDashboard()
        self.autonomous_modes = AutonomousModeSelector('autonomous', self.components)

        self.drive.log()


    def disabled(self):
        self.drive.reset()
        #self.drive.disablePIDs()

        while self.isDisabled():
            wpilib.Timer.delay(0.01)              # Wait for 0.01 seconds

    def autonomous(self):
        self.drive.reset()
        self.drive.enablePIDs()

        while self.isAutonomous() and self.isEnabled():

            # Run the actual autonomous mode
            self.drive.log()
            self.autonomous_modes.run()

    def operatorControl(self):
        # Resetting encoders

        self.drive.reset()
        #self.drive.enablePIDs()

        while self.isOperatorControl() and self.isEnabled():
            self.drive.xboxTankDrive(self.controller.getLeftY(), self.controller.getRightY(), self.controller.getLeftBumper(), self.controller.getRightBumper(), self.controller.getLeftTrigger(), self.controller.getRightTrigger())

            self.drive.log()

            wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)

    def test(self):
        wpilib.LiveWindow.run()

        self.drive.reset()
        self.drive.enablePIDs()

        while self.isTest() and self.isEnabled():

            self.drive.xboxTankDrive(self.controller.getLeftY(), self.controller.getRightY(), self.controller.getLeftBumper(), self.controller.getRightBumper(), self.controller.getLeftTrigger(), self.controller.getRightTrigger())

    '''
    def checkPixy():
        distanceFromCenter = 0
        closestBallArea = 0 #meaningless number that any result returned by the function can always beat
        biggestBallID = None
        blocks = self.pixy.getBlocks()

        for i in range(0, len(blocks)):
            area = blocks[i].getArea()
            if(area > closestBallArea):
                closestBallArea = area
                biggestBallID = i
       if(controller.getLeftTriggerRaw() > 0.75):
            distanceFromCenter = blocks[BiggestballID] - 180

            if(distanceFromCenter < 0):#turn right
                self.drive.turnAngle(-2)
            elif(distanceFromCenter > 0):#turn left
                self.drive.turnAngle(2)
    '''

if __name__ == "__main__":
    wpilib.run(MyRobot)
