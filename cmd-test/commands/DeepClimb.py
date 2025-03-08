import commands2 as cmd2
from subsystems.climber_subsystem import ClimberSubsystem

class DeepClimb(cmd2.Command):
    def __init__(self, climber: ClimberSubsystem) -> None:
        super().__init__()

        self.climber = climber

    def execute(self) -> None:
        self.climber.manualClimb(direction = 1)
    
    def end(self,interrupt:bool) -> None:
        self.climber.stopClimbing()