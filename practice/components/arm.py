import components.motors as m
from components.switch import LimitSwitch
from typing import Literal

# Arm does not inherit from another class unlike switch or drive.
# Arm consists of more than just one motor.


class Arm:
    ARM_GEARBOX_RATIO = 64    #(num rotations of motor):1
    ARM_MANUAL_POWER = 0.15   # 0 - 1
    ARM_AUTO_POWER = 0.25     # 0 - 1
    ARM_ROLLER_POWER = 0.25   # 0 - 1
    ARM_ROTATION_DELTA = 45   # degrees

    # change if you want a software or hardware limit control.
    # hardware uses limit switches and is most accurate, software relies only on encoder.
    # options, please type as is: switch / encoder
    RETRACTION_LIMIT = "switch"

    # DO NOT DELETE > These check if the variables are valid. 
    # Code will NOT deploy if variable is configured incorrectly.
    assert ARM_GEARBOX_RATIO >= 0
    assert ARM_MANUAL_POWER >= 0 and ARM_MANUAL_POWER <= 1
    assert ARM_AUTO_POWER >= 0 and ARM_AUTO_POWER <= 1
    assert ARM_ROLLER_POWER >= 0 and ARM_ROLLER_POWER <= 1
    assert ARM_ROTATION_DELTA > 0 and ARM_ROTATION_DELTA <= 90
    assert RETRACTION_LIMIT in ["switch", "encoder"]

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
        '''Automatically retracts arm. Implemented primarily for Autonomous phase.''' 
        # Offset - Encoder reads angle as negative when extended. We add the delta for our calculations.
        # As the encoder approaches our robot's neutral position, the offset will ensure it approaches 
        # our intended change in rotation.
        offset = Arm.ARM_ROTATION_DELTA
        self.__switchingArmState__ = True
        self.__setExtended__ = False
        self.__isExtended__ = False

        # For retract arm: we get the encoder value as given (negative when extended)
        # We want to make it so that the motor turns until it reaches its limit
        # Assuming the angle is correct, it should be within 45 degrees forward.
        currentRotations = self.getArmAngle(enableCutOff=True, cutoff="positive")
    
        if (currentRotations + offset < Arm.ARM_ROTATION_DELTA):
            # Speed check. Set motor to a minimum low speed if arm approaches destination (at least 1/3 more to go)
            # Otherwise, slow down as it approaches the target.
            if (currentRotations > Arm.ARM_ROTATION_DELTA / 3):
                speed = ((currentRotations) / Arm.ARM_ROTATION_DELTA) * Arm.ARM_AUTO_POWER
            else:
                speed = Arm.ARM_MANUAL_POWER

            # two implementations are provided: physical limit (switch) or soft limit (encoder)
            # switch recommended! configure in line 18 
            if Arm.RETRACTION_LIMIT == "switch":
                # Limit switch solution: arm continues to retract until the switch is tripped. 
                if self.arm_limit.getPressed():
                    self.calibrateArm()
                else:
                    self.arm_motor.set(speed=speed)

            # using the encoder, the motor's speed is always limited to manual speed.
            # this prevents the arm from shaking too much, which can affect the encoder reading.
            elif Arm.RETRACTION_LIMIT == "encoder":               
                if currentRotations <= 0:
                    self.calibrateArm()
                else:
                    self.arm_motor.set(speed=Arm.ARM_MANUAL_POWER)
            

    def extendArm(self):
        '''Automatically extends arm. Implemented primarily for Autonomous phase.''' 
        self.__switchingArmState__ = True
        self.__setExtended__ = True

        # For extend arm: we negate the encoder value as its negative when extended.
        # We want to make it so that the motor turns until it reaches its limit
        currentRotations = -self.getArmAngle(enableCutOff=True, cutoff="negative")

        if (currentRotations < Arm.ARM_ROTATION_DELTA):
            
            speed = (1-((currentRotations) / Arm.ARM_ROTATION_DELTA)) * Arm.ARM_AUTO_POWER if currentRotations > (2/3 * Arm.ARM_ROTATION_DELTA) else Arm.ARM_MANUAL_POWER
    
        if currentRotations > Arm.ARM_ROTATION_DELTA:
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
        
    def manualArmControl(self, dpad: float):
        self.checkArmPosition()

        if (dpad == 90):
            direction = -1
        elif (dpad == 270):
            direction = 1
        else:
            direction = 0

        if (not(self.__isExtended__) and direction < 0):
            self.arm_motor.set(direction * Arm.ARM_MANUAL_POWER)
        elif(not(self.__isRetracted__) and direction > 0):
            self.arm_motor.set(direction * Arm.ARM_MANUAL_POWER)
        else:
            self.arm_motor.set(0)

    def checkArmPosition(self):
        '''Checks position of arm. Basically a software limit check.'''

        # Calculate encoder counts relative to arm, and convert to degrees
        armAngle = self.getArmAngle()
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
            print("CANT GO ANY MORE CAPTAIN")
        else:
            self.__isExtended__ = False

        # Check if arm is retracted (set to dispense coral or algae)
        if (self.arm_limit.get() and not(self.__calibrated__)):
            self.arm_encoder.setPosition(0)        
            print("Retracted!")
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
        self.roller_motor.set(direction * Arm.ARM_ROLLER_POWER)

    def initializeArm(self):
        # to be done in the pit: executes only during Test mode

        # On startup: the robot is considered "not calibrated". 
        # Low power delivered to motor of arm to wind it back to its neutral position.
        if not(self.__calibrated__):
            self.arm_motor.set(0.05)
        
        # Limit switch mounted on robot neutral point. 
        # Robot is considered "calibrated" and retracted once triggered, and motor is set to standby
        if self.arm_limit.getPressed():
            self.calibrateArm()

    def calibrateArm(self):
        self.__isRetracted__ = True
        self.__calibrated__ = True
        self.__switchingArmState__ = False
        self.arm_motor.set(0)
        self.arm_encoder.setPosition(0)

    
    def getArmAngle(self, enableCutOff: bool = False, cutoff: str = Literal["negative", "positive"]) -> float:
        '''returns arm rotations relative to arm itself, not the motor.'''

        # note that encoder is in the negatives when it is extended.
        position = (self.arm_encoder.getPosition() / Arm.ARM_GEARBOX_RATIO) * 360

        if enableCutOff:
            match(cutoff):
                case ("negative") :
                    position = 0 if (position < 0) else position
                case ("positive"):
                    position = 0 if (position > 0) else position

        return position