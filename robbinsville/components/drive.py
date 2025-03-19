from wpilib import MotorControllerGroup, SmartDashboard

from wpilib.drive import DifferentialDrive
from typing import Literal
import components.motors as m

'''
WHAT TO DO FOR NEXT YEAR:
-   wpilib.MotorControllerGroup is deprecated as of 2024 and will be removed next season (2026). 
    -   Find a replacement method for MotorControllerGroup?

-   Document next year's code :D
'''

# ----CONSTANTS---- #
MAX_POWER = 0.6                     # Maximum speed of drive train [0 - 1]
INVERT_LEFT = True                  # Inverts left side of drive train. NOTE: one train must ALWAYS be inverted
INVERT_RIGHT = not(INVERT_LEFT)     
NEUTRAL_MODE = m.NeutralMode.Brake  # Idle mode for drive train (what the train does once you set it to neutral state (0)

SmartDashboard.putBoolean("Invert", INVERT_LEFT)


# ----DECLARATIONS---- #
# Motors are created like this: Left[0, 1] Right[2,3]
# Use Phoenix Tuner to change CAN IDs if needed.
front_left = m.createTalonSRX(0, neutral_mode=NEUTRAL_MODE)
back_left = m.createVictorSPX(1, neutral_mode=NEUTRAL_MODE)
front_right = m.createVictorSPX(2, neutral_mode=NEUTRAL_MODE)
back_right = m.createTalonSRX(3, neutral_mode=NEUTRAL_MODE)

left_train = MotorControllerGroup(front_left, back_left)
right_train= MotorControllerGroup(front_right, back_right)

class Drive(DifferentialDrive):
    ''' Drive class - inherits from Differential Drive. Represents the robot drive train.
    Class parameters to modify:
        MAX_POWER - Adjust maximum robot power (0-1, where 1 is full power)
        INVERT_LEFT - Inverts left drive train (assuming intake region is front)  
        INVERT_RIGHT - Inverts right drive train (assuming intake region is front)

    # The way the motors are inverted may affect robot direction.
    # By default, the left train is inverted. At least ONE drive train must be inverted.

    '''

    def __init__(self):
        # Since this class inherits DifferentialDrive, we all super().__init__ to
        # initialize parent class and create a reference for the robot.
        super().__init__(leftMotor=left_train, rightMotor=right_train)
        # super().__init__(leftMotor=front_left, rightMotor=front_right)
        self.setMaxOutput(maxOutput=MAX_POWER)

    def configureInvert(self):
        left_train.setInverted(INVERT_LEFT)
        right_train.setInverted(INVERT_RIGHT)


    def getTrainOutput(self, train: Literal['left', 'right']):
        if train == 'left':
            return left_train.get()
        if train == 'right':
            return right_train.get()
        
    def updateDashboard(self):
        global INVERT_LEFT
        SmartDashboard.putNumber("Left Output", self.getTrainOutput(train="left"))
        SmartDashboard.putNumber("Right Output", self.getTrainOutput(train="right"))
        
        invert_setting = SmartDashboard.getBoolean("Invert", True)
        if invert_setting != INVERT_LEFT:
            INVERT_LEFT = invert_setting
            self.configureInvert()

