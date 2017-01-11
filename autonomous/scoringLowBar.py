"""
File Author: Will Lowry
File Creation Date: 2/23/2016
File Purpose: To create a skeleton autonomous mode testing the low bar
"""

import wpilib
from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import SendableChooser, Timer
#from components.armControl import arm


class autonomousModeScoringLowBar(StatefulAutonomous):

    MODE_NAME = 'Low Bar Scoring'
    DEFAULT = False
    DRIVE_DISTANCE = 200
    GOAL_TURN_ANGLE = 60
    DRIVE_DISTANCE_2 = 40
    ArmDown = False
    UnderLowBar = False
    Turned = False
    DriveToGoal = False
    SpitOutBall = False
    wpilib.SmartDashboard.putBoolean('ArmDown', ArmDown)
    wpilib.SmartDashboard.putBoolean('UnderLowBar', UnderLowBar)
    wpilib.SmartDashboard.putBoolean('Turned', Turned)
    wpilib.SmartDashboard.putBoolean('DriveToGoal', DriveToGoal)
    wpilib.SmartDashboard.putBoolean('SpitOutBall', SpitOutBall)


    chooser = SendableChooser()
    default_modes = []
    iCount = 0
    #dt = driveTrain()

    def Initialize(self):
        pass

# A positive motor value for the ARM makes it go down
# A positive motor value for the WHEEL makes them take in the ball

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='move_arm')
    def drive_stop(self) :
        self.drive.reset()
        self.drive.autonTankDrive(0, 0)

    @state()
    def move_arm(self):
        if(self.arm.getPOT() >= 1):
            self.arm.armAuto(0,1,1,rate=0.6)
        else:
            self.arm.armAuto(0,0,1)
            ArmDown = True
            self.next_state('drive_forward_under_lowbar')

    @state()
    def drive_forward_under_lowbar(self):
        if self.drive.getAutonDistance() <= self.DRIVE_DISTANCE :
            self.drive.autonTankDrive(0.5, 0.5)
        else :
            self.drive.autonTankDrive(0, 0)
            self.drive.reset()
            Timer.delay(0.5)
            UnderLowBar = True
            self.next_state('turn_toward_goal')

    @state()
    def turn_toward_goal(self):
        if(self.drive.turn_angle(self.GOAL_TURN_ANGLE)):
            Timer.delay(0.1)
        else:
            self.drive.reset()
            Turned = True
            self.next_state('drive_toward_goal')

    @state()
    def drive_toward_goal(self):
        if self.drive.getAutonDistance() <= self.DRIVE_DISTANCE_2 :
            self.drive.autonTankDrive(0.25, 0.25)
        else :
            self.drive.autonTankDrive(0, 0)
            DriveToGoal = True
            self.next_state('drop_ball')

    @state()
    def drop_ball(self):
        self.arm.wheelSpin(1)
        SpitOutBall = True
        self.next_state('done')

    @state()
    def done(self) :
        pass
