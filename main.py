#! /usr/bin/python2

import time
import sys

from datetime import datetime

from picamera import PiCamera

import pigpio

from Electronic_Components.RESOLUTION import RESOLUTION
from Electronic_Components.StepperMotor import StepperMotor


EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    motor1.stop()
    motor2.stop()
    motor3.stop()
    pi.stop()
        
    print("Bye!")
    sys.exit()

def on_weight(weight_grams):
    global sleep_count
    global motor1
    global motor2
    global motor3
    cooldown = 100
    if weight_grams < -5:
        print('tare because of negative weight')
        hx.tare()
        return
    if sleep_count == cooldown:
        print('tare after cooldown was set')
        hx.tare()
        sleep_count = sleep_count - 1
        return
    if weight_grams > 10:
        # take picture
        now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        camera.capture(f'/home/pi/pics/{now}-{weight_grams:.0f}g.jpg')
    if sleep_count == 0 and weight_grams > 150:
        print(f'heavy bird: {weight_grams}')
        # dispense whole nuts
        motor1.set_turning()
        time.sleep(0.3)
        motor1.stop()
        sleep_count = 100
    elif sleep_count == 0 and weight_grams > 25:
        print(f'medium bird: {weight_grams}')
        # dispense chopped nuts and worms
        motor2.set_turning()
        motor3.set_turning()
        time.sleep(0.3)
        motor2.stop()
        time.sleep(0.3)
        motor3.stop()
        sleep_count = 100
    elif sleep_count == 0 and weight_grams > 10:
        print(f'light bird: {weight_grams}')
        # dispense chopped nuts
        motor2.set_turning()
        time.sleep(0.3)
        motor2.stop()
        sleep_count = 100
    elif sleep_count > 0:
        sleep_count = sleep_count - 1
        if sleep_count < 0:
            sleep_count = 0
    print(f'sleep_count = {sleep_count}')


hx = HX711(17, 27)

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
#hx.tare_A()
#hx.tare_B()

pi = pigpio.pi()
# whole nuts
motor2: StepperMotor = StepperMotor(sleep_pin=10, dir_pin=20, step_pin=21, mode_pins=(14, 15, 18),
                                    resolution=RESOLUTION.QUARTER, pi=pi)
# chopped nuts
motor1: StepperMotor = StepperMotor(sleep_pin=9, dir_pin=23, step_pin=24, mode_pins=(2, 16, 4),
                                    resolution=RESOLUTION.QUARTER, pi=pi)
# worms
motor3: StepperMotor = StepperMotor(sleep_pin=11, dir_pin=19, step_pin=26, mode_pins=(5, 6, 13),
                                    resolution=RESOLUTION.QUARTER, pi=pi)

camera = PiCamera()

sleep_count = 0

while True:

    try:
        # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
        # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
        # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
        
        # np_arr8_string = hx.get_np_arr8_string()
        # binary_string = hx.get_binary_string()
        # print binary_string + " " + np_arr8_string
        
        # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
        val = hx.get_weight(5)

        weight_grams = -val / 225
        on_weight(weight_grams)
        print(f'weight: {weight_grams:.1f}g')

        # To get weight from both channels (if you have load cells hooked up 
        # to both channel A and B), do something like this
        #val_A = hx.get_weight_A(5)
        #val_B = hx.get_weight_B(5)
        #print "A: %s  B: %s" % ( val_A, val_B )

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
