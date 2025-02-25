import wpilib as wpi

class LimitSwitch(wpi.DigitalInput):
    def __init__(self, id: int):
        super().__init__(id)
        self.__isTriggered__ = False

    def getPressed(self) -> bool:
        print('Pressed: ', self.get())
        if (self.get() == True and not(self.__isTriggered__)):
            self.__isTriggered__ = True
            return True
        else:
            return False
        
    def getReleased(self) -> bool:
        print('Released: ', self.get())
        if (self.get() == False and self.__isTriggered__):
            self.__isTriggered__ = False
            return True
        else:
            return False
    
    
        