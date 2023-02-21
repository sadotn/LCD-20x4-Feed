import time
from machine import I2C, Pin
from I2C_LCD import I2CLcd                                            

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000) # 8574AT chip = 0x3F address
devices = i2c.scan()
lcd = I2CLcd(i2c, devices[0], 4, 20)              # Assumes only LCD is connected

lcddata=["","Welcome              ","to                  ","Pico                "]

def lcdfeed(new):
    try:
        if devices != []:self.lcddata.append(new)
            self.lcddata.pop(0)
            for x in range(0,3)
                self.lcd.move_to(0, x)
                self.lcd.putstr(lcddata[x])
    else:
        print("No device found")
    except:
        pass
