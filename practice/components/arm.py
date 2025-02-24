import components.motors as m
from components.switch import LimitSwitch as ls

# Arm does not inherit from another class unlike switch or drive.
# Arm consists of more than just one motor.


class Arm:
    GEAR_BOX_RATIO_ARM = 64
    ARM_MOTOR_POWER = .1

    def __init__(self):
        # create motor for the intake and "arm" mechanism
        self.roller_motor = m.createTalonSRX(
            5, neutral_mode=m.NeutralMode.Coast)
    
        self.arm_motor = m.createSparkMax(
            can_id= 5,
            neutral_mode=m.SparkMax.IdleMode.kBrake,
            motor_type= m.SparkLowLevel.MotorType.kBrushless
        )
        # remember that encoder tracks rotations. gear box ratio is 64:1.
        # meaning: it takes 64 rotations of the motor for the gears to complete one rotation
        # 0.125 or 1/8th gear box rotation = 45 degrees (theoretically)

        self.arm_encoder = m.createSparkMaxEncoder(self.arm_motor)

        self.arm_limit = ls(0)

        self.__hit_lower_limit__ = False
        self.__hit_upper_limit__ = False
        self.__calibrated__ = True
        self.__isExtended__ = False
        self.__isRetracted__ = False

        self.arm_encoder.setPosition(0)

    # def rotate_arm_45_degrees(self):
        # Assuming encoder counts per full revolution is 2048
        # To rotate 45 degrees (1/8th), we need to move 256 encoder counts
        # target_position = self.arm_encoder.getPosition() + 256

        # Set the target position for the arm motor to rotate 45 degrees
        # self.arm_motor.getPIDController().setReference(target_position, m.SparkMax.ControlType.kPosition)


    def retractArm(self):
        pass

    def extendArm(self):
        pass

    def manualArmControl(self, direction: float):
        self.checkArmPosition()

        if (not(self.__isExtended__) and direction > 0):
            self.arm_motor.set(direction * Arm.ARM_MOTOR_POWER)
        elif(not(self.__isRetracted__) and direction < 0):
            self.arm_motor.set(direction * Arm.ARM_MOTOR_POWER)
        else:
            self.arm_motor.set(0)


    def checkArmPosition(self):
        '''Checks position of arm. Basically a software limit check.'''

        # Calculate encoder counts relative to arm, and convert to degrees
        armAngle = (self.arm_encoder.getPosition() / Arm.GEAR_BOX_RATIO_ARM) * 360

        # Check if arm is extended (set to pick up algae)
        if armAngle >= 45:
            self.__isExtended__ = True
        else:
            self.__isExtended__ = False

        # Check if arm is retracted (set to dispense coral or algae)
        if (self.arm_limit.getPressed() and not(self.__calibrated__)):
            self.arm_encoder.setPosition(0)        


        if armAngle <= 0:
            self.__isRetracted__ = True

            # Motor will recalibrate itself automatically once it is back on neutral position
            if not(self.__calibrated__):
                self.arm_encoder.setPosition(0)
                self.__calibrated__ = True

        else:
            # The motor is not considered calibrated once away from neutral retracted position
            self.__isRetracted__ = False
            self.__calibrated__ = False
