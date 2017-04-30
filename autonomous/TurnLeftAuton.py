from autonomous.SideGearAuton import BaseSideGearAuton

class leftSideAuton(BaseSideGearAuton):

    MODE_NAME = 'LeftSideAuton'

    def getTurnAngle(self):
        return 48

    def getStrafe(self):
        return -0.8

    def getTargetDistance(self):
        return 101/2.25

    def getSpeed(self):
        return  -0.35

    def getOffset(self):
        return -0.47

    def getCounterforce(self):
            return -0.1

    def getCenter(self):
        return False
