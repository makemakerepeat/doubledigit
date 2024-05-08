import time
from machine import Pin
import ntptime
import network
import steppermotor as stepper
from stepperconfig import *
from netconfig import *

m1 = stepper.StepperMotor("0-2",STEPPER_1_PINS, STEPPER_1_STOP_PIN, STEPPER_1_DIGITS)
m2 = stepper.StepperMotor("0-9",STEPPER_2_PINS, STEPPER_2_STOP_PIN, STEPPER_2_DIGITS)

print("STEPPERS CREATED" )

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(NET_SSID, NET_PWD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def get_time():
    ntptime.settime()


def reset_pos():
    print("STARTING POS 2")
    in_pos = False
    while not in_pos:    
        m1_in_pos = m1.step_if_non_zero()
        m2_in_pos = m2.step_if_non_zero()
        in_pos = m1_in_pos and m2_in_pos
        time.sleep(STEP_DELAY)
    in_pos = False
    print("STARTING POS 1")
    while not in_pos:    
        m1_in_pos = m1.step_if_zero()
        m2_in_pos = m2.step_if_zero()
        in_pos = m1_in_pos and m2_in_pos
        time.sleep(STEP_DELAY)


    m1.set_zero()
    m2.set_zero()

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


do_connect()
get_time()

sec = 0
in_position = False

num = 0

reset_pos_1by1()
print("IN POSITION")

while True:
    p1 = num % 10
    p2 = num // 10

    m1.set_target_digit(p2)
    m2.set_target_digit(p1)

    done = False
    print(p1, p2)
    while not done:
        m1done = m1.step_to_target()
        m2done = m2.step_to_target()

        done = m1done and m2done

        time.sleep(STEP_DELAY)

    time.sleep(1)
    num = (num +1) % 21

    # time.sleep(STEP_DELAY)
    # loc = time.localtime()    
    # if loc[5] != sec:
    #     sec = loc[5]
    #     p1 = sec % 10
    #     p2 = sec // 10
    #     print(p1, p2)

    #     m1.set_target_digit(p2)
    #     m2.set_target_digit(p1)


    # m1.step_to_target()    
    # m2.step_to_target()