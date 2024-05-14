import steppermotor as stepper
import time

from clocktime import time_init, get_time_number, print_time, get_time_number_test
from config import CLOCK_MODE
from constants import *
from pinconfig import *


STEPPER_1_DIGITS = CLOCK_012345_DIGITS
if CLOCK_MODE == CLOCK_SHOW_HOURS:
    STEPPER_1_DIGITS = CLOCK_012_DIGITS
STEPPER_2_DIGITS = CLOCK_0123456789_DIGITS

STEP_DELAY = 0.003

m1 = stepper.StepperMotor("0-2",STEPPER_1_PINS, STEPPER_1_STOP_PIN, STEPPER_1_DIGITS)
m2 = stepper.StepperMotor("0-9",STEPPER_2_PINS, STEPPER_2_STOP_PIN, STEPPER_2_DIGITS)

print("STEPPERS CREATED" )

time_init()
print("TIME SET")

def reset_pos_1by1():
    m1.reset(STEP_DELAY)
    m2.reset(STEP_DELAY)

reset_pos_1by1()
print("IN POSITION")

num = 0
while True:
    time.sleep(STEP_DELAY)
    newnum = get_time_number_test(CLOCK_MODE)

    if newnum != num:
        num = newnum
        p2 = num % 10
        p1 = num // 10
        print(num, p1, p2)

        m1.set_target_digit(p1)
        m2.set_target_digit(p2)


    m1.step_to_target()    
    m2.step_to_target()