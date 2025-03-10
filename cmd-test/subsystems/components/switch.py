from wpilib import DigitalInput

class LimitSwitch(DigitalInput):
    '''
    Class to read a limit switch. 
    This class will read digital inputs from the limit switch.
    This class can return the current value of the switch or return a value when the switch is pressed/released.

    This clsas is meant to be used with switches. For all other DIO components, use the DigitalInput class.
    '''
    def __init__(self, id: int):
        '''
        id: the DIO channel that the switch is connected to on the roboRIO.

        Construct an instance of a limit switch given a channel.
        The ID is labeled directly on the roboRIO. 
        '''
        super().__init__(id)
        self.__triggered_lastCheck__ = False


    def getPressed(self) -> bool:
        '''
        Get whether this limit switch was pressed in the last check.
        Recommended for events that should execute once.

        Returns: boolean
        '''

        # Get current value of limit switch. Check if the switch was not triggered in the last check.
        if (self.get() == True and not(self.__triggered_lastCheck__)):
            self.__triggered_lastCheck__ = True     # Set this variable true for next check.
            return True                             # This should return true ONLY ONCE when the switch is pressed.
        
        else:
            return False                            # This should return FALSE if the switch remains pressed or is released.
        
        
    def getReleased(self) -> bool:
        '''
        Get whether this limit switch was released in the last check.
        Recommended for events that should execute once.

        Returns: boolean
        '''
        # Get current value of limit switch. Check if the switch is triggered in the last check.
        if (self.get() == False and self.__triggered_lastCheck__):
            self.__triggered_lastCheck__ = False     # Set this variable true for next check.
            return True                             # This should return true ONLY ONCE when the switch is released.
        
        else:
            return False                            # This should return FALSE if the switch remains released or is pressed.
