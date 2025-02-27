
import wpilib
import wpilib.drive
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PPLTVController
from pathplannerlib.config import RobotConfig
from wpilib import DriverStation
from pathplannerlib import PathPlanner, PathPlannerTrajectory, AutoBuilder, PathConstraints
from wpilib.geometry import Pose2d
from wpilib.kinematics import ChassisSpeeds

class DriveSubsystem(Subsystem):

     def __init__(self):
        self.front_left = m.createTalonSRX(0, neutral_mode=m.NeutralMode.Coast)
        self.back_left = m.createVictorSPX(1, neutral_mode=m.NeutralMode.Coast)
        self.front_right = m.createVictorSPX(2, neutral_mode=m.NeutralMode.Coast)
        self.back_right =m.createVictorSPX(3, neutral_mode=m.NeutralMode.Coast)

        # Group the left and right motors
        self.left_motors = wpilib.MotorControllerGroup(self.left_front_motor, self.left_rear_motor)
        self.right_motors = wpilib.MotorControllerGroup(self.right_front_motor, self.right_rear_motor)

        # Create a differential drive object
        self.drive = wpilib.drive.DifferentialDrive(self.left_motors, self.right_motors)

    def arcade_drive(self, forward_speed, rotation_speed):
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