from wpilib import MotorControllerGroup
from wpilib.drive import DifferentialDrive
from typing import List

import components.motors as m


class Drive(DifferentialDrive):
    MAX_POWER = 0.25           # Adjust maximum robot power (0-1, where 1 is full power)

    # The way the motors are inverted may affect robot direction.
    # By default, the left train is inverted. At least ONE drive train must be inverted.
    INVERT_LEFT = True
    INVERT_RIGHT = False

    def __init__(self):
        drive_train_motors: List[m.WPI_TalonSRX] = []

        # Motors are created like this: Left[0, 1] Right[2,3]
        # Use Phoenix Tuner to change CAN IDs if needed.
        for id in range(4):
            drive_train_motors.append(
                m.createTalonSRX(id, m.NeutralMode.Coast))

        # wpilib.MotorControllerGroup is deprecated as of 2024.
        # See if you could use the follow command to replace MotorControllerGroup?
        # drive_train_motors[0].follow(drive_train_motors[1])

        left_train = MotorControllerGroup(
            drive_train_motors[0], drive_train_motors[1])
        left_train.setInverted(Drive.INVERT_LEFT)

        right_train = MotorControllerGroup(
            drive_train_motors[2], drive_train_motors[3])
        right_train.setInverted(Drive.INVERT_RIGHT)

        # Since this class inherits DifferentialDrive, we all super().__init__ to
        # initialize parent class and create a reference for the robot.
        super().__init__(leftMotor=left_train, rightMotor=right_train)


        self.setMaxOutput(maxOutput=Drive.MAX_POWER)
