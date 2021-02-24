from machine import Pin, I2C
import ssd1306

# Oled Driver direct link:  https://raw.githubusercontent.com/RuiSantosdotme/ESP-MicroPython/master/code/Others/OLED/ssd1306.py

i2c = I2C(0, scl=Pin(21), sda=Pin(20))

width = 128
height = 32
display = ssd1306.SSD1306_I2C(width, height, i2c)

display.text('PLEASE SUBSCRIBE', 0, 5)
display.text('SPIDERMAF YOUTUBE', 0, 25)
      
display.show()
