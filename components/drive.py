'''"""
File Author: Will Hescott
File Creation Date: 1/25/2017
File Purpose: To create and run our operator functions
"""

import wpilib
from robot import MyRobot
from wpilib import Encoder, Timer, RobotDrive, Spark
from ctre.cantalon import CANTalon
from wpilib.interfaces import Gyro
from . import Component


class auton(Component) :



    def __init__(self, robot):
        super().__init__()

    def turnAngle(self, angle):
        if(robot.gyro.getAngle() > 0)
