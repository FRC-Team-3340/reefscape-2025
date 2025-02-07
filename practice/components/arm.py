import motors as m
from switch import LimitSwitch as ls

# Arm does not inherit from another class unlike switch or drive.
# Arm consists of more than just one motor.


class Arm:
    def __init__(self):
        # create motor for the intake and "arm" mechanism
        self.roller_motor = m.createTalonSRX(
            5, neutral_mode=m.NeutralMode.Coast)

        self.arm_motor = m.createSparkMax(5, m.SparkMax.IdleMode.kBrake)

        # remember that encoder tracks rotations. gear box ratio is 64:1.
        # meaning: it takes 64 rotations of the motor for the gears to complete one rotation
        self.arm_encoder = m.createSparkMaxEncoder(self.arm_motor)

        self.arm_limit = ls(0)

        self.__hit_lower_limit__ = False
        self.__hit_upper_limit__ = False

        # TODO: Restrict maximum power of motors. Try 1/4.
        # TODO:
