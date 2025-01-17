import wpilib as wpi
import wpilib.drive as drive
import rev
import phoenix5 as p5
from phoenix5 import NeutralMode as nm


class MyRobot(wpi.TimedRobot):
    # Functions for creating objects relating to our motors
    def createCIM(self, can_id, neutral_mode: p5.NeutralMode):
        '''Creates a motor controller object corresponding to a CTRE Talon SRX.'''
        motor = p5.WPI_TalonSRX(can_id)
        motor.setNeutralMode(neutral_mode)
        return motor

    def createSparkMax(self, can_id, neutral_mode: rev.CANSparkMax.IdleMode):
        '''Creates a motor controller object corresponding to a REV Robotics Spark MAX.'''
        motor = rev.CANSparkMax(can_id, neutral_mode)
        motor.setIdleMode(neutral_mode)
        return motor

    def createSparkMaxEncoder(self, controller: rev.CANSparkMax):
        '''Creates a relative encoder object given '''
        encoder = controller.getEncoder()
        return encoder

    def robotInit(self):
        self.controller = wpi.Joystick(0)
        motors = []
        for i in range(4):
            motors.append(self.createCIM(can_id=i, neutral_mode=nm.Coast))

        # Assigning motors to corressponding motor controllers (can change depending on wiring)
        self.left_train = wpi.MotorControllerGroup(motors[0], motors[1])
        self.right_train = wpi.MotorControllerGroup(motors[2], motors[3])

        # Inverted so both sets of wheels (left + right) move in same direction
        self.left_train.setInverted(True)

        self.robot_drive = drive.DifferentialDrive(
            leftMotor=self.left_train, rightMotor=self.right_train)

        # Setting max output (currently at 25% power)
        self.robot_drive.setMaxOutput(0.25)

        self.elevator_motor = self.createSparkMax(
            6, rev.CANSparkMax.IdleMode.kBrake)
        self.elevator_motor.setSoftLimit(
            rev.CANSparkMax.SoftLimitDirection.kForward, 100)
        self.elevator_motor.setSoftLimit(
            rev.CANSparkMax.SoftLimitDirection.kReverse, -100)
        self.elevator_motor.setVoltage(self.elevator_motor.getBusVoltage() / 2)

        self.elevator_encoder = self.createSparkMaxEncoder(self.elevator_motor)

        self.control_scheme = "arcade"
        self.arcade_drive_preference = "two-button"

        wpi.cameraserver.CameraServer.launch()

    # def robotPeriodic(self):

    # Assigning buttons on selected controller to
    def teleopPeriodic(self):
        match(self.control_scheme):
            case("arcade"):
                '''Arcade drive. Same configuration we used since 2023.'''
                match(self.control_scheme):
                    case("two-button"):
                        '''Emulates the control scheme of a particular racing game on the Switch.'''
                        acceleration = self.controller.getRawButton(
                            2) - self.controller.getRawButton(1)
                        rotation = self.controller.getRawAxis(0)

                    case("arcade two-stick"):
                        '''Most common configuration for Arcade.'''
                        acceleration = self.controller.getRawAxis(1)
                        rotation = self.controller.getRawAxis(3)

                    case ("arcade single-stick"):
                        '''One-stick control, like 2024.'''
                        acceleration = self.controller.getRawAxis(1)
                        rotation = self.controller.getRawAxis(0)

                self.robot_drive.arcadeDrive(
                    xSpeed=acceleration,
                    zRotation=rotation
                )

            case("tank"):
                '''Two sticks - corresponds to one wheel train.'''
                self.robot_drive.tankDrive(
                    leftSpeed=self.controller.getRawAxis(1),
                    rightSpeed=self.controller.getRawAxis(3)
                )

        arm = (self.controller.getPOV() == 0 + self.controller.getPOV() == 180)
        self.elevator_motor.set(arm)

    def autonomousInit(self):
        self.timer = wpi.Timer()
        self.stage = 0
        self.timer.start()

    def autonomousPeriodic(self):
        match(self.stage):
            case 0:
                if self.timer.get() < 5:
                    self.robot_drive.arcadeDrive(xSpeed=.75, zRotation=0)
                else:
                    self.stage += 1
            case 1:
                self.robot_drive.arcadeDrive(xSpeed=0, zRotation=0)
                if self.timer.get() > 10:
                    self.stage += 1
            case 2:
                if self.timer.get() < 15:
                    self.robot_drive.arcadeDrive(xSpeed=-.75, zRotation=0)
                else:
                    self.stage += 1
            case 3:
                self.robot_drive.arcadeDrive(xSpeed=.0, zRotation=0)
                self.timer.stop()
