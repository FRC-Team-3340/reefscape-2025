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

    def createSparkMax(self, can_id, neutral_mode: rev.CANSparkMax.IdleMode):
        motor = rev.CANSparkMax(can_id, rev.CANSparkLowLevel.MotorType.kBrushless)
        motor.setIdleMode(neutral_mode)

        return motor
    
    def createSparkMaxEncoder(self, controller: rev.CANSparkMax):
        encoder = controller.getEncoder()
        return encoder

    def robotInit(self):
        self.controller = wpi.Joystick(0)
        motors = []
        for i in range(5):
            motors.append(self.createCIM(can_id=i, neutral_mode=nm.Coast))

        # Assigning motors to corressponding motor controllers (can change depending on wiring)
        self.left_train = wpi.MotorControllerGroup(motors[0], motors[1])
        self.right_train = wpi.MotorControllerGroup(motors[2], motors[3])
        self.addPeriodic

        # Inverted so both sets of wheels (left + right) move in same direction
        self.left_train.setInverted(True)

        self.robot_drive = drive.DifferentialDrive(
            leftMotor=self.left_train, rightMotor=self.right_train)

        # Setting max output (currently at 25% power)
        self.robot_drive.setMaxOutput(0.25)

        self.elevator_motor = self.createSparkMax(6,rev.CANSparkMax.IdleMode.kBrake)

        self.elevator_encoder = self.createSparkMaxEncoder(self.elevator_motor)

        wpi.cameraserver.CameraServer.launch()

    # def robotPeriodic(self):

    # Assigning buttons on selected controller to
    def teleopPeriodic(self):
        forward = (-self.controller.getRawButton(1) + self.controller.getRawButton(2)
                   )/(.5+(abs(self.controller.getRawAxis(0)) > 0.1))

        try:

            self.robot_drive.arcadeDrive(
                xSpeed=forward, zRotation=self.controller.getRawAxis(0))
        except Exception:
            raise Exception
        
        arm = (self.controller.getPOV() == 0, self.controller.getPOV() == 180)

        

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


if __name__ == "__main__":
    wpi.run(MyRobot)
