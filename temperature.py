# https://youtu.be/l90pn_LpaLc
# Please subscribe to https://www.youtube.com/spidermaf to support my channel

from machine import Pin, I2C
import time
# below from:  https://gist.github.com/futureshocked/287606dd7556a82c90f86473a6cf2ed0
import BME280
from ssd1306 import SSD1306_I2C

led = Pin(25, Pin.OUT)
led.off

i2cbus1=I2C(0,sda=Pin(0), scl=Pin(1))

devices=i2cbus1.scan()
for i in devices:
    print(hex(i))

oled = SSD1306_I2C(128, 32, i2cbus1)

oled.text("Temperature", 0, 0)
oled.show()
count=0;
oled.show()

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
bme = BME280.BME280(i2c=i2cbus1)


def internalTemp():
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    return temperature

while True:
    count+=1
    for i in range(60):
        time.sleep(.98)
        led.toggle()
        time.sleep(.02)
        led.toggle()
        tempstr="Temp: " + str(bme.temperature)
        print("int:"+str(internalTemp()) + tempstr) 
        oled.fill(0)
        oled.text(tempstr, 0, 12)
        oled.show()

  
