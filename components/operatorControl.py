"""
File Author: Will Hescott
File Creation Date: 1/25/2017
File Purpose: To create and run our operator functions
"""

import wpilib

from wpilib import Encoder, Timer, RobotDrive, Spark
from ctre.cantalon import CANTalon
from wpilib.interfaces import Gyro
from . import Component


class opControl(Component) :



    def __init__(self, robot):
        super().__init__()

        # Constants
        CONTROL_LOOP_WAIT_TIME = 0.025
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
        self.wait = 0
        self.ShooterSpeed = 1
        self.ShooterFeedSpeed = .20
        self.intakeToggle = False
        self.shooterToggle = True

        self.frontIntake = Spark(4)
        self.backIntake = Spark(5)
        self.shooterMain = Spark(6)
        self.shooterSecondary = Spark(7)
        self.shooterFeed = Spark(8)
        self.climberMotor = Spark(9)
        self.releaseMotor = Spark(10) # This may not be nessecary depending upon how we decide to deploy the climber
        self.agitator = Spark(11)
        '''
        self.frontIntake.enableBrakeMode(True)
        self.backIntake.enableBrakeMode(True)
        self.shooterMain.enableBrakeMode(True)
        self.shooterSecondary.enableBrakeMode(True)
        self.shooterFeed.enableBrakeMode(True)
        self.climberMotor.enableBrakeMode(True)
        self.releaseMotor.enableBrakeMode(True)
        '''

    def operatorFunctions(self, aButton, bButton, xButton, climberStick, rightTrigger,agitatorBumper): #rightBumper= agitator
        if(self.wait>0):
            self.wait-=1
        elif(self.wait<=0):
            if(aButton and self.intakeToggle == False):
                self.intakeToggle = True
                self.wait = 20
            elif(aButton and self.intakeToggle == True):
                self.intakeToggle = False
                self.wait = 20
            else:
                pass
        if(self.intakeToggle == True):
                self.frontIntake.set(0.75)
                self.backIntake.set(0.75)
        else:
                self.frontIntake.set(0)
                self.backIntake.set(0)



        if(bButton):
            self.frontIntake.set(self.intakeToggle*(-1))
        else:
            pass

        if(xButton and ShooterToggle == True):
            self.ShooterToggle = False
        elif(xButton and ShooterToggle == False):
            self.ShooterToggle = True

        self.shooterMain.set(self.ShooterSpeed)

        self.shooterSecondary.set(self.ShooterFeedSpeed)

        if(rightTrigger):
            self.shooterFeed.set(1)

        self.climberMotor.set(climberStick)
        if(agitatorBumper == True):
            self.agitator.set(1)
