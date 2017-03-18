from autonomous.SideGearAuton import BaseSideGearAuton

class gearScoreCenter(BaseSideGearAuton):

    MODE_NAME = 'MiddleGearScore'

    def getTurnAngle(self):
        return 90

    def getStrafe(self): #rotational speed needs to be .25, all other autons need to be .2
        return -0.2

    def getTargetDistance(self):
        return 50

    def getSpeed(self):
        return -0.5
