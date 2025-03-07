import wpilib as wpi
import wpimath.controller

import commands2 as cm2
import commands2.cmd as cmd
import commands2.button as btn

from subsystems.drive_subsystem import DriveTrainSubsystem
from subsystems.climber_subsystem import ClimberSubsystem
from subsystems.pieces_subsystem import PiecesSubsystem

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
            self.driverController, PS4Controller.Button.kSquare
        ).onTrue(
            
        )
        btn.JoystickButton(
            self.driverController, PS4Controller.Button.kL3
        ).whileTrue(
            
        )
        btn.JoystickButton(
            self.driverController, PS4Controller.Button.kSquare
        ).onTrue(
            command = lambda: self.robotArm.extendArm()
        )
        
        btn.JoystickButton(
            self.driverController, PS4Controller.Button.kTriangle
        ).onTrue(
            command = lambda: self.robotArm.extendArm()
        )  

        # USE POVBUTTON FOR MANUAL CONTROL!!!
        btn.POVButton(
            self.driverController,0
            
        ).onTrue(
            command = lambda: self.robotClimber.manualClimb(direction=1)
        )

    