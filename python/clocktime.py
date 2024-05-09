import ntptime
import network
import time

from config import TIMEZONE_OFFSET_HOURS, NET_PWD, NET_SSID
from constants import SECONDS_PER_HOUR

SECONDS_OFFSET = int(TIMEZONE_OFFSET_HOURS * SECONDS_PER_HOUR)

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

def get_time_number(num):
    tm = get_local_time()
    return tm[num]

def print_time():
    tm = get_local_time()
    print(tm)