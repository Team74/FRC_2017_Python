from autonomous.SideGearAuton import BaseSideGearAuton

class rightSideAuton(BaseSideGearAuton):

    MODE_NAME = 'RightSideAuton'

    def getTurnAngle(self):
        return 26.5

    def getStrafe(self):
        return 0.46

    def getTargetDistance(self):
        return 110

    def getSpeed(self):
        return -0.5
