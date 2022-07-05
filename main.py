from Electronic_Components.StepperMotor import StepperMotor
from Electronic_Components.RESOLUTION import RESOLUTION
import pigpio

if __name__ == '__main__':
    pi = pigpio.pi()
    motor1: StepperMotor = StepperMotor(sleep_pin=10, dir_pin=20, step_pin=21, mode_pins=(14, 15, 18),
                                        resolution=RESOLUTION.QUARTER, pi=pi)
    motor2: StepperMotor = StepperMotor(sleep_pin=9, dir_pin=23, step_pin=24, mode_pins=(2, 3, 4),
                                        resolution=RESOLUTION.QUARTER, pi=pi)
    motor3: StepperMotor = StepperMotor(sleep_pin=11, dir_pin=19, step_pin=26, mode_pins=(5, 6, 13),
                                        resolution=RESOLUTION.QUARTER, pi=pi)

    print('First Loop')
    motor1.turn_motor(3)
    motor2.turn_motor(3)
    motor3.turn_motor(3)
    print('Final Loop')
    motor1.turn_motor(3)
    motor2.turn_motor(3)
    motor3.turn_motor(3)
    print('Exiting')
    pi.stop()
