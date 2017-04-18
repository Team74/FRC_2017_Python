"""
File Author: Sam VanderArk
File Creation Date: 4/7/2016
File Purpose: Score a gear into the side station, back up, then shoot
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
#from components.drive import driveTrain
from wpilib import SendableChooser, Relay
import camera


class shootAndGear_Right(StatefulAutonomous):

    MODE_NAME = 'shootAndGear_Right'
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
        return -45

    def getStrafe(self):
        return -0.8

    def getTargetDistance(self):
        return 78/2.25

    def getSpeed(self):
        return 0.5

    def getOffset(self):
        return -0.47


    @timed_state(first=True, duration=0.5, next_state='drive_forward')
    def drive_stop(self) :
        self.drive.reset()
        self.opControl.flash1.set(Relay.Value.kForward)
        self.opControl.flash2.set(Relay.Value.kForward)
        self.drive.autonTankDrive(0, 0)

    @state()
    def drive_forward(self) :
        if self.drive.getDistance() < self.getTargetDistance():
            self.drive.autonTankDrive(self.getSpeed(), self.getSpeed())
        else :
            self.drive.reset()
            self.next_state('turn')

    @state()
    def turn(self):
        if(self.drive.turnAngle(self.getTurnAngle(), .25)):
            self.next_state('drive_forward_2')

    @timed_state(first=False, duration=2.0, next_state='done')
    def drive_forward_2(self):
        self.drive.autonTankDrive(-0.4, -0.4)

    @timed_state(first=False, duration=3.0, next_state='reverse')
    def pause(self):
        pass

    @timed_state(first=False, duration=1.5, next_state='done')
    def reverse(self):
        self.drive.autonTankDrive(0.4, 0.4)

    @state()
    def spin_around(self):
        if(self.drive.turnAngle(180+self.getTurnAngle(), .25)):
            self.next_state('moveBack')

    @timed_state(first=False, duration=1.0, next_state='lineUp')
    def moveBack(self): #forward
        self.drive.autonTankDrive(-0.25,-0.25)

    @timed_state(first=False, duration=3.0, next_state='shoot')
    def lineUp(self):
        camera.TARGET = camera.SHOOTER_TARGET #0.2
        self.drive.centerSide(True)
        camera.TARGET = 0

    @state()
    def startShoot(self):
        self.opControl.toggleShooter(True)
        self.opControl.toggleIntake(True)
        self.next_state = 'shoot'

    @timed_state(first=False, duration=4.0, next_state='done')
    def shoot(self):    #might go over time
        pass

    @state()
    def done(self) :
        self.opControl.toggleIntake(False)
        self.opControl.toggleShooter(False)
        self.drive.autonTankDrive(0, 0)
