import commands2 as cmd2
from wpilib import Timer

from subsystems.drive_subsystem import DriveTrainSubsystem

class TimedMove(cmd2.Command):
    def __init__(self, drive: DriveTrainSubsystem, time: float, speed: float):
        super().__init__()

        self.drive = drive
        self.time = time     
        self.pwr = speed   # in seconds

        self.timer = Timer()
        

    def start(self):
        self.timer.start()

    def execute(self):
        self.drive.driveTrain.setMaxOutput(self.pwr)
        
        if self.timer.get() < self.time:
            self.drive.arcadeDrive(fwd=1, rot=0)

    def stop(self, interrupt:bool):
        self.drive.arcadeDrive(fwd=0 rot=0)
        self.drive.driveTrain.setMaxOutput(self.drive.driveTrain.MAX_POWER)
    