import components.motors as m
from components.switch import LimitSwitch
from typing import Literal

# Arm does not inherit from another class unlike switch or drive.
# Arm consists of more than just one motor.


class Arm:
    GEAR_BOX_RATIO_ARM = 64
    ARM_MOTOR_POWER_MANUAL = 0.15
    ARM_MOTOR_POWER_AUTO = 0.25
    ROLLER_POWER = 0.25
    RETRACTION_LIMIT = "switch"

    def __init__(self):
        # create MotorController reference reference for the intake mechanism
        self.roller_motor = m.createTalonSRX(
            7, neutral_mode=m.NeutralMode.Brake)   

        # create MotorController Object for the arm mechanism. note that you must set the Idle Mode on REV Hardware Client.
        self.arm_motor = m.createSparkMax(
            can_id= 5,
            motor_type= m.SparkLowLevel.MotorType.kBrushless
        )

        # create reference to encoder for motor. tracks rotations of the motor (may be inaccurate at times)
        self.arm_encoder = m.createSparkMaxEncoder(self.arm_motor)
        # remember that encoder tracks rotations. gear box ratio is 64:1.
        # meaning: it takes 64 rotations of the motor for the gears to complete one rotation
        # 0.125 or 1/8th gear box rotation = 45 degrees (theoretically)

        # Create limit switch object on DIO 0.
        self.arm_limit = LimitSwitch(0)

        # state variables for robot. avoid access outside of class.
        self.__calibrated__ = False
        self.__isExtended__ = False
        self.__isRetracted__ = False

        self.__setExtended__  = False
        self.__switchingArmState__ = False

        self.arm_encoder.setPosition(0)

    def retractArm(self):  
        '''retracts arm''' 
        deltaAngle = 45
        self.__switchingArmState__ = True
        self.__setExtended__ = False

        # For retract arm: we get the encoder value as given (negative when extended)
        # We want to make it so that the motor turns until it reaches its limit
        currentRotations = self.getArmRotations(enableCutOff=True, cutoff="positive")
        
        targetChange = 45

        # two implementations are provided: physical limit (switch) or soft limit (encoder)
        # switch recommended!
        if (currentRotations + deltaAngle < targetChange):
            speed = ((currentRotations) / targetChange) * Arm.ARM_MOTOR_POWER_AUTO if currentRotations > targetChange/3 else Arm.ARM_MOTOR_POWER_MANUAL

            if Arm.RETRACTION_LIMIT == "switch":
                if self.arm_limit.getPressed():
                    self.calibrate()
                    self.__switchingArmState__ = False
                else:
                    self.arm_motor.set(speed=speed)

            elif Arm.RETRACTION_LIMIT == "encoder":               
                if currentRotations <= 0:
                    self.calibrate()
                else:
                    self.arm_motor.set(speed=speed)

    def extendArm(self):
        '''extends arm''' 
        self.__switchingArmState__ = True
        self.__setExtended__ = True

        # For extend arm: we negate the encoder value as its negative when extended.
        # We want to make it so that the motor turns until it reaches its limit
        currentRotations = -self.getArmRotations(enableCutOff=True, cutoff="negative")
        
        targetChange = 45

        # two implementations are provided: physical limit (switch) or soft limit (encoder)
        # switch recommended!
        if (currentRotations < targetChange):
            speed = (1-((currentRotations) / targetChange)) * Arm.ARM_MOTOR_POWER_AUTO if currentRotations > (2/3 * targetChange) else Arm.ARM_MOTOR_POWER_MANUAL
    
        if currentRotations > targetChange:
            self.arm_motor.set(0)
            self.__switchingArmState__ = False
        else:
            self.arm_motor.set(speed=speed)

                

    def toggleArm(self, toggle):
        # TODO: This code I wrote but not tested. Please fix if necessary. Rely on state variables.
        
        # flip-flop. Check if arm is not switching states (extend/retract) before switching.
        if toggle and not(self.__switchingArmState__):
            self.__setExtended__ = not(self.__setExtended__)   
            self.__switchingArmState__ = True

        if(self.__switchingArmState__):
            if self.__setExtended__:
                self.extendArm()
            elif not(self.__setExtended__):
                self.retractArm()                
                

        '''       
        Assuming encoder counts per full revolution is 2048
        To rotate 45 degrees (1/8th), we need to move 256 encoder counts
        target_position = self.arm_encoder.getPosition() + 256

        Set the target position for the arm motor to rotate 45 degrees
        self.arm_motor.getPIDController().setReference(target_position, m.SparkMax.ControlType.kPosition)        
        '''

    def checkArmPosition(self):
        '''Checks position of arm. Basically a software limit check.'''

        # Calculate encoder counts relative to arm, and convert to degrees
        armAngle = self.getArmRotations()
        print(self.arm_encoder.getPosition())
        # # Check if arm is extended (set to pick up algae)
        # if armAngle >= 45 * 64:
        #     self.__isExtended__ = True
        #     print("CANT GO ANY MORE CAPTAIN")
        # else:
        #     self.__isExtended__ = False

        # Check if arm is extended (set to pick up algae)
        if armAngle <= -45:
            self.__isExtended__ = True
        else:
            self.__isExtended__ = False

        # Check if arm is retracted (set to dispense coral or algae)
        if (self.arm_limit.get() and not(self.__calibrated__)):
            self.arm_encoder.setPosition(0)        
            self.__calibrated__ = True
            self.__isRetracted__ = True


        if armAngle >= 5:
            self.__isRetracted__ = True

            # Motor will recalibrate itself automatically once it is back on neutral position
            if not(self.__calibrated__):
                self.arm_encoder.setPosition(0)
                self.__calibrated__ = True

        elif int(armAngle) !=0:
            # The motor is not considered calibrated once away from neutral retracted position
            self.__isRetracted__ = False
            self.__calibrated__ = False

    def activateRollers(self, direction: float):
        self.roller_motor.set(direction * Arm.ROLLER_POWER)

    def calibrate(self):
        self.__isRetracted__ = True
        self.__calibrated__ = True
        self.arm_motor.set(0)
        self.arm_encoder.setPosition(0)

    
    def getArmRotations(self, enableCutOff: bool = False, cutoff: str = Literal["negative", "positive"]) -> float:
        '''returns arm rotations relative to arm itself, not the motor.'''

        # note that encoder is in the negatives when it is extended.
        position = (self.arm_encoder.getPosition() / Arm.GEAR_BOX_RATIO_ARM) * 360

        if enableCutOff:
            match(cutoff):
                case ("negative") :
                    position = 0 if (position < 0) else position
                case ("positive"):
                    position = 0 if (position > 0) else position

        return position
    