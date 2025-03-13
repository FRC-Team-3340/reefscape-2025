import wpilib as wpi
from wpilib import Joystick, CameraServer
from components.drive import Drive
from components.climber import Climber
from components.arm import Arm
import math
from networktables import NetworkTables

class MyRobot(wpi.TimedRobot):
    def robotInit(self):
        # Initialize robot components
        self.drive = Drive()
        self.climber = Climber()
        self.arm = Arm()
        self.controller = Joystick(0)

        # Initialize camera server for vision processing
        self.cs = CameraServer()
        self.cs.launch()

        # Initialize NetworkTables for Limelight (vision system)
        self.limelight_table = NetworkTables.getTable("limelight")
        
        # Timer for autonomous
        self.timer = wpi.Timer()
        self.stage = 1
        self.timer.start()

    def testPeriodic(self):
        self.arm.initializeArm()

    def teleopPeriodic(self):
        # Control robot's drive using joystick input
        self.drive.tankDrive(self.controller.getRawAxis(1), self.controller.getRawAxis(5))

        # Climber control using joystick POV (directional pad)
        self.climber.climb(self.controller.getPOV())

        # Arm roller control using joystick triggers
        roller_direction = -self.controller.getRawAxis(2) + self.controller.getRawAxis(3)
        self.arm.activateRollers(roller_direction)

    def autonomousInit(self):
        # Start the camera for vision processing
        self.camera = CameraServer.startAutomaticCapture()
        self.vision_distance = self.getVisionDistance()

    def autonomousPeriodic(self):
        match self.stage:
            case 0:
                if self.timer.get() > 3:
                    self.stage += 1
            case 1:
                target_distance = 36  # Target distance in inches
                vision_distance = self.getVisionDistance()
                
                if vision_distance > target_distance:
                    self.drive.arcadeDrive(xSpeed=-0.5, zRotation=0)  # Move forward
                else:
                    self.drive.arcadeDrive(0, 0)
                    self.stage += 1
            case 2:
                if self.timer.get() < 11:
                    self.drive.arcadeDrive(0, 0)
                    self.arm.activateRollers(direction=1)  # Engage rollers
                else:
                    self.stage += 1
            case 3:
                self.arm.activateRollers(0)  # Stop rollers

    def getVisionDistance(self):
        # Get the vertical angle (ty) to the target from Limelight
        ty = self.limelight_table.getEntry("ty").getDouble(0.0)
        
        # Limelight mounting and target information
        limelight_mount_angle_degrees = 25.0  # Angle limelight is mounted at
        limelight_lens_height_inches = 20.0  # Height of limelight from the floor
        goal_height_inches = 60.0  # Height of the target from the floor
        
        # Calculate angle to target
        angle_to_goal_degrees = limelight_mount_angle_degrees + ty
        angle_to_goal_radians = math.radians(angle_to_goal_degrees)
        
        # Compute distance from limelight to target
        if math.tan(angle_to_goal_radians) == 0:
            return -1  # Avoid division by zero
        
        distance = (goal_height_inches - limelight_lens_height_inches) / math.tan(angle_to_goal_radians)
        return distance
