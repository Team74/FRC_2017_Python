"""
File Author: Will Hescott
File Creation Date: 2/09/2017
File Purpose: cross auton line and fire balls into the high goal
Start with shooter facing driver station, ndxt to the boiler
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
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

    @state()
    def drive_backward(self) :
        if self.drive.getDistance() < 50:
            self.drive.autonTankDrive(0.5, 0.4)
        else :
            self.drive.reset()
            self.next_state('findGoal')

    @state()
    def findGoal(self):
        if(self.drive.findGoal()):
            self.drive.autonTankDrive(0, 0)
            self.next_state('sim_Fire')

    @timed_state(first=False, duration=7.5, next_state='done')
    def sim_Fire(self) :
        self.drive.reset()
        self.drive.fire(True)
        #else:
        #    self.opControl.toggleShooter(True)


    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)
