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

    MODE_NAME = 'LeftTurn'
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
    @timed_state(first=True, duration=0.5, next_state='drive_forward')
    def drive_stop(self) :
        self.drive.reset()
        self.drive.autonTankDrive(0, 0)

    @state()
    def turnLeft(self):
        if(self.drive.turnAngle(-90)):
            self.next_state('drive_forward2')

    @state()
    def turnLeft2(self):
        if(self.drive.turnAngle(-40)):
            self.next_state('drive_forward3')

    @state()
    def drive_forward(self) :
        print ('driveForeward1')
        if self.drive.getDistance() < 61 :
            self.drive.autonTankDrive(0.5, 0.5)
        else :
            print ('driveForewardPassed')
            self.drive.reset()
            self.next_state('turnLeft')

    @state()
    def drive_forward2(self) :
        if self.drive.getDistance() < 92 :
            self.drive.autonTankDrive(0.5, 0.5)
        else :
            self.drive.reset()
            self.next_state('turnLeft2')

    @state()
    def drive_forward3(self) :
        if self.drive.getDistance() < 20:
            self.drive.autonTankDrive(0.5, 0.5)
        else :
            self.drive.reset()
            self.next_state('done')
    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)
