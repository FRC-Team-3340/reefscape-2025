import components.motors as m
from components.switch import LimitSwitch

# Arm does not inherit from another class unlike switch or drive.
# Arm consists of more than just one motor.


class Arm:
    GEAR_BOX_RATIO_ARM = 64
    ARM_MOTOR_POWER = .25
    ROLLER_POWER = 0.25

    def __init__(self):
        # create motor for the intake and "arm" mechanism
        self.roller_motor = m.createTalonSRX(
            7, neutral_mode=m.NeutralMode.Coast)
    
        self.arm_motor = m.createSparkMax(
            can_id= 5,
            motor_type= m.SparkLowLevel.MotorType.kBrushless
        )
        # remember that encoder tracks rotations. gear box ratio is 64:1.
        # meaning: it takes 64 rotations of the motor for the gears to complete one rotation
        # 0.125 or 1/8th gear box rotation = 45 degrees (theoretically)

        self.arm_encoder = m.createSparkMaxEncoder(self.arm_motor)

        self.arm_limit = LimitSwitch(0)

        self.__hit_lower_limit__ = False
        self.__hit_upper_limit__ = False
        self.__calibrated__ = False
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

    def manualArmControl(self, dpad: float):
        self.checkArmPosition()

        if (dpad == 90):
            direction = -1
        elif (dpad == 270):
            direction = 1
        else:
            direction = 0

        if (not(self.__isExtended__) and direction > 0):
            self.arm_motor.set(direction * Arm.ARM_MOTOR_POWER)
        elif(not(self.__isRetracted__) and direction < 0):
            self.arm_motor.set(direction * Arm.ARM_MOTOR_POWER)
        else:
            self.arm_motor.set(0)

    def checkArmPosition(self):
        '''Checks position of arm. Basically a software limit check.'''

        # Calculate encoder counts relative to arm, and convert to degrees
        armAngle = (self.arm_encoder.getPosition() / Arm.GEAR_BOX_RATIO_ARM) * 64 * 360

        # Check if arm is extended (set to pick up algae)
        if armAngle >= 45 * 64:
            self.__isExtended__ = True
            print("CANT GO ANY MORE CAPTAIN")
        else:
            self.__isExtended__ = False

        # Check if arm is retracted (set to dispense coral or algae)
        if (self.arm_limit.getPressed() and not(self.__calibrated__)):
            self.arm_encoder.setPosition(0)        
            print("Retracted!")
            self.__calibrated__ = True
            self.__isRetracted__ = True


        if armAngle <= -5:
            self.__isRetracted__ = True

            # Motor will recalibrate itself automatically once it is back on neutral position
            if not(self.__calibrated__):
                self.arm_encoder.setPosition(0)
                self.__calibrated__ = True

        elif int(armAngle) !=0:
            # The motor is not considered calibrated once away from neutral retracted position
            self.__isRetracted__ = False
            self.__calibrated__ = False

    def activateRollers(self, direction: float):
        self.roller_motor.set(direction * Arm.ROLLER_POWER)

    def resetAndCalibrate(self):


        if not(self.__calibrated__):
            self.arm_motor.set(0.05)
        
        if self.arm_limit.getPressed():
            self.__isRetracted__ = True
            self.__calibrated__ = True
            self.arm_motor.set(0)
            self.arm_encoder.setPosition(0)
