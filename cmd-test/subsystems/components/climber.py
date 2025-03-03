import components.motors as m

class Climber:
    def __init__(self):
        self.__power__ = 0.5

        assert self.__power__ <= 1

        self.climber_motor = m.createSparkMax(
            can_id= 6,
            motor_type= m.SparkLowLevel.MotorType.kBrushless
        )

        self.__isActive__ = False
        
    def climb(self, dpad):
        # USING THE DPAD
        if (dpad == 0):
            direction = 1
        elif (dpad == 180):
            direction = -1
        else:
            direction = 0

        self.manualClimb(direction=direction)


    def manualClimb(self, direction):
        self.__isActive__ = True if abs(self.climber_motor.getBusVoltage()) > 0 else False
        
        self.climber_motor.set(direction * self.__power__)

    def getActive(self) -> bool:
        return self.__isActive__
