import time

import pigpio

from Electronic_Components.RESOLUTION import RESOLUTION
from Electronic_Components.StepperMotor import StepperMotor

if __name__ == '__main__':
    pi = pigpio.pi()
    # whole nuts
    motor1: StepperMotor = StepperMotor(sleep_pin=10, dir_pin=20, step_pin=21, mode_pins=(14, 15, 18),
                                        resolution=RESOLUTION.QUARTER, pi=pi)
    # chopped nuts
    motor2: StepperMotor = StepperMotor(sleep_pin=9, dir_pin=23, step_pin=24, mode_pins=(2, 16, 4),
                                        resolution=RESOLUTION.QUARTER, pi=pi)
    # worms
    motor3: StepperMotor = StepperMotor(sleep_pin=11, dir_pin=19, step_pin=26, mode_pins=(5, 6, 13),
                                        resolution=RESOLUTION.QUARTER, pi=pi)

sleep_count = 0


def on_weight(weight_grams):
    global sleep_count
    if sleep_count > 0:
        return
    if weight_grams > 150:
        # dispense whole nuts
        motor1.set_turning()
        time.sleep(0.5)
        motor1.stop()
        sleep_count = 20
    elif weight_grams > 25:
        # dispense chopped nuts and worms
        motor2.set_turning()
        motor3.set_turning()
        time.sleep(0.75)
        motor2.stop()
        time.sleep(0.25)
        motor3.stop()
        sleep_count = 20
    elif weight_grams > 7.5:
        # dispense chopped nuts
        motor2.set_turning()
        time.sleep(0.5)
        motor2.stop()
        sleep_count = 20

    else:
        sleep_count = sleep_count - 1
        if sleep_count < 0:
            sleep_count = 0
