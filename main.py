#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""I2C LCD showcase"""

#from lcd_i2c import LCD
from machine import SoftI2C, Pin
from hcsr04 import HCSR04
from time import sleep
from LCD_Display import LcdApi, I2CLcd
import json as js

# ESP32
#sensor = HCSR04(trigger_pin=2, echo_pin=15, echo_timeout_us=10000)
# ESP8266
sensor = HCSR04(trigger_pin=12, echo_pin=14, echo_timeout_us=10000)

ADDR = 0x27
ROWS = 4
COLS = 20
FREQ = 100000

# define custom I2C interface, default is 'I2C(0)'
i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100000)   # ESP8266
#i2c = I2C(1, scl=Pin(4), sda=Pin(5), freq=100000)   # ESP8266
#i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=100000) # ESP32


devices = i2c.scan()
if len(devices) == 0:
 print("No i2c device !")
else:
 print('i2c devices found:',len(devices))
for device in devices:
 print("At address: ",hex(device))
 
if devices != []:
    lcd = I2CLcd(i2c, devices[0], 4, 20) #For 4 row x 20 column LCDs
    lcd.topdata('Found I2C device: {}'.format(devices[0]))
    sleep(2)

lcd.clear()


config_file = 'hcsr04_config.json'

def read_config():
    f = open(config_file, 'r')
    data = js.loads(f.read())
    f.close()
    return data

def write_config(data):
    f = open(config_file, 'w')
    f.write(js.dumps(data))
    f.close()

def d_calc():
    cnt = 3
    currentd = sensor.distance_cm()
    while cnt > 0:
        sleep(0.01)
        cnt -= 1
        newd = sensor.distance_cm()
        if abs(currentd - newd) > 0.1:
            cnt = 3 
            currentd = newd
            
    #print('Check1 cnt {} and distance_cm {}'.format(cnt, currentd))
    return currentd

def sensor_calibration():
    #config = joy_read_config(joy_file)
    d_ref = sensor.distance_cm()

    cnt = 20    # Loop for 20 times
    skip = 0    # Skip calibrarion in first 5 seconds from power up
    while cnt > 0 and skip < 50:
        skip += 1
        cnt -= 1
        sleep(0.05)
        
        currentd = sensor.distance_cm()
        if abs(currentd - d_ref) > 0.1 :
            d_ref = currentd
            cnt = 20
            
    data = read_config()
    if cnt == 0 and d_ref != data['d_ref']:
        config = {'d_ref': d_ref}
        write_config(config)
        print("Save new calibration: ", config)
        lcd.topdata('Save new calibration: {}'.format(config))
    else:
        print("Skip calibration and use saved value!")
        lcd.topdata('Skip calibration and use saved value!')
    sleep(2)
    
sensor_calibration()
data = read_config()


while True:
    distance = d_calc()
    height = data['d_ref'] - distance
    
    lcd.topdata('DO CHIEU CAO:({:.2f})'.format( distance))
    lcd.feed('Cao: {:.3f} cm'.format(height))
    
    print('Distance: {:.2f}cm  Height: {:.2f}cm'.format( distance, height))
    sleep(0.7)
