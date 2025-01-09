import wpilib as wpi
import wpilib.drive as drive
import phoenix5 as p5

class MyRobot(wpi.TimedRobot):
    def createCIM(self, ID, neutralMode: p5.NeutralMode):
        motor = p5.WPI_TalonSRX(ID)
        motor.setNeutralMode(neutralMode)
        return motor

    def robotInit(self):
        self.controller = wpi.Joystick(0)
        motors = []
        for i in range(4):
            motors.append(self.createCIM(i, p5.NeutralMode.Coast))

        self.left_train = wpi.MotorControllerGroup(motors[0], motors[1])
        self.right_train = wpi.MotorControllerGroup(motors[2], motors[3])
        
        self.left_train.setInverted(True)

        self.robot_drive = drive.DifferentialDrive(leftMotor=self.left_train, rightMotor=self.right_train)
        self.robot_drive.setMaxOutput(0.25)

    def teleopPeriodic(self):
        forward = (-self.controller.getRawButton(1) + self.controller.getRawButton(2))/(.5+(abs(self.controller.getRawAxis(0)) > 0.1))
        self.robot_drive.arcadeDrive(xSpeed=forward, zRotation=self.controller.getRawAxis(0))
    
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
                    self.stage+=1
            case 1:
                self.robot_drive.arcadeDrive(xSpeed=0, zRotation=0)
                if self.timer.get() > 10:
                    self.stage+=1
            case 2:
                if self.timer.get() < 15:
                    self.robot_drive.arcadeDrive(xSpeed=-.75, zRotation=0)
                else:
                    self.stage += 1
            case 3:
                self.robot_drive.arcadeDrive(xSpeed=.0, zRotation=0)
                self.timer.stop()


            
                    
            