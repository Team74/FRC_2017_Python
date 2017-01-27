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

        self.frontIntake = CANTalon(4)
        self.backIntake = CANTalon(5)
        self.shooterMain = CANTalon(6)
        self.shooterSecondary = CANTalon(7)
        self.shooterFeed = CANTalon(8)
        self.climberMotor = CANTalon(9)
        self.releaseMotor = CANTalon(10) # This may not be nessecary depending upon how we decide to deploy the climber


        self.frontIntake.enableBrakeMode(True)
        self.backIntake.enableBrakeMode(True)
        self.shooterMain.enableBrakeMode(True)
        self.shooterSecondary.enableBrakeMode(True)
        self.shooterFeed.enableBrakeMode(True)
        self.climberMotor.enableBrakeMode(True)
        self.releaseMotor.enableBrakeMode(True)


    def operatorFunctions(self, aButton, bButton, xButton, climberStick, rightTrigger, agitator):

            IntakeToggle = False
            if(aButton and IntakeToggle == False):
                IntakeToggle = True
            elif(aButton and IntakeToggle == True):
                IntakeToggle = False
            else:
                pass

            frontIntake.set(IntakeToggle)
            backIntake.set(IntakeToggle)
