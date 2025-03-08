from components.arm import Arm
from commands2 import Subsystem
from typing import Literal

class PiecesSubsystem(Subsystem):
    def __init__(self):
        '''Creates new PiecesSubsystem. Encompasses arm and intake/outtake mechanism for game pieces for 2025.'''
        super().__init__()

        # Port all code from Arm
        self.arm = Arm()

    def setArmMaxPower(self, pwr: float, stage: Literal['autonomous', 'teleoperated']):
        match stage:
            case 'autonomous':
                self.arm.ARM_MOTOR_POWER_AUTO = pwr
            case 'teleoperated':
                self.arm.ARM_MOTOR_POWER_MANUAL = pwr
    

    def setRollerMaxPower(self, pwr: float):
        self.arm.ROLLER_POWER = pwr

    def moveArm(self, input: float):
        self.arm.checkArmPosition()
        
        if not(self.arm.__switchingArmState__):
            if (input == 90):
                direction = -1
            elif (input == 270):
                direction = 1
            else:
                direction = 0

            if (not(self.arm.__isExtended__) and direction < 0):
                self.arm.arm_motor.set(direction * Arm.ARM_MOTOR_POWER_MANUAL)
            elif(not(self.arm.__isRetracted__) and direction > 0):
                self.arm.arm_motor.set(direction * Arm.ARM_MOTOR_POWER_MANUAL)
            else:
                self.arm.arm_motor.set(0)

    def manualArmControl(self, direction = float):
        if not(self.arm.__switchingArmState__):
            if (not(self.arm.__isExtended__) and direction < 0):
                self.arm.arm_motor.set(direction * Arm.ARM_MOTOR_POWER_MANUAL)
            elif(not(self.arm.__isRetracted__) and direction > 0):
                self.arm.arm_motor.set(direction * Arm.ARM_MOTOR_POWER_MANUAL)
            else:
                self.arm.arm_motor.set(0)


    def initializeArm(self):
        # to be done in the pit: executes only during Test mode

        # On startup: the robot is considered "not calibrated". 
        # Low power delivered to motor of arm to wind it back to its neutral position.
        if not(self.arm.__calibrated__):
            self.arm.arm_motor.set(0.05)
        
        # Limit switch mounted on robot neutral point. 
        # Robot is considered "calibrated" and retracted once triggered, and motor is set to standby
        if self.arm.arm_limit.getPressed():
            self.calibrate()

    def activateRollers(self, direction: float):
        self.arm.activateRollers(direction=direction)

    def extendArm(self):
        self.arm.extendArm()
    
    def retractArm(self):
        self.arm.retractArm()