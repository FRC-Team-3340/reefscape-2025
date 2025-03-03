
import wpilib
import wpilib.drive
from commands2 import Subsystem, Command
import commands2
from pathplannerlib.auto import AutoBuilder, PathPlannerAuto, NamedCommands
from pathplannerlib.controller import PPLTVController
from pathplannerlib.config import RobotConfig
from wpilib import DriverStation
import components.motors as m
from components.drive import Drive
# from wpilib.kinematics import ChassisSpeeds
# from wpilib.geometry import Pose2d
from pathplannerlib import PathPlanner, PathPlannerTrajectory, AutoBuilder, PathConstraints

class DriveSubsystem(Subsystem):

    def __init__(self):
        self.drive = Drive()

    def arcadeDrive(self, forward_speed, rotation_speed) -> Command:
        self.drive.arcadeDrive(forward_speed, rotation_speed, False)

    def stop(self):
        """Stops the robot's movement."""
        self.drive.stopMotor() 
       #########################################################
        # Load the RobotConfig from the GUI settings. You should probably
        # store this in your Constants file
        config = RobotConfig.fromGUISettings()

        # Configure the AutoBuilder last
        AutoBuilder.configure(
            self.getPose, # Robot pose supplier
            self.resetPose, # Method to reset odometry (will be called if your auto has a starting pose)
            self.getRobotRelativeSpeeds, # ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
            lambda speeds, feedforwards: self.driveRobotRelative(speeds), # Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds. Also outputs individual module feedforwards
            PPLTVController(0.02), # PPLTVController is the built in path following controller for differential drive trains
            config, # The robot configuration
            self.shouldFlipPath, # Supplier to control path flipping based on alliance color
            self # Reference to this subsystem to set requirements
        )

    def shouldFlipPath():
        # Boolean supplier that controls when the path will be mirrored for the red alliance
        # This will flip the path being followed to the red side of the field.
        # THE ORIGIN WILL REMAIN ON THE BLUE SIDE
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed
    
    from pathplannerlib.auto import PathPlannerAuto

class RobotContainer:
    def getAutonomousCommand():
        # This method loads the auto when it is called, however, it is recommended
        # to first load your paths/autos when code starts, then return the
        # pre-loaded auto/path
        return PathPlannerAuto('Example Auto')
    
    











    from pathplannerlib.auto import NamedCommands

class RobotContainer:
    def __init__(self):
        # Subsystem initialization
        self.swerve = Swerve()
        self.exampleSubsystem = ExampleSubsystem()

        # Register Named Commands
        NamedCommands.registerCommand('autoBalance', swerve.autoBalanceCommand())
        NamedCommands.registerCommand('exampleCommand', exampleSubsystem.exampleCommand())
        NamedCommands.registerCommand('someOtherCommand', SomeOtherCommand())

        # Do all other initialization
        self.configureButtonBindings()

        # ...