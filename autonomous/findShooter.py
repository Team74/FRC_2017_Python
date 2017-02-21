"""
File Author: Will Hescott
File Creation Date: 2/03/2017
File Purpose:Creating a proof of concept autonomous program that uses
multiple features available to practice implementation and work our kinks.
This auton begins in front of the gear loading statsion, drives forwards,
turns 90 degrees to the left, then proceeds forward before turning again and
driving up to the 'key' line.
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
#from components.drive import driveTrain
from wpilib import SendableChooser
#from components.armControl import arm


class autonomousModeTestingLowBar(StatefulAutonomous):

    MODE_NAME = 'findGoal'
    DEFAULT = False
    DRIVE_DISTANCE = 60
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
    @timed_state(first=True, duration=0.5, next_state='findGoal')
    def drive_stop(self) :
        self.drive.reset()
        self.drive.autonTankDrive(0, 0)

    #@timed_state(first=False, duration = 7, next_state ='done')
    @state
    def findGoal(self):
        if(self.drive.findGoal()):
            #self.next_state('done')
            pass    


    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)
        self.opControl.fire(True)
