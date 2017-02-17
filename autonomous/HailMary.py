"""
File Author: Will Hescott
File Creation Date: 2/11/2017
File Purpose: cross auton line, load balls from the hopper, and fire balls into the high goal
"""
'''
from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
#from components.drive import driveTrain
from wpilib import SendableChooser
#from components.armControl import arm


class autonomousModeTestingLowBar(StatefulAutonomous):

    MODE_NAME = 'HailMary'
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
        if self.drive.getDistance() > -200:
            self.drive.autonTankDrive(-0.5, -0.5)
        else :
            #self.drive.autonTankDrive(0, 0)
            self.drive.reset()
            self.next_state('strafeRight')

    @timed_state(first=False, duration=1, next_state='strafeLeft')
    def strafeRight(self):
        self.drive.drive(0, 1, 0)

    @timed_state(first=False, duration=1, next_state='prepTurn')
    def strafeLeft(self):
        self.drive.drive(0, -1, 0)

    @state()
    def prepTurn(self):
        if self.drive.getDistance < 70:
            self.drive.autonTankDrive(.5, .5)
        else:
            self.drive.reset()
            self.next_state('turnLeft')

    @state()
    def turnLeft(self):
        if self.drive.turnAngle(-90)
            self.drive.reset()
            self.next_state('driveToShip')

    @state()
    def driveToShip(self):
        if self.drive.getDistance < 80:
            self.drive.autonTankDrive(.5, .5)
        else:
            self.drive.reset()
            self.next_state('lookForStation')

    @state()
    def lookForStation(self):
        if (self.cam.getLocation != self.coordinates):
            self.drive.strafe(direction)
        else:
            self.drive.reset()
            self.next_state('scoreGear')

    @timed_state(first=False, duration=3, next_state='backOff')
    def scoreGear(self):
            self.drive.autonTankDrive(0.5, 0.5)

    @timed_state(first=False, duration=1.5, next_state='findGoal')
    def scoreGear(self):
            self.drive.autonTankDrive(-0.35, -0.75)

    @state()
    def findGoal(self):
        if (self.shooterCam.getLocation() != self.coordinates):
            self.drive.strafe(direction)
        elif(self.shooterCam.getDistance() >= self.targetDistance):
            self.drive.autonTankDrive(0.3, 0.3)
        elif(self.shooterCam.getDistance() <= self.targetDistance):
            self.drive.autonTankDrive(-0.3, -0.3)
        else
            self.drive.reset()
            self.nextState('fire')

    @timed_state(first=False, duration=7.5, next_state='done')
    def fire(self) :
        self.drive.reset()
        if(self.opControl.getShooter()):
            self.fire = True
            while(fire):
                self.opControl.fire(True)
        else:
            self.opControl.toggleShooter()
            self.fire = True
            while(fire):
                self.opControl.fire(True)


    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)
        '''
