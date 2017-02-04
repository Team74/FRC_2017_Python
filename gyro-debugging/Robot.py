#!/usr/bin/env python3

import wpilib

class MyRobot(wpilib.SampleRobot):    
    def robotInit(self):
        self.gyro = wpilib.ADXRS450_Gyro(wpilib.SPI.Port.kOnboardCS0)
        self.countTest = 0
        
    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def autonomous(self):
        while self.isAutonomous() and self.isEnabled():
            wpilib.Timer.delay(0.01)

    def operatorControl(self):
        timer = wpilib.Timer()
        timer.start()

        while self.isOperatorControl() and self.isEnabled():
            angle = self.gyro.getAngle()
            self.countTest += 1
            wpilib.SmartDashboard.putNumber("GyroAngleTest", angle)
            wpilib.SmartDashboard.putNumber("CountTest", self.countTest)
            wpilib.Timer.delay(0.02)

if __name__ == '__main__':
    wpilib.run(MyRobot)
