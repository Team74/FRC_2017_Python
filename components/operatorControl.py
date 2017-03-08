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
        self.MAX_SPEED = 1
        self.MIN_SPEED = .65
        self.MAX_RANGE = 90
        self.MIN_RANGE = 50
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
        self.shooterSlave = CANTalon(8)
        self.shooterFeed = CANTalon(4)
        self.shooterMain.set(self.shooterSpeed)
        self.climberMotor = CANTalon(9)

        self.shooterMain.configEncoderCodesPerRev(4096)
        self.shooterMain.configNominalOutputVoltage(+0.0, -0.0)
        self.shooterMain.configPeakOutputVoltage(+12.0, -12.0)
        self.shooterMain.setAllowableClosedLoopErr(0)
        self.shooterMain.setProfile(0)
        self.shooterMain.setF(0.0)
        self.shooterMain.setP(0.01)
        self.shooterMain.setI(0.0)
        self.shooterMain.setD(0.0)
        self.shooterMain.setControlMode(CANTalon.ControlMode.Speed)
        self.shooterMain.set(5)

        self.shooterSlave.setControlMode(CANTalon.ControlMode.Follower)
        self.shooterSlave.set(5)

        self.shooterMain.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
        self.shooterMain.setEncPosition(CANTalon.FeedbackDevice.PulseWidth)
        '''
        self.frontIntake.enableBrakeMode(True)
        self..enableBrakeMode(True)
        self.shooterMain.enableBrakeMode(True)
        self.shooterFeed.enableBrakeMode(True)
        '''
        self.climberMotor.enableBrakeMode(True)
        '''
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
    def rampShooter(self):#this method is supposed to ramp the motor speed based on our distance away from the target. Ideally we can use this to shoot on the move
        return shooterSpeed = (1 - 0.716)/(126 - 77)*(self.cam.distance - 126) + 1      #Converted for us, see camera.py

        #the theoretical proportion between motor
        #input and distance from goal. When implementing be sure to account for a
        #fall off point at which point the motor doesnt move fast enough to get a ball
        #to the goal. Our current range is .6 to 1, and 60" to 102" but that requires
        #more testing

    def getShooter(self):
        return self.shooterToggle

    def toggleIntake(self, aButton):#the wait is because under normal circumstances the code will cycle twice, so when you press the button it turns the intake off and on before you can release the button
        if(self.wait>0):
            self.wait-=1
        elif(self.wait<=0):
            if(aButton and self.intakeToggle == False):
                self.intakeToggle = True
                self.wait = 35
            elif(aButton and self.intakeToggle == True):
                self.intakeToggle = False
                self.wait = 35
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
                self.flash1.set(Relay.Value.kForward)#using spike H-bridge relays, need tp use forward instead of on because of the way the modes function
                #self.flash2.set(True)
                self.wait2 = 50
                print ('Lights_On')
                self.lights = True
            elif(yButton and self.lights == True):
                #self.flash1.set(Relay.Value.Off)
                self.flash1.set(Relay.Value.kOff)
                #self.flash2.set(False)
                self.wait2 = 50
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
    def toggleShooter(self, xButton, speed=None):#switches the front motors on or off
        if(speed==None):
            speed = self.shooterSpeed
        if(self.wait>0):
            self.wait-=1
        elif(self.wait<=0):
            if(xButton and self.shooterToggle == False):
                self.shooterToggle = True
                self.wait = 35
            elif(xButton and self.shooterToggle == True):
                self.shooterToggle = False
                self.wait = 35
            else:
                pass
            if(self.shooterToggle == True):
                self.shooterMain.set(speed)

            elif(self.shooterToggle == False):
                self.shooterMain.set(0)

    def fire(self, speedValue):#accepts input from 0 to 1,
            self.shooterFeed.set(int(speedValue))#usually passing it controller #'s
            self.shooterSpeed = self.rampShooter()

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
        #print(self.lights)
        self.toggleIntake(aButton)
        self.toggleLights(yButton)
        #self.reverseIntake(bButton)
        self.toggleShooter(xButton)
        self.fire(rightTrigger)
        self.climb(climberStick)
