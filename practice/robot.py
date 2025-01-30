import wpilib as wpi
import wpilib.drive as drive
import rev
import phoenix5 as p5
from phoenix5 import NeutralMode as nm

class MyRobot(wpi.TimedRobot):
    def createCIM(self, can_id, neutral_mode: p5.NeutralMode):
        motor = p5.WPI_TalonSRX(can_id)
        motor.setNeutralMode(neutral_mode)
        return motor

    def createSparkMax(self, can_id, neutral_mode: rev.SparkMax.IdleMode):
        motor = rev.SparkMax(can_id, rev.SparkLowLevel.MotorType.kBrushless)
        motor.IdleMode(neutral_mode)

        return motor
    
    def createSparkMaxEncoder(self, controller: rev.SparkMax):
        encoder = controller.getEncoder()
        return encoder

    def robotInit(self):
        self.controller = wpi.XboxController(0)
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

        self.elevator_motor = self.createSparkMax(6, rev.SparkMax.IdleMode.kBrake)
        self.elevator_motor.setVoltage(self.elevator_motor.getBusVoltage() / 2)

        self.new_motor = self.createSparkMax(4, rev.SparkMax.IdleMode.kBrake)
        self.new_motor.setVoltage(self.new_motor.getBusVoltage() / 2) 

        self.elevator_encoder = self.createSparkMaxEncoder(self.elevator_motor)

        wpi.cameraserver.CameraServer.launch()

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
        
        self.robot_drive.tankDrive(-self.controller.getLeftY(), -self.controller.getRightY())
        
        arm = (self.controller.getPOV() == 0 + self.controller.getPOV() == 180)
        self.elevator_motor.set(arm)

        arm_2 = (self.controller.getPOV() == 90 + self.controller.getPOV() == 270)
        self.new_motor.set(arm_2)

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


