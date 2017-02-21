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


class autonomousModeTestingLowBar(StatefulAutonomous):

    MODE_NAME = 'Blue_GearScoreLeft'
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
    def drive_forward(self) :
        if self.drive.getDistance() < 67:
            self.drive.autonTankDrive(0.5, 0.5)
        else :
            #self.drive.autonTankDrive(0, 0)
            if(self.drive.turnAngle(-90, .3)):
                self.drive.reset()
                self.next_state('strafe_left')

    @state()
    def turnLeft(self):
        if(self.drive.turnAngle(-45))
            self.next_state('drive_forward')

    @state()
    def drive_forward(self):
        if self.drive.getDistance() <30:
            self.drive.autonTankDrive(0.5, 0.5)
        else:
            self.next_state('strafe_right')


    @timed_state(first=False, duration=2, next_state='done')
    def strafe_left(self):
        self.drive.drive(-0.5, 0, -0.5)


    @state()
    def strafe_right(self):
        if not(self.drive.getSensor()==False):
            self.drive.drive(0.5, 0, 0)
        else:
            self.drive.reset()
            x=0
            if(x==100 or x>100):
                self.next_state('strafe_left')
            else:
                x+=1


    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)
