from commands2 import Subsystem
from components.drive import Drive

from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PPLTVController
from pathplannerlib.config import RobotConfig
from wpilib import DriverStation, SmartDashboard, Field2d
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import ChassisSpeeds, DifferentialDriveKinematics, DifferentialDriveOdometry, DifferentialDriveWheelPositions

from navx import AHRS

class DriveTrainSubsystem(Subsystem):
    def __init__(self):
        '''Creates new DriveSubsystem'''
        super().__init__()

        # Port all code from components.Drive here if you want to use less files :D
        self.driveTrain = Drive()
        self.gyro = AHRS(comType=AHRS.NavXComType.kMXP_SPI)

        # PathPlanner setup
        self.__odometry__ = DifferentialDriveOdometry()
        self.__kinematics__ = DifferentialDriveKinematics()

        config = RobotConfig.fromGUISettings()      # Configure in FRC PathPlanner app

        AutoBuilder.configure(
            
        )




    def arcadeDrive(self, fwd: float, rot: float, exp: bool = False):
        '''
        Tried and true for 2 years!
        Use arcade controls to pilot robot.
            
            fwd: forward movement. Recommended: Vertical axis on joystick.
            rot: rotation. Recommended: Horizontal axis on joystick.
            exp: use square inputs instead of linear. at lower axis values, robot moves slower.
        '''

        self.driveTrain.arcadeDrive(xSpeed=fwd, zRotation=rot, squareInputs=exp)

    def tankDrive(self, left:float, right:float, exp:bool=False):
        '''
        Alternate control scheme.
        Use tank controls to pilot robot, where one axis controls its corresponding drive train.
            
            left: left train movement. Recommended: vertical axis on one joystick.
            right: rotation. Recommended: vertical axis on other joystick.
            exp: use square inputs instead of linear. at lower axis values, robot moves slower.
        '''
        self.driveTrain.tankDrive(leftSpeed=left, rightSpeed=right, squareInputs=exp)

    def mkDrive(self, fwd:bool, rev:bool, rot:float):
        '''
        Alternate control scheme suggested by Esteban.
        Control scheme aims to emulate that of a very popular racing game known for destroying friendships.

            fwd: button for accelerating. holding both fwd and rev cancel each other out.
            rev: button for reversing. holding both fwd and rev cancel each other out.
            rot: rotation axis.

        
        Implementation is still a bit jank so yeah...

        '''

        direction = int(fwd) - int(rev)

        left = direction * (-rot * rot<0)
        right = direction * (rot * rot>0)

        self.driveTrain.tankDrive(leftSpeed=left, rightSpeed=right, squareInputs=False)

    def setMaxOutput(self, pwr:float):
        '''
        Set maximum power output of robot. Configure if you want robot to move slower or faster based on circumstances.

            pwr: maximum power of robot. 
        '''
        self.driveTrain.setMaxOutput(pwr)

    def getPose(self) -> Pose2d:
        return self.__odometry__.getPose()
    
    def resetPose(self, pose: Pose2d):
        return self.__odometry__.resetPosition(gyroAngle=self.gyro.getRotation2d(), pose=pose)
    
    def getRobotRelativeSpeeds(self) -> ChassisSpeeds:
        return self.__kinematics__.toChassisSpeeds(getModuleStates())
    
    public Diff