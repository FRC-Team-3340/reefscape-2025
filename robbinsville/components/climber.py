from sre_constants import CATEGORY_LOC_NOT_WORD
import components.motors as m
from wpilib import Servo, SmartDashboard

CLIMBER_POWER = 0.5


climber_motor = m.createSparkMax(can_id=6, motor_type=m.SparkLowLevel.MotorType.kBrushless)
climber_encoder = m.createSparkMaxEncoder(controller=climber_motor)
cageLock_servo = Servo(channel=0)

assert CLIMBER_POWER >= 0 and CLIMBER_POWER <= 1

class Climber:
    def __init__(self):
        self.__isActive__ = False
        self.__cageLock__ = False
        self.__performCageLock__ = True

        
    def climb(self, dpad):
        # USING THE DPAD
        if (dpad == 0):
            direction = 1
        elif (dpad == 180):
            direction = -1
        else:
            direction = 0

        self.__isActive__ = True if abs(climber_motor.getBusVoltage()) > 0 else False
        
        climber_motor.set(direction * CLIMBER_POWER)

    def getClimberActive(self) -> bool:
        return self.__isActive__
    
    def getCageLock(self) -> bool:
        return self.__cageLock__

    def updateDashboard(self):
        SmartDashboard.putNumber("Climber position", climber_encoder.getPosition())
        SmartDashboard.putBoolean("Cage Lock", self.__cageLock__)

    def toggleCageLock(self, input: bool):
        if (input == True) and not(self.__performCageLock__):
            self.__performCageLock__ = True
            if (self.__cageLock__ == False):
                cageLock_servo.setPosition(1)
                self.__cageLock__ = True
                
            elif (self.__cageLock__ == True):
                cageLock_servo.setPosition(0)
                self.__cageLock__ = False
        
        elif not(input): 
            self.__performCageLock__ = False


    '''
    Create algorithm:
    Over time, make power less, but using the   

    counteract 

    if power cut to climber after climbing, motor turns in reverse
    
    70lbs to kg*9.8m/s =
    if encoder value = -, we need to turn the motor forward (+) 
    calibrate every second 


    '''