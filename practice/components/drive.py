from wpilib import MotorControllerGroup
from wpilib.drive import DifferentialDrive

import components.motors as m

class Drive(DifferentialDrive):
    def __init__(self):
        # Adjust maximum robot power (0-1, where 1 is full power)
        maxPower = 0.25

        # True: Left Side inverted; False: Right side inverted
        # The way the motors are inverted may affect robot direction
        INVERT_LEFT = True


        drive_train_motors = []

        for id in range(4):
            drive_train_motors.append(m.createTalonSRX(id, m.NeutralMode.Coast))
        

        left_train = MotorControllerGroup(drive_train_motors[0], drive_train_motors[1])
        left_train.setInverted(INVERT_LEFT)

        right_train = MotorControllerGroup(drive_train_motors[2], drive_train_motors[3])
        left_train.setInverted(not(INVERT_LEFT))
        
        # Since this class inherits DifferentialDrive, we all super().__init__ to 
        # initialize parent class and create a reference for the robot.
        super().__init__(leftMotor=left_train, rightMotor=right_train)

        self.setMaxOutput(maxOutput=maxPower)



    