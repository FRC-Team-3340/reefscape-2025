import wpilib as wpi
import wpimath.controller

import commands2 as cm2
import commands2.cmd as cmd
import commands2.button as btn
from commands2 import RunCommand

from subsystems.drive_subsystem import DriveTrainSubsystem
from subsystems.climber_subsystem import ClimberSubsystem
from subsystems.pieces_subsystem import PiecesSubsystem

from commands.DeepClimb import DeepClimb
from commands.UndoClimb import UndoClimb
from commands.HalfDrive import HalfDrive
from commands.TimedMove import TimedMove

from wpilib import PS4Controller,SmartDashboard



class RobotContainer():
    CONTROLLER_PORT = 0
    CONTROL_SCHEME = "tank"
    USE_EXPONENTIAL = False

    def __init__(self):
        self.robotDrive = DriveTrainSubsystem()
        self.robotClimber = ClimberSubsystem()
        self.robotArm = PiecesSubsystem()
        self.driverController = PS4Controller(port=RobotContainer.CONTROLLER_PORT)

        self.deepClimb = DeepClimb(self.robotClimber)
        self.undoClimb = UndoClimb(self.robotClimber)
        
        self.basic_auto = TimedMove(self.robotDrive, speed=0.4, time=5)

        self.chooser = wpi.SendableChooser()

        self.chooser.setDefaultOption("Basic Auto", self.basic_auto)
        SmartDashboard.putData(self.chooser)

        self.configureBindings()
        

        match(RobotContainer.CONTROL_SCHEME):
            case("tank"):
                self.robotDrive.setDefaultCommand(
                    cm2.RunCommand(
                        lambda: self.robotDrive.tankDrive(
                            left = -self.driverController.getLeftY(),
                            right= -self.driverController.getRightY(),
                            exp = RobotContainer.USE_EXPONENTIAL
                        ), self.robotDrive
                    )
                )
            case("mk"):
                self.robotDrive.setDefaultCommand(
                    cm2.RunCommand(
                        lambda: self.robotDrive.mkDrive(
                            fwd = self.driverController.getCircleButton(),
                            rev = self.driverController.getCrossButton(),
                            rot = self.driverController.getLeftX()
                        ), self.robotDrive
                    )
                )
            case("arcade"):
                self.robotDrive.setDefaultCommand(
                    cm2.RunCommand(
                        lambda: self.robotDrive.arcadeDrive(
                            fwd = self.driverController.getLeftY(),
                            rot = self.driverController.getRightX(),
                            exp = RobotContainer.CONTROL_SCHEME
                        ), self.robotDrive
                    )
                )
            
        
    def configureBindings(self):
        btn.JoystickButton(
            self.driverController, PS4Controller.Button.kL3
        ).whileTrue(
            command = lambda: HalfDrive()
        )
        btn.JoystickButton(
            self.driverController, PS4Controller.Button.kSquare
        ).onTrue(
            command = lambda: self.robotArm.extendArm()
        )
        
        btn.JoystickButton(
            self.driverController, PS4Controller.Button.kTriangle
        ).onTrue(
            command = lambda: self.robotArm.retractArm()
        )  

        # USE POVBUTTON FOR MANUAL CONTROL!!!
        btn.POVButton(
            self.driverController, 0
            
        ).whileTrue(
            command = lambda: self.deepClimb
        )

        btn.POVButton(
            self.driverController, 180
        ).whileTrue(
            command = lambda: self.undoClimb
        )
        btn.POVButton(
            self.driverController, 90
        ).whileTrue(
            command = lambda: self.robotArm.manualArmControl(1)
        ).onFalse(
            command = lambda: self.robotArm.manualArmControl(0)
        )

        btn.POVButton(
            self.driverController, 270
        ).whileTrue(
            command = lambda:self.robotArm.manualArmControl(-1)
        ).onFalse(
            command = lambda: self.robotArm.manualArmControl(0)
        )

        btn.JoystickButton(
            self.driverController, PS4Controller.Button.kR2
        ).whileTrue(
            self.robotArm.activateRollers(self.driverController.getR2Axis())
        ).onFalse(
            self.robotArm.activateRollers(0)
        )

        btn.JoystickButton(
            self.driverController, PS4Controller.Button.kL2
        ).whileTrue(
            self.robotArm.activateRollers(-self.driverController.getL2Axis())
        ).onFalse(
            self.robotArm.activateRollers(0)
        )

    def getAutonomousCommand(self) -> cm2.Command:
        return self.chooser.getSelected()
