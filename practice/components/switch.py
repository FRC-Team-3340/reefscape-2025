import wpilib as wpi

class LimitSwitch(wpi.DigitalInput):
    def __init__(self, id: int):
        super().__init__(id)
        self.__isTriggered = False

    def getPressed(self) -> bool:
        if (self.get() == True and not(self.__isTriggered)):
            self.__isTriggered = True
            return True
        else:
            return False
        
    def getReleased(self) -> bool:
        if (self.get() == False and self.__isTriggered):
            self.__isTriggered = False
            return True
        else:
            return False
        
    
        