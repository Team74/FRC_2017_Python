"""
File Author: Will Hescott
File Creation Date: 1/25/2017
File Purpose: To create and run our operator functions
"""

import wpilib

from wpilib import Encoder, Timer, RobotDrive, Spark, DigitalOutput
from ctre.cantalon import CANTalon
from wpilib.interfaces import Gyro
from . import Component

class opControl(Component):

    def __init__(self, robot):
        super().__init__()

        self.wait = 0
        self.wait2 = 0
        #self.ShooterSpeed = 1
        self.ShooterFeedSpeed = .20
        self.intakeToggle = False
        self.shooterToggle = True
        self.lights = True
        self.shooterSpeed = .5

        self.flash1 = DigitalOutput(0)
        self.flash2 = DigitalOutput(1)
        self.frontIntake = Spark(4)
        self.backIntake = Spark(5)
        self.shooterMain = Spark(6)
        self.shooterSecondary = Spark(7)
        self.shooterFeed = Spark(8)
        self.climberMotor = Spark(9)
        self.releaseMotor = Spark(10) # This may not be nessecary depending upon how we decide to deploy the climber
        self.agitator = Spark(11)
        self.shooterMain.set(self.shooterSpeed)

        '''
        self.frontIntake.enableBrakeMode(True)
        self.backIntake.enableBrakeMode(True)
        self.shooterMain.enableBrakeMode(True)
        self.shooterSecondary.enableBrakeMode(True)
        self.shooterFeed.enableBrakeMode(True)
        self.climberMotor.enableBrakeMode(True)
        self.releaseMotor.enableBrakeMode(True)
        '''
    def getSpeed(self):
        return self.shooterSpeed

    def modifySpeed(self, rightTrigger, leftTrigger):
        if(rightTrigger):
            self.shooterSpeed = self.shooterSpeed + .01
            self.shooterMain.set(self.shooterSpeed)
            print("right trigger looping")
        if(leftTrigger):
            self.shooterSpeed= self.shooterSpeed- .01
            self.shooterMain.set(self.shooterSpeed)
            print ("left Trigger Looping")

    def setSpeed(self):
        self.shooterSpeed = .5
        '''
    def getShooter(self):
        return self.shooterToggle

    def toggleIntake(self, aButton):
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

    def toggleLights(self, yButton):
        if(self.wait2>0):
            self.wait2-=1
        elif(self.wait2<=0):
            if(yButton and self.lights == False):
                self.light.set(True)
                self.light2.set(True)
                self.lights = True
            elif(yButton and self.lights == True):
                self.light.set(False)
                self.light2.set(False)
                self.lights = False
            else:
                pass

    def reverseIntake(self, bButton):
        if(bButton):
            self.frontIntake.set(self.intakeToggle*(-1))
        else:
            pass

    def toggleShooter(self, xButton):
        if(xButton and ShooterToggle == True):
            self.ShooterToggle = False
        elif(xButton and ShooterToggle == False):
            self.ShooterToggle = True

        self.shooterMain.set(self.ShooterSpeed)

        self.shooterSecondary.set(self.ShooterFeedSpeed)

    def fire(self, rightTrigger):
        if(rightTrigger):
            self.shooterFeed.set(1)
    def climb(self, climberStick):
        self.climberMotor.set(climberStick)

    def agitate(self, agitatorBumper):
        if(agitatorBumper == True):
            self.agitator.set(1)
'''
    def operatorFunctions(self, aButton, bButton, xButton, yButton, climberStick, rightTrigger,agitatorBumper,leftTrigger): #rightBumper= agitator
        self.modifySpeed(rightTrigger,leftTrigger)

        '''
            self.toggleIntake(aButton)
            self.toggleLights(bButton)
            self.reverseIntake(xButton)
            self.toggleShooter(yButton)
            self.fire(rightTrigger)
            self.climb(climberStick)
            self.agitate(agitatorBumper)
            '''
