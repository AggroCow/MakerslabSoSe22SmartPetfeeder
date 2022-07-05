import time

from Electronic_Components.RESOLUTION import RESOLUTION


class StepperMotor:
    sleep_pin: int = None
    dir_pin: int = None
    step_pin: int = None
    mode_pins: tuple[int, int, int] = None
    resolution: RESOLUTION = None
    pi = None

    def __init__(self, sleep_pin, dir_pin, step_pin, mode_pins, resolution, pi):
        self.sleep_pin = sleep_pin
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.mode_pins = mode_pins
        self.resolution = resolution
        self.pi = pi
        self._write_resolution_to_mode()

    def _write_resolution_to_mode(self):
        for i in range(len(self.mode_pins)):
            self.pi.write(self.mode_pins[i], self.resolution.value[i])

    def set_turning(self, dutycycle: int = 128, frequency: int = 500):
        self.pi.set_PWM_dutycycle(self.step_pin, dutycycle)  # 50% On 50% Off
        self.pi.set_PWM_frequency(self.step_pin, frequency)  # 500 pulses per second
        self.pi.write(self.sleep_pin, 1)  # wake up driver
        self.pi.write(self.dir_pin, 1)  # 1=clockwise ; 0 = counter clockwise

    def stop(self):
        self.pi.write(self.sleep_pin, 0)  # put driver to sleep
        self.pi.set_PWM_dutycycle(self.step_pin, 0)  # pwm off

    def __repr__(self):
        return f'StepperMotor(sleep_pin={self.sleep_pin}, dir_pin={self.dir_pin}, step_pin={self.step_pin}, mode_pins={self.mode_pins}, resolution={self.resolution})'
