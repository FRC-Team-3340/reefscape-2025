import wpilib as wpi

class MyRobot(wpi.TimedRobot):
    def __init__(self):
        self.mySwitch = wpi.DigitalInput(0)

    def robotPeriodic(self):
        if self.mySwitch.get() == True:
            print("hi :D")
        
        