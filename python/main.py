import steppermotor as stepper
from stepperconfig import *
from clocktime import time_init, get_time_number, print_time
import time

m1 = stepper.StepperMotor("0-2",STEPPER_1_PINS, STEPPER_1_STOP_PIN, STEPPER_1_DIGITS)
m2 = stepper.StepperMotor("0-9",STEPPER_2_PINS, STEPPER_2_STOP_PIN, STEPPER_2_DIGITS)

print("STEPPERS CREATED" )

time_init()
print("TIME SET")

def reset_pos_1by1():
    in_pos = False
    print("STARTING POS 1")
    while not in_pos:    
        in_pos = m1.step_if_zero()
        time.sleep(STEP_DELAY)

    in_pos = False
    print("STARTING POS 2")
    while not in_pos:    
        in_pos = m2.step_if_zero()
        time.sleep(STEP_DELAY)

    in_pos = False
    print("STARTING POS 3")
    while not in_pos:    
        in_pos = m1.step_if_non_zero()
        time.sleep(STEP_DELAY)

    in_pos = False
    print("STARTING POS 4")
    while not in_pos:    
        in_pos = m2.step_if_non_zero()
        time.sleep(STEP_DELAY)

    m1.set_zero()
    m2.set_zero()


reset_pos_1by1()
print("IN POSITION")

num = 0
while True:
    time.sleep(STEP_DELAY)
    newnum = get_time_number(MODE)    

    if newnum != num:
        num = newnum
        p1 = num % 10
        p2 = num // 10
        print(p1, p2, time.time())
        print_time()

        m1.set_target_digit(p2)
        m2.set_target_digit(p1)


    m1.step_to_target()    
    m2.step_to_target()