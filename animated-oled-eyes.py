from machine import Pin, I2C
import time
import math
import random
from ssd1306 import SSD1306_I2C

#Animated eyes - from video at https://youtu.be/h0Yw4KmnUls

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=100000)
oled = SSD1306_I2C(128, 32, i2c)

#oled.text("CIRCLES: 0", 0, 0)
#oled.show()
#time.sleep(10)

#thanks tonygo2 https://www.instructables.com/Drawing-Filled-Circles-and-Triangles-With-MicroPyt/ for the following circle routine
def circle(x,y,r,c):
  oled.hline(x-r,y,r*2,c)
  for i in range(1,r):
    a = int(math.sqrt(r*r-i*i)) # Pythagoras!
    oled.hline(x-a,y+i,a*2,c) # Lower half
    oled.hline(x-a,y-i,a*2,c) # Upper half
  
    
vpos=18
EYE=12
PUPIL=5
TICK=1
EXR =35
EXL = 95
WHITE = 1
BLACK = 0

#circle(35, 18, 12, 1)
#circle(95, 18, 12, 1)


def drawEyes(plh,prh,plv):
    circle(EXR, vpos, EYE, WHITE)
    circle(EXL, vpos, EYE, WHITE)
    circle(EXR+plh, vpos+plv, PUPIL, BLACK)
    circle(EXL+prh, vpos+plv, PUPIL, BLACK)
    
def displayTick():
    oled.show()
    time.sleep(TICK)

def centerDraw():
    drawEyes(1,-1,0)
    
def center():
    centerDraw()
    displayTick()  
    
def left():
    drawEyes(-3,-3,0)
    displayTick()
    
def up():
    drawEyes(1,-1,-3)
    displayTick()
    
def down():
    drawEyes(1,-1,+3)
    displayTick()

def right():
    drawEyes(3,3,0)
    displayTick()
    
def rollEyes():
    center()
    left()
    up()
    right()
    center()
    
def lookLeft():
    left()
    center()

def lookRight():
    right()
    center()

def lookUp():
    up()
    center()

def lookDown():
    down()
    center()
    
center()
while True:
    action=random.randint(0, 20)
    print(action)
    if action==1:
        lookRight()
    if action==2:
        lookUp()
    if action==3:
        lookDown()
    if action==4:
        lookLeft()
    if action==5:
        rollEyes()
    if action==6:
        up()
    if action==7:
        down()
    if action==8:
        left()
    if action==9:
        right()

    


