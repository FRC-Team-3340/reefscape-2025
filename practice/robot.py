import wpilib as wpi
from components.drive import Drive

import rev
import phoenix5 as p5
from phoenix5 import NeutralMode as nm

import components.motors as m

class MyRobot(wpi.TimedRobot):
    def robotInit(self):
        self.drive = Drive()
        self.controller = wpi.XboxController(0)

        self.elevator_motor = m.createSparkMax(6, m.SparkMax.IdleMode.kBrake, m.SparkMax.MotorType.kBrushless)
        self.elevator_motor.setVoltage(self.elevator_motor.getBusVoltage() / 2)

        self.new_motor = m.createSparkMax(5, m.SparkMax.IdleMode.kBrake,  m.SparkMax.MotorType.kBrushless)
        self.new_motor.setVoltage(self.new_motor.getBusVoltage() / 2) 

        self.elevator_encoder = m.createSparkMaxEncoder(self.elevator_motor)

        wpi.cameraserver.CameraServer.launch()
        self.mySwitch = wpi.DigitalInput(0)
        
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
        
        if self.driveSwitch.get() == False:
            self.drive.tankDrive(-self.controller.getRawAxis(1), self.controller.getRawAxis(5))
        
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


