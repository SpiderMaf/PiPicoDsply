# writes the number of minutes elapsed to the internal filesystem and oled every minute.
# displays on oled and pulses led
# When power fails, the last written value is still on the non-volitile flash
# so is shown on the oled at the next boot time but is overwritten after the first 60 seconds approximately of run time
# 
# create empty timer-file file on the flash (save as to rpico in thonny) before first run to provent possible file not found error

# https://www.youtube.com/spidermaf  


from machine import Pin, I2C
import time
from ssd1306 import SSD1306_I2C

led = Pin(25, Pin.OUT)
#OR on Pico W I think you need this to access the LED 
#led =  machine.Pin("LED", machine.Pin.OUT)
led.off

i2c=I2C(0,sda=Pin(0), scl=Pin(1))

oled = SSD1306_I2C(128, 32, i2c)

oled.text("Timer: 0", 0, 0)
oled.show()
count=0;
previous_time = ""
f = open('timer-file')
previous_time = f.read()
previous_time = previous_time.replace("Timer:","Previous time:")
f.close()
oled.text(previous_time, 0, 24)
oled.show()

while True:
    count+=1
    for i in range(60):
        time.sleep(.98)
        led.toggle()
        time.sleep(.02)
        led.toggle()
    
    oled.fill(0)
    timestr="Timer: " + str(count) + "minutes"
    oled.text(timestr, 0, 0)
    oled.text(previous_time, 0, 24)
    oled.show()
    f = open('timer-file', 'w')
    f.write(timestr)
    f.close()
    



