from commands2 import Command
from subsystems.pieces_subsystem import PiecesSubsystem
class extendArm(Command):
    def __init__(self, arm:PiecesSubsystem) -> None:
        super().__init__()

        self.arm = arm

    def execute(self) -> None:
        self.arm.extendArm()
    
    def end(self,interrupt:bool) -> None:
        self.arm.stopClimbing()