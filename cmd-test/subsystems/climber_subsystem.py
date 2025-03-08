from commands2 import Subsystem
from subsystems.components.climber import Climber
from typing import Literal

class ClimberSubsystem(Subsystem):
    def __init__(self):
        super().__init__()

        self.climber = Climber()

    def manualClimb(self, direction: float):
        self.climber.manualClimb(direction)

    def stopClimbing(self):
        self.climber.stopClimbing()
    