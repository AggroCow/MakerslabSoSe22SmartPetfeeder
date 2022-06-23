import time

import pigpio

from Electronic_Components.RESOLUTION import RESOLUTION


class StepperMotor:
    sleepPin: int = None
    dirPin: int = None
    stepPin: int = None
    modePins: tuple[int, int, int] = None
    resolution: RESOLUTION = None
    pi = None

    def __int__(self, sleepPin: int, dirPin: int, stepPin: int, modePins: tuple[int, int, int], resolution: RESOLUTION):
        self.sleepPin = sleepPin
        self.dirPin = dirPin
        self.stepPin = stepPin
        self.modePins = modePins
        self.resolution = resolution
        self.pi = pigpio.pi()
        self._writeResolutionToMode()

    def _writeResolutionToMode(self):
        for i in range(len(self.modePins)):
            self.pi.write(self.modePins[i], self.resolution.value[i])

    def turnMotor(self, revolutions: float, dutycycle: int = 128, frequency: int = 500):
        # Set duty cycle and frequency
        self.pi.set_PWM_dutycycle(self.stepPin, dutycycle)  # 50% On 50% Off
        self.pi.set_PWM_frequency(self.stepPin, frequency)  # 500 pulses per second
        timeSpendTurningInMicroSeconds = 1000
        self.pi.write(self.sleepPin, 1)  # wake up driver
        startTime = time.time()
        while time.time() - 1000 < startTime:
            self.pi.write(self.dirPin, 1)  # 1=clockwise ; 0 = counter clockwise
        self.pi.write(self.sleepPin, 0)  # put driver to sleep
        self.pi.set_PWM_dutycycle(self.stepPin, 0)  # pwm off
