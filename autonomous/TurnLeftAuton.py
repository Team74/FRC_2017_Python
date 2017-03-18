from autonomous.SideGearAuton import BaseSideGearAuton

class leftSideAuton(BaseSideGearAuton):

    MODE_NAME = 'LeftSideAuton'

    def getTurnAngle(self):
        return -30

    def getStrafe(self):
        return -0.725

    def getTargetDistance(self):
        return 110

    def getSpeed(self):
        return 0.5
