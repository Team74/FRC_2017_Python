"""
File Author: Will Hescott
File Creation Date: 2/4/2016
File Purpose: Score a gear into the 'Main' (Frontmost) gear scoring station on the red side
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
#from components.drive import driveTrain
from wpilib import SendableChooser, Relay
#from components.armControl import arm
import camera


class BaseSideGearAuton(StatefulAutonomous):

    #MODE_NAME = 'SideGearAuton'
    DEFAULT = False
    DRIVE_DISTANCE = 60
    #drive = driveTrain
    chooser = SendableChooser()
    default_modes = []
    iCount = 0
    #dt = driveTrain()

    def Initialize(self):
        pass

    def getTurnAngle(self):
        return 90

    def getStrafe(self):
        return 1

    def getTargetDistance(self):
        return 89/2.25

    def getSpeed(self):
        return 0.5

    def getOffset(self):
        return -0.47

    def getCounterforce(self):
        return -0.1

    def getCenter(self):
        return True

    @timed_state(first=True, duration=0.5, next_state='drive_forward')
    def drive_stop(self) :
        self.drive.reset()
        #self.opControl.flash1.set(Relay.Value.kForward)
        #self.opControl.flash2.set(Relay.Value.kForward)
        self.drive.autonTankDrive(0, 0)

    @state()
    def drive_forward(self) :
        print (self.drive.getDistance())
        if self.drive.getDistance() < self.getTargetDistance():
            self.drive.autonTankDrive(self.getSpeed(), self.getSpeed())
        else :
            #self.drive.autonTankDrive(0, 0)
            self.drive.reset()
            if self.getCenter():
                self.next_state('done')
            else:
                self.next_state('turn')


    @timed_state(first=False, duration=5, next_state='done')
    def drive_forward_2(self):
        self.drive.autonTankDrive(-0.2, -0.2)

    @state()
    def turn(self):
        if(self.drive.turnAngle(self.getTurnAngle(), .25)):
            self.next_state('drive_forward_2')
            #self.drive.zeroGyro()
               #lineUp

    @timed_state(first=False, duration=15, next_state='done')
    def strafe(self):
        self.drive.strafe2(1, 0) # if'st'nt'd'll

    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)

    @timed_state(first=False, duration=4.0, next_state='strafe')
    def lineUp(self):
        camera.TARGET = self.getOffset()
        self.drive.centerSide(False)
        camera.TARGET = 0
