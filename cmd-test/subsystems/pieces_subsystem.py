from components.arm import Arm
from commands2 import Subsystem

class PiecesSubsystem(Subsystem):
    def __init__(self):
        self.arm = Arm()