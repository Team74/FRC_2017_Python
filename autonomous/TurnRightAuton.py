from autonomous.SideGearAuton import BaseSideGearAuton

class rightSideAuton(BaseSideGearAuton):

    MODE_NAME = 'RightSideAuton'

    def getTurnAngle(self):
        return -51

    def getStrafe(self):
        return -0.8

    def getTargetDistance(self):
        return 107/2.25

    def getSpeed(self):
        return -0.35

    def getOffset(self):
        return -0.47

    def getCounterforce(self):
            return 0.1

    def getCenter(self):
        return False
