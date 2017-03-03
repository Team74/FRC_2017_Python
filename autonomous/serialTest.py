"""
File Author: Will Hescott
File Creation Date: 2/09/2017
File Purpose: cross auton line and fire balls into the high goal
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
#from components.drive import driveTrain
from wpilib import SendableChooser
#from components.armControl import arm

from camera import Camera


class autonomousModeSerialTest(StatefulAutonomous):

    MODE_NAME = 'SerialTest'
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

    @state(first=True)
    def test_start(self) :
        self.drive.reset()
        self.drive.autonTankDrive(0, 0)
        self.thng = Tthhinnggyy()
        self.next_state('test_serial')

    @state()
    def test_serial(self):
        self.thng.receive()
        if thng.centerSide() and thng.centerLine() :	#this works because of short-circuiting
            print("hooboyshoot")
            self.next_state('test_end')

    @state()
    def test_end(self):
        pass
