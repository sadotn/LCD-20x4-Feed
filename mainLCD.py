import time
from machine import I2C, Pin, UART
from LCD_Display import LcdApi, I2CLcd

"""LCD Section"""
i2c = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000) #GPIO 20 & 21 have no other function but I2C
devices = i2c.scan()
if devices != []:
    lcd = I2CLcd(i2c, devices[0], 4, 20)

lcd.topdata("THIS REMAINS STATIC")
time.sleep(1)
lcd.feed("^ These")
time.sleep(1)
lcd.feed("^^ Lines")
time.sleep(1)
lcd.feed("^^^ Feed")
time.sleep(1)
lcd.feed("^^^^ Up")
time.sleep(1)
lcd.feed("as you add new ones")