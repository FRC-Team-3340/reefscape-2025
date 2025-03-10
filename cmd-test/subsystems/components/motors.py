from phoenix5 import NeutralMode, WPI_TalonSRX, WPI_VictorSPX
from rev import SparkMax, SparkLowLevel

# think of this file as an abstract class because it isn't really a class but it contains the
# functions that most of the other classes rely on.

def createSparkMax(can_id: int, motor_type: SparkLowLevel.MotorType) -> SparkMax:
    '''
    can_id: the assigned ID of the SparkMax motor controller via REV client.
    motor_type: the motor type connected to the controller.
    '''
    motor = SparkMax(can_id, motor_type)

    return motor

def createVictorSPX(can_id: int, neutral_mode: NeutralMode) -> WPI_VictorSPX:
    '''
    can_id: the assigned ID of the VictorSPX motor controller via Phoenix Tuner X.
    neutral_mode: set the behavior of the motor during neutral output (0).
    '''
    motor = WPI_VictorSPX(can_id)
    motor.setNeutralMode(neutral_mode)

    return motor

def createTalonSRX(can_id: int, neutral_mode: NeutralMode) -> WPI_TalonSRX:
    '''
    can_id: the assigned ID of the TalonSRX motor controller via Phoenix Tuner X.
    neutral_mode: set the behavior of the motor during neutral output (0).
    '''
    motor = WPI_TalonSRX(can_id)
    motor.setNeutralMode(neutral_mode)

    return motor
    
def createSparkMaxEncoder(controller: SparkMax):
    '''
    controller: get the relative encoder of this SparkMAX motor controller.
    '''
    return controller.getEncoder()

                    