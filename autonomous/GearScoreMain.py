from autonomous.SideGearAuton import BaseSideGearAuton

class gearScoreCenter(BaseSideGearAuton):

    MODE_NAME = 'MiddleGearScore'

    def getTurnAngle(self):
        return 0

    def getStrafe(self): #rotational speed needs to be .25, all other autons need to be .2
        return -0.8

    def getTargetDistance(self):
        return 120

    def getSpeed(self):
        return -0.25

    def getOffset(self):
        return -0.47

    def getCounterforce(self):
        return 0.0

    def getCenter(self):
        return True
# ex die
