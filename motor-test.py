from Electronic_Components.StepperMotor import StepperMotor
from Electronic_Components.RESOLUTION import RESOLUTION
import time
import pigpio

if __name__ == '__main__':
    pi = pigpio.pi()
    motor1: StepperMotor = StepperMotor(sleep_pin=10, dir_pin=20, step_pin=21, mode_pins=(14, 15, 18),
                                        resolution=RESOLUTION.QUARTER, pi=pi)
    motor2: StepperMotor = StepperMotor(sleep_pin=9, dir_pin=23, step_pin=24, mode_pins=(2, 16, 4),
                                        resolution=RESOLUTION.QUARTER, pi=pi)
    motor3: StepperMotor = StepperMotor(sleep_pin=11, dir_pin=19, step_pin=26, mode_pins=(5, 6, 13),
                                        resolution=RESOLUTION.QUARTER, pi=pi)

    try:
        print("Turn 1")
        motor1.set_turning()
        time.sleep(2)
        motor1.stop()

        print("Turn 2")
        motor2.set_turning()
        time.sleep(2)
        motor2.stop()

        print("Turn 3")
        motor3.set_turning()
        time.sleep(2)
        motor3.stop()

        print("Turn 1 and 2")
        motor1.set_turning()
        motor2.set_turning()
        time.sleep(2)
        motor1.stop()
        motor2.stop()

        print("Turn 2 and 3")
        motor2.set_turning()
        motor3.set_turning()
        time.sleep(2)
        motor2.stop()
        motor3.stop()

        print("Turn 1 and 3")
        motor1.set_turning()
        motor3.set_turning()
        time.sleep(2)
        motor1.stop()
        motor3.stop()

        print("Turn 1 and 2 and 3")
        motor1.set_turning()
        motor2.set_turning()
        motor3.set_turning()
        time.sleep(2)
        motor1.stop()
        motor2.stop()
        motor3.stop()
    finally:
        print('Exiting')
        motor1.stop()
        motor2.stop()
        motor3.stop()
        pi.stop()
