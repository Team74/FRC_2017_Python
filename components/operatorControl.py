"""
File Author: Will Hescott
File Creation Date: 1/25/2017
File Purpose: To create and run our operator functions
"""

import wpilib

from wpilib import Encoder, Timer, RobotDrive, Spark, DigitalOutput, Relay
from ctre.cantalon import CANTalon
from wpilib.interfaces import Gyro
from . import Component

class opControl(Component):

    def __init__(self, robot):
        super().__init__()

        self.wait = 0
        self.wait2 = 0
        self.wait3 = 0
        #self.ShooterSpeed = 1
        self.ShooterFeedSpeed = 1
        self.intakeToggle = False
        self.shooterToggle = True
        self.lights = True
        self.shooterSpeed = .65

        #self.flash1 = DigitalOutput(0)
        self.flash1 = Relay(0)
        self.flash2 = DigitalOutput(1)
        self.frontIntake = CANTalon(3)
        self.shooterMain = CANTalon(5)
        self.shooterFeed = CANTalon(4)
        self.climberMotor = CANTalon(8) # This may not be nessecary depending upon how we decide to deploy the climber
        self.shooterMain.set(self.shooterSpeed)
        '''
        self.frontIntake.enableBrakeMode(True)
        self..enableBrakeMode(True)
        self.shooterMain.enableBrakeMode(True)
        self.shooterFeed.enableBrakeMode(True)
        self.climberMotor.enableBrakeMode(True)
        self.releaseMotor.enableBrakeMode(True)

    def getSpeed(self):
        return self.shooterSpeed

    def modifySpeed(self, rightTrigger, leftTrigger):
        if(rightTrigger):
            self.shooterSpeed = self.shooterSpeed + 0.01
            self.shooterMain.set(self.shooterSpeed)
            print("right trigger looping")
        if(leftTrigger):
            self.shooterSpeed= self.shooterSpeed- 0.01
            self.shooterMain.set(self.shooterSpeed)
            print ("left Trigger Looping")

    def setSpeed(self):
        self.shooterSpeed = 0.5
        '''

    def getShooter(self):
        return self.shooterToggle

    def toggleIntake(self, aButton):#the wait is because under normal circumstances the code will cycle twice, so when you press the button it turns the intake off and on before you can release the button
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
                self.frontIntake.set(1)
        else:
                self.frontIntake.set(0)

    def toggleLights(self, yButton): #wait is implemented for the same reason as above, if it isnt implemented below it probably needs to be.
        if(self.wait2>0):
            self.wait2-=1
        elif(self.wait2<=0):
            if(yButton and self.lights == False):
                #self.flash1.set(Relay.Value.kOn)
                self.flash1.set(Relay.Value.kOn)
                self.flash2.set(True)
                self.wait2 = 25
                print ('Lights_On')
                self.lights = True
            elif(yButton and self.lights == True):
                #self.flash1.set(Relay.Value.Off)
                self.flash1.set(Relay.Value.kOff)
                self.flash2.set(False)
                self.wait2 = 25
                print ('Lights_Off')
                self.lights = False
            else:
                pass
                '''
    def reverseIntake(self, bButton):# reverses the intake in case we need to dump our balls onto the field (probably in case of climbing)
        if(bButton):
            self.frontIntake.set(self.intakeToggle*(-1))
        else:
            pass
            '''
    def toggleShooter(self, xButton):#switches the front motors on or off
        if(self.wait>0):
            self.wait-=1
        elif(self.wait<=0):
            if(xButton and self.shooterToggle == False):
                self.shooterToggle = True
                self.wait = 20
            elif(xButton and self.shooterToggle == True):
                self.shooterToggle = False
                self.wait = 20
            else:
                pass
            if(self.shooterToggle == True):
                self.shooterMain.set(self.shooterSpeed)

            elif(self.shooterToggle == False):
                self.shooterMain.set(0)

    def fire(self, rightTrigger):
            self.shooterFeed.set(int(rightTrigger))

    def singleFire(self,leftTrigger):#single ball fire for testing
        if(leftTrigger and self.wait3 < 30):
            self.shooterFeed.set(1)
            self.wait3+=1
        else:
            self.shooterFeed.set(0)

    def climb(self, climberStick):#using a stick because we ran out of buttons on the controller
        self.climberMotor.set(climberStick)


    def operatorFunctions(self, aButton, bButton, xButton, yButton, climberStick, rightTrigger,leftTrigger): #rightBumper= agitator
        #self.modifySpeed(rightTrigger,leftTrigger)
        print(self.lights)
        self.toggleIntake(aButton)
        self.toggleLights(yButton)
        #self.reverseIntake(bButton)
        self.toggleShooter(xButton)
        self.fire(rightTrigger)
        self.climb(climberStick)
