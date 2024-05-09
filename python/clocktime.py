import ntptime
import network
import time

from config import *
from constants import *

SECONDS_OFFSET = int(TIMEZONE_OFFSET_HOURS * SECONDS_PER_HOUR)

TEST_MODE_OFFSET = 0
TEST_MODE_FACTOR = 60
if CLOCK_MODE == CLOCK_SHOW_HOURS:
    if CLOCK_12_HOUR:
        TEST_MODE_FACTOR = 12
        TEST_MODE_OFFSET = 1
    else:
        TEST_MODE_FACTOR = 24

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(NET_SSID, NET_PWD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def time_init():
    do_connect()
    ntptime.settime()

def get_local_time():
    seconds = time.time()
    return time.gmtime(seconds + SECONDS_OFFSET)

def get_time_number_test(mode, slowdown = 5):
    seconds = int(time.time() // slowdown)
    return seconds % TEST_MODE_FACTOR + TEST_MODE_OFFSET

def get_time_number(mode):
    tm = get_local_time()
    result = tm[mode]

    if CLOCK_MODE == CLOCK_SHOW_HOURS and CLOCK_12_HOUR:
        result = result % 12

    return result

def print_time():
    tm = get_local_time()
    print(tm)