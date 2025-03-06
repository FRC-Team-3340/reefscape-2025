from commands2 import Command
from subsystems.drive_subsystem import DriveTrainSubsystem

class HalfDrive(Command):
    def __init__(self, drive:DriveTrainSubsystem):
        super().__init__()
        self.drive = drive

    def start(self) -> None:
        self.drive.setMaxOutput(self.drive.driveTrain.MAX_POWER / 2)

    def end(self, interrupt: bool) -> None:
        self.drive.setMaxOutput(self.drive.driveTrain.MAX_POWER)