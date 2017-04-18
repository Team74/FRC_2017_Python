"""
File Author: Will Hescott
File Creation Date: 2/09/2017
File Purpose: cross auton line and fire balls into the high goal
Start with shooter facing driver station, ndxt to the boiler
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
import camera
#from components.drive import driveTrain
from wpilib import SendableChooser
#from components.armControl import arm


class autonomousModeTestingLowBar(StatefulAutonomous):

    MODE_NAME = 'SimpleFire'
    DEFAULT = False
    #drive = driveTrain
    chooser = SendableChooser()
    default_modes = []
    iCount = 0
    #dt = driveTrain()

    def Initialize(self):
        pass

# A positive motor value for the ARM makes it go down
# A positive motor value for the WHEEL makes them take in the ball

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='drive_backward')
    def drive_stop(self) :
        self.drive.reset()
        self.drive.autonTankDrive(0, 0)
        self.opControl.toggleLights(True)

    @state()
    def drive_backward(self) :
        if self.drive.getDistance() < 78/2.25:
            self.drive.autonTankDrive(0.5, 0.5)
        else :
            self.drive.reset()
            self.next_state('findGoal')

    @state()
    def findGoal(self):
            camera.TARGET = .4
            if(self.drive.centerSide(True)):
                pass
                camera.TARGET = 0
            else:
                self.drive.reset()
                self.next_state('fire')

    @timed_state(first=False, duration=15, next_state='done')
    def fire(self) :
        self.drive.reset()
        self.opControl.toggleShooter(True)
        self.opControl.toggleIntake(True)
        self.opControl.fire(1)

    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)
