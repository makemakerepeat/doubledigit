import ntptime
import network
from netconfig import *
import time

SECONDS_PER_HOUR = 60*60

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
    seconds_offset = int(TIME_OFFSET * SECONDS_PER_HOUR)
    return time.gmtime(seconds + seconds_offset)

def get_time_number(num):
    tm = get_local_time()
    return tm[num]

def print_time():
    tm = get_local_time()
    print(tm)