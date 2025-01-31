import wpilib as wpi
import wpilib.drive as drive

import motors as m

class Drive(drive.DifferentialDrive):
    def __init__(self):
        drive_train_motors = []

        for id in range(4):
            drive_train_motors.append(m.createTalonSRX(id, m.p5.NeutralMode.Coast))
        
        # True: Left Side inverted; False: Right side inverted
        # The way the motors are inverted may affect robot direction
        invert_left = True

        left_train = wpi.MotorControllerGroup(drive_train_motors[0], drive_train_motors[1])
        left_train.setInverted(invert_left)

        right_train = wpi.MotorControllerGroup(drive_train_motors[2], drive_train_motors[3])
        left_train.setInverted(not(invert_left))
        
        # Since this class inherits DifferentialDrive, we all super().__init__ to 
        # initialize parent class and create a reference for the robot.
        super().__init__(leftMotor=left_train, rightMotor=right_train)

        # Adjust maximum robot power (0-1, where 1 is full power)
        self.setMaxOutput(maxOutput=0.5)



    