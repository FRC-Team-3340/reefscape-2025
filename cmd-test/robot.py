from commands2 import TimedCommandRobot, Command, CommandScheduler
import commands2.cmd

import wpilib as wpi
from robotcontainer import RobotContainer

from typing import Optional

class MyRobot(TimedCommandRobot):
    def robotInit(self):
        self.autonomousCommmand: Optional[Command] = None
        self.container = RobotContainer()

        __autoReady__ = False

    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass
    
    def autonomousInit(self):
        self.autonomousCommand = self.container.getAutonomousCommand()

        if self.autonomousCommand is not None:
            __autoReady__ = True
            self.autonomousCommand.schedule()
        else: 
            print("Cannot find autonomous command")
            __autoReady__ = False

        def autonomousPeriodic(self):
            pass
        
        def teleopInit(self):
            if self.autonomousCommand is not None:
                self.autonomousCommand.cancel()
        
        def teleopPeriodic(self):
            pass
        
        def testInit(self):
            CommandScheduler.getInstance().cancelAll()
        