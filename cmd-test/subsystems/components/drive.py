from wpilib import MotorControllerGroup
from wpilib.drive import DifferentialDrive
import subsystems.components.motors as m


class Drive(DifferentialDrive):
    ''' 
    Inherits from Differential Drive. Represents the robot drive train.
    Class parameters to modify:
        MAX_POWER - Adjust maximum robot power (0-1, where 1 is full power)
        INVERT_LEFT - Inverts left drive train (assuming intake region is front)  
        INVERT_RIGHT - Inverts right drive train (assuming intake region is front)

    '''

    # The way the motors are inverted may affect robot direction.
    # By default, the left train is inverted. At least ONE drive train must be inverted.
    MAX_POWER = 0.6
    INVERT_LEFT = True  
    INVERT_RIGHT = not(INVERT_LEFT)

    def __init__(self):
        # Motors are created like this: Left[0, 1] Right[2,3] 
        # Use Phoenix Tuner to change CAN IDs if needed.
        front_left = m.createTalonSRX(0, neutral_mode=m.NeutralMode.Coast)
        back_left = m.createVictorSPX(1, neutral_mode=m.NeutralMode.Coast)
        front_right = m.createVictorSPX(2, neutral_mode=m.NeutralMode.Coast)
        back_right = m.createVictorSPX(3, neutral_mode=m.NeutralMode.Coast)

        # wpilib.MotorControllerGroup is deprecated as of 2024 and will be removed the following season.
        # See if you could use the follow command to replace MotorControllerGroup?

        left_train = MotorControllerGroup(
            front_left, back_left)
        left_train.setInverted(Drive.INVERT_LEFT)

        right_train = MotorControllerGroup(
            front_right, back_right)
        right_train.setInverted(Drive.INVERT_RIGHT)

    
        # Since this class inherits DifferentialDrive, we all super().__init__ to
        # initialize parent class and create a reference for the robot.
        super().__init__(leftMotor=left_train, rightMotor=right_train)

        self.setMaxOutput(maxOutput=Drive.MAX_POWER)
