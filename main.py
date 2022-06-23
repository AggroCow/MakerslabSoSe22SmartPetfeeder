# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Electronic_Components.StepperMotor import StepperMotor
from Electronic_Components.RESOLUTION import RESOLUTION


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    motorOne: StepperMotor = StepperMotor
    #motorOne: StepperMotor = StepperMotor(sleepPin=10, dirPin=20, stepPin=21, modePins=(14, 15, 18), resolution=RESOLUTION.QUARTER)
    #motorTwo: StepperMotor = StepperMotor(sleepPin=9, dirPin=23, stepPin=24, modePins=(2,3,4),resolution= RESOLUTION.QUARTER)
    #motorThree: StepperMotor = StepperMotor(sleepPin=11, dirPin=19, stepPin=26, modePins=(5,6,13),resolution= RESOLUTION.QUARTER)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
