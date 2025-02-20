from phoenix5 import NeutralMode, WPI_TalonSRX
from rev import SparkMax 

# think of this file as an abstract class because it isn't really a class but it contains the
# functions that most of the other classes rely on.

def createSparkMax(can_id: int, neutral_mode: SparkMax.IdleMode, motor_type: SparkMax.MotorType) -> SparkMax:
    motor = SparkMax(can_id, motor_type)
    motor.IdleMode(neutral_mode)

    return motor

def createTalonSRX(can_id: int, neutral_mode: NeutralMode) -> WPI_TalonSRX:
    motor = WPI_TalonSRX(can_id)
    motor.setNeutralMode(neutral_mode)

    return motor
    
def createSparkMaxEncoder(controller: SparkMax):
    return controller.getEncoder()

                    