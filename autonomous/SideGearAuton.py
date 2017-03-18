"""
File Author: Will Hescott
File Creation Date: 2/4/2016
File Purpose: Score a gear into the 'Main' (Frontmost) gear scoring station on the red side
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
#from components.drive import driveTrain
from wpilib import SendableChooser
#from components.armControl import arm


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
        return 89

    def getSpeed(self):
        return 0.5

    @timed_state(first=True, duration=0.5, next_state='drive_forward')
    def drive_stop(self) :
        self.drive.reset()
        self.opControl.toggleLights(True)
        self.drive.autonTankDrive(0, 0)

    @state()
    def drive_forward(self) :
        print (self.drive.getDistance())
        if self.drive.getDistance() < self.getTargetDistance():
            self.drive.autonTankDrive(self.getSpeed(), self.getSpeed())
        else :
            #self.drive.autonTankDrive(0, 0)
            self.drive.reset()
            self.next_state('turn')

    @state()
    def turn(self):
        if(self.drive.turnAngle(self.getTurnAngle())):
            self.next_state('strafe')

    @timed_state(first=False, duration=3.7, next_state='done')
    def strafe(self):
        self.drive.autonStrafe(0.5)

    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)

    @timed_state(first=False, duration=2.0, next_state='strafe')
    def lineUp(self):
        if self.cam.centerSide(False):
            self.next_state('strafe')
