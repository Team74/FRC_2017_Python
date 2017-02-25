"""
File Author: Will Hescott
File Creation Date: 1/8/2017
File Purpose: To create our drive functions


"""
import math
import wpilib
from wpilib import RobotDrive
from xbox import XboxController
from wpilib.smartdashboard import SmartDashboard
from components.operatorControl import opControl
from components.drive import driveTrain
from ctre.cantalon import CANTalon
from robotpy_ext.autonomous.selector import AutonomousModeSelector

## from wpilib import USBCamera, CameraServer



class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        self.controller = XboxController(0)#logitech controllers
        self.controller2 = XboxController(1)
        self.drive = driveTrain(self)#initialising a drivetrain objet
        self.drive.reset()
        self.opControl = opControl(self)#initialising a operator control object
        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()


        # Initialize Components functions
        # components are referenced from auton to avoid the trouble of running multiple inits of the same objects
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
        while self.isAutonomous() and self.isEnabled():
            self.autonomous_modes.run()


    def operatorControl(self):
        #self.opControl.setSpeed() #used for manually setting motor speeds for testing, disable for teleop
        while self.isOperatorControl() and self.isEnabled():
            wpilib.SmartDashboard.putNumber("GyroAngle",self.drive.getGyroAngle())#Putting important information onto the dashboard for reference in teleop


            '''if self.controller.getButtonB():
                self.drive.findGoal()
            else:'''
            if(self.controller.getButtonA() and self.drive.getSensor()==False):
                self.drive.drive(0,0,0)
            else:
                if(self.controller.getRightTrigger()==True):#This statement tells the drivetrain exclusively track the target and ignore other movement commands. It is faster than the moving and shooting system and more accurate. we
                    self.drive.findGoal()                  #do trade off mobility for it however, so it is important to have both
                elif self.controller.getButtonY():
                    self.drive.findGoal(False)	#uses the other type
                else:
                    if(self.controller.getButtonB()):
                        self.drive.findGoal()
                    self.drive.drive(self.scaleInput(self.controller.getLeftX()), self.scaleInput(self.controller.getLeftY()),self.scaleInput(self.controller.getRightX()))#Passing variables from the drivers controller to
                    #[cont.] the drive functions file. It also wraps the values with the scaleInput method which puts the input on an exponential curve, which gives the driver both fine-tuned control and power if you need it
            if(self.controller.getButtonX() == True):#This just allows the driver to zero the gyro out. It drifts between 30 and 60 degrees on every 360 degree rotation. It's  a hardare problem so this is the best we can  do
                self.drive.zeroGyro()

            self.opControl.operatorFunctions(self.controller2.getButtonA(), self.controller2.getButtonB(), self.controller2.getButtonX(), self.controller2.getButtonY(), self.controller2.getLeftY(), self.controller2.getRightTrigger(), self.controller2.getLeftTrigger())
            #passes controller2 values to the operatorControl file

    def scaleInput(self, x):#Wrapper method that puts all 0-1 input on an exponential curve, meaning that low values are exponentially low and high values scale up quickly. This allows for both fine motor control and
    #[cont.] power without the need to press a button or aply a new setting
        negativeOutput = False
        if(x<0):#checks for negative value. The equation can only scale positive numbers exponentially, so we pass a positive value regardless and then switch it back to negative after the calculations are done
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
