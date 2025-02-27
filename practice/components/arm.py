import components.motors as m
from components.switch import LimitSwitch

# Arm does not inherit from another class unlike switch or drive.
# Arm consists of more than just one motor.


class Arm:
    # Class variables. Please adjust if necessary.
    GEAR_BOX_RATIO_ARM = 64     # Gear box ratio. It takes this many rotations of the motor for one rotaiton of the gearbox.
    ARM_MOTOR_POWER = .25       # Limit power output of robot. Expressed as a decimal from 0 to 1
    ROLLER_POWER = 0.25         # Limit power output of rollers on arm. Expressed as decimal from 0 to 1

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

    def toggleArm(self, toggle):
        # TODO: This code I wrote but not tested. Please fix if necessary. Rely on state variables.
        
        # flip-flop. Check if arm is not switching states (extend/retract) before switching.
        if toggle and not(self.__switchingArmState__):
            self.__setExtended__ = not(self.__setExtended__)   
            self.__switchingArmState__ = True

        if self.__setExtended__:
            # When the robot arm is extended, encoder rotations are negative.
            # To make calculations easier, I negate the position so that movement outward is positive.
            # ignore all values less than 0 for encoder. encoder rotations should floor to 0.
            currentRotations = -self.getArmRotations() if self.getArmRotations() >= 0 else 0
            target = 45

            if not(self.__isExtended__): 
                if currentRotations < 45:
                    speed = (1 - (currentRotations/target)) * Arm.ARM_MOTOR_POWER
                
                

        '''       
        Assuming encoder counts per full revolution is 2048
        To rotate 45 degrees (1/8th), we need to move 256 encoder counts
        target_position = self.arm_encoder.getPosition() + 256

        Set the target position for the arm motor to rotate 45 degrees
        self.arm_motor.getPIDController().setReference(target_position, m.SparkMax.ControlType.kPosition)        
        '''


    def retractArm(self):
        pass

    def extendArm(self):
        pass

    def manualArmControl(self, dpad: float):
        self.checkArmPosition()

        if (dpad == 90):
            direction = -1
        elif (dpad == 270):
            direction = 1
        else:
            direction = 0

        if (not(self.__isExtended__) and direction > 0):
            self.arm_motor.set(direction * Arm.ARM_MOTOR_POWER)
        elif(not(self.__isRetracted__) and direction < 0):
            self.arm_motor.set(direction * Arm.ARM_MOTOR_POWER)
        else:
            self.arm_motor.set(0)

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

        # # Check if arm is retracted (set to dispense coral or algae)
        # if (self.arm_limit.getPressed() and not(self.__calibrated__)):
        #     self.arm_encoder.setPosition(0)        
        #     print("Retracted!")
        #     self.__calibrated__ = True
        #     self.__isRetracted__ = True


        # if armAngle <= -5:
        #     self.__isRetracted__ = True

        #     # Motor will recalibrate itself automatically once it is back on neutral position
        #     if not(self.__calibrated__):
        #         self.arm_encoder.setPosition(0)
        #         self.__calibrated__ = True

        # elif int(armAngle) !=0:
        #     # The motor is not considered calibrated once away from neutral retracted position
        #     self.__isRetracted__ = False
        #     self.__calibrated__ = False

    def activateRollers(self, direction: float):
        self.roller_motor.set(direction * Arm.ROLLER_POWER)

    def resetAndCalibrate(self):
        # to be done in the pit: executes only during Test mode

        # On startup: the robot is considered "not calibrated". 
        # Low power delivered to motor of arm to wind it back to its neutral position.
        if not(self.__calibrated__):
            self.arm_motor.set(0.05)
        
        # Limit switch mounted on robot neutral point. 
        # Robot is considered "calibrated" and retracted once triggered, and motor is set to standby
        if self.arm_limit.getPressed():
            self.__isRetracted__ = True
            self.__calibrated__ = True
            self.arm_motor.set(0)
            self.arm_encoder.setPosition(0)
    
    def getArmRotations(self) -> float:
        '''returns arm rotations relative to arm itself, not the motor.'''
        return (self.arm_encoder.getPosition() / Arm.GEAR_BOX_RATIO_ARM) * 360