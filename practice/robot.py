import wpilib as wpi
from components.drive import Drive
from components.climber import Climber
from components.arm import Arm

import components.motors as m
from components.switch import LimitSwitch


class MyRobot(wpi.TimedRobot):
    def robotInit(self):
        self.drive = Drive()
        self.climber = Climber()
        self.arm = Arm()
        self.controller = wpi.Joystick(0)

        wpi.cameraserver.CameraServer.launch()
        self.mySwitch = LimitSwitch(0)

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

        if self.mySwitch.get() == False:
            self.drive.tankDrive(self.controller.getRawAxis(1),
                                 self.controller.getRawAxis(5))
            # self.drive.arcadeDrive(self.controller.getRawAxis(1), self.controller.getRawAxis(4))

        self.climber.getActive()
        self.arm.manualArmControl((self.controller.getPOV() == 90 + self.controller.getPOV() == 270))


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
