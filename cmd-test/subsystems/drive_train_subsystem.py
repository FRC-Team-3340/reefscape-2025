from commands2 import Subsystem, Command
from wpilib import MotorControllerGroup
from wpilib.drive import DifferentialDrive
import components.motors as m
from components.drive import Drive

class DriveTrainSubsystem(Subsystem):
    def __init__(self):
        super().__init__()

        self.driveTrain = Drive()


