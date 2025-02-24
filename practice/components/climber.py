import components.motors as m

class Climber():
    def __init__(self):
        self.__power__ = 0.1

        assert self.__power__ <= 1

        self.climber_motor = m.createSparkMax(6, m.SparkMax.IdleMode.kBrake, m.SparkMax.MotorType.kBrushless)
        self.climber_motor.IdleMode(m.SparkMax.IdleMode.kBrake)

        self.__isActive__ = False
        
    def climb(self, dpad):
        # USING THE DPAD
        if (dpad == 0):
            direction = 1
        elif (dpad == 180):
            direction = -1
        else:
            direction = 0

        self.__isActive__ = True if abs(self.climber_motor.getBusVoltage()) > 0 else False
        
        self.climber_motor.set(direction * self.__power__)

    def getActive(self) -> bool:
        return self.__isActive__
    


    '''
    Create algorithm:
    Over time, make power less, but using the   

    counteract 

    if power cut to climber after climbing, motor turns in reverse
    
    70lbs to kg*9.8m/s =
    if encoder value = -, we need to turn the motor forward (+) 
    calibrate every second 


    '''