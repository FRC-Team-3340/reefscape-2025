import wpilib as wpi
from components.drive import Drive
from components.climber import Climber

import components.motors as m
from components.switch import LimitSwitch


class MyRobot(wpi.TimedRobot):
    
    def robotInit(self):
        self.drive = Drive()
        self.climber = Climber()
        self.controller = wpi.XboxController(0)

        self.new_motor = m.createSparkMax(
            5, m.SparkMax.IdleMode.kBrake,  m.SparkMax.MotorType.kBrushless)
        self.new_motor.setVoltage(self.new_motor.getBusVoltage() / 4)

        wpi.cameraserver.CameraServer.launch()
        self.mySwitch = LimitSwitch(0)
        AutoBuilder.configure(
            lambda: get_pose(),  # Robot pose supplier
            lambda pose: reset_pose(pose),  # Method to reset odometry
            lambda: get_robot_relative_speeds(),  # ChassisSpeeds supplier (Robot Relative)
            lambda speeds, feedforwards: drive_robot_relative(speeds),  # Method to drive the robot
        )


        from wpilib.geometry import Pose2d, Rotation2d, Translation2d

def get_pose() -> Pose2d:
    """
    Returns the robot's current pose using odometry and/or sensor data.
    """
    # 1. Get data from odometry (e.g., using encoders and a gyro)
    # Example using a simulated method, replace with actual odometry logic
    x_position = get_current_x_position()  # in meters
    y_position = get_current_y_position()  # in meters
    rotation_angle = get_current_rotation()  # in degrees

    # 2. Create a Translation2d object for the position
    translation = Translation2d(x_position, y_position)

    # 3. Create a Rotation2d object for the orientation
    rotation = Rotation2d.fromDegrees(rotation_angle)

    # 4. Combine translation and rotation to create a Pose2d
    current_pose = Pose2d(translation, rotation)
    
    return current_pose

# Simulated methods - replace with your actual implementations
def get_current_x_position() -> float:
    """Implement logic to get the robot's x position."""
    # Replace with actual sensor data or odometry calculation
    return 0.0

def get_current_y_position() -> float:
    """Implement logic to get the robot's y position."""
    # Replace with actual sensor data or odometry calculation
    return 0.0

def get_current_rotation() -> float:
    """Implement logic to get the robot's rotation."""
    # Replace with actual gyro or encoder-based calculation
    return 0.0
    
        def get_pose() -> Pose2d:
            """Implement logic to return the robot's current pose."""
            ...

        def reset_pose(pose: Pose2d) -> None:
            """Implement logic to reset the robot's pose."""
            ...

        def get_robot_relative_speeds() -> ChassisSpeeds:
            """Implement logic to return the robot's current speeds, robot relative."""
            ...

        def drive_robot_relative(speeds: ChassisSpeeds, feedforwards) -> None:
            """Implement logic to drive the robot based on robot-relative speeds."""
            ...

    # def robotPeriodic(self):

    # Assigning buttons on selected controller to
    def teleopPeriodic(self):
        '''forward = (-self.controller.getRawButton(1) + self.controller.getRawButton(2)
                   )/(.5+(abs(self.controller.getRawAxis(0)) > 0.1))
        self.robotDrive.arcadeDrive(
             -self.controller.getLeftY(), -self.controller.getRightX()
        )

         try:
            self.robot_drive.arcadeDrive( 
                xSpeed=forward, zRotation=self.controller.getRawAxis(0))
        except Exception:
            raise Exception'''

        if self.controller.getRawButton(1):
            self.new_motor.set(0.3)
        else:
            self.new_motor.set(0)

        if self.mySwitch.get() == False:
            self.drive.tankDrive(-self.controller.getRawAxis(1),
                                 self.controller.getRawAxis(5))

        self.climber.climb(self.controller.getPOV())

        '''        
        arm_2 = (self.controller.getPOV() == 90 + self.controller.getPOV() == 270)
        self.new_motor.set(arm_2)
        '''

        

    def autonomousInit(self):
        self.timer = wpi.Timer()
        self.stage = 0
        self.timer.start()

    def autonomousPeriodic(self):
        match(self.stage):
            case 0:
                if self.timer.get() < 5:
                    self.drive.arcadeDrive(xSpeed=.75, zRotation=0)
                else:
                    self.stage += 1
            case 1:
                self.drive.arcadeDrive(xSpeed=0, zRotation=0)
                if self.timer.get() > 10:
                    self.stage += 1
            case 2:
                if self.timer.get() < 15:
                    self.drive.arcadeDrive(xSpeed=-.75, zRotation=0)
                else:
                    self.stage += 1
            case 3:
                self.drive.arcadeDrive(xSpeed=.0, zRotation=0)
                self.timer.stop()
