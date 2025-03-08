import wpilib as wpi
import wpimath.controller

import commands2 as cm2
import commands2.cmd as cmd
import commands2.button as btn

from subsystems.drive_subsystem import DriveTrainSubsystem
from subsystems.climber_subsystem import ClimberSubsystem
from subsystems.pieces_subsystem import PiecesSubsystem

from commands.DeepClimb import DeepClimb
from commands.UndoClimb import UndoClimb
from commands.HalfDrive import HalfDrive

from wpilib import PS4Controller




class RobotContainer():
    CONTROLLER_PORT = 0
    CONTROL_SCHEME = "tank"
    USE_EXPONENTIAL = False

    def __init__(self):
        self.robotDrive = DriveTrainSubsystem()
        self.robotClimber = ClimberSubsystem()
        self.robotArm = PiecesSubsystem()
        self.driverController = PS4Controller(port=RobotContainer.CONTROLLER_PORT)

        self.robotArm.setDefaultCommand(
            cm2.runcommand(
                lambda: self.robotArm.activateRollers(

                )
            )
        )
        

        match(RobotContainer.CONTROL_SCHEME):
            case("tank"):
                self.robotDrive.setDefaultCommand(
                    cm2.runcommand(
                        lambda: self.robotDrive.tankDrive(
                            left = self.driverController.getLeftY(),
                            right= self.driverController.getRightY(),
                            exp = RobotContainer.USE_EXPONENTIAL
                        )
                    )
                )
            case("mk"):
                self.robotDrive.setDefaultCommand(
                    cm2.runcommand(
                        lambda: self.robotDrive.mkDrive(
                            fwd = self.driverController.getCircleButton(),
                            rev = self.driverController.getCrossButton(),
                            rot = self.driverController.getLeftX()
                        )
                    )
                )
            case("arcade"):
                self.robotDrive.setDefaultCommand(
                    cm2.runcommand(
                        lambda: self.robotDrive.arcadeDrive(
                            fwd = self.driverController.getLeftY(),
                            rot = self.driverController.getRightX(),
                            exp = RobotContainer.CONTROL_SCHEME
                        )
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
            command = lambda: self.DeepClimb()
        )

        btn.POVButton(
            self.driverController, 180
        ).whileTrue(
            command = lambda: self.UndoClimb()
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

    