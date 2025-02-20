import motors as m
from switch import LimitSwitch as ls

# Arm does not inherit from another class unlike switch or drive.
# Arm consists of more than just one motor.


class Arm:
    def __init__(self):
        # create motor for the intake and "arm" mechanism
        self.roller_motor = m.createTalonSRX(
            5, neutral_mode=m.NeutralMode.Coast)


        # made the code but the motor isnt working properly, I will check over in the REV app and then re-make the code
        # I feel like we're registering the motors incorrectly+        
        self.arm_motor = self.new_motor
        self.arm_encoder = m.createSparkMaxEncoder(self.arm_motor)
        self.arm_motor.setIdleMode(m.SparkMaxLowLevel.IdleMode.kBrake)

        # remember that encoder tracks rotations. gear box ratio is 64:1.
        # meaning: it takes 64 rotations of the motor for the gears to complete one rotation
        # 0.125 or 1/8th gear box rotation = 45 degrees (theoretically)

        self.arm_encoder = m.createSparkMaxEncoder(self.arm_motor)

        self.arm_limit = ls(0)

        self.__hit_lower_limit__ = False
        self.__hit_upper_limit__ = False

    def rotate_arm_45_degrees(self):
        # Assuming encoder counts per full revolution is 2048
        # To rotate 45 degrees (1/8th), we need to move 256 encoder counts
        target_position = self.arm_encoder.getPosition() + 256

        # Set the target position for the arm motor to rotate 45 degrees
        self.arm_motor.getPIDController().setReference(target_position, m.SparkMax.ControlType.kPosition)


        # TODO: Restrict maximum power of motors. Try 1/4.
        # TODO:
    def catcher(self, dpad: int):
        if (dpad == 90):
            self.rotate_arm_45_degrees()