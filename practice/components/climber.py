from rev import SparkMax

class Climber(SparkMax):
    def __init__(self):
        MAX_POWER = 0.25
        super().__init__(6, SparkMax.MotorType.kBrushless)
        self.IdleMode(SparkMax.IdleMode.kBrake)
        
        assert MAX_POWER <= 1
        self.setVoltage(MAX_POWER * 12)

    def climb(self, dpad: int):
        # USING THE DPAD
        print(dpad)
        if (dpad != -1):
            
            self.set(0)
