import time, random
import picoexplorer as explorer
from machine import Pin

width = explorer.get_width()
height = explorer.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
explorer.init(display_buffer)

#explorer.set_backlight(1.0)
explorer.set_audio_pin(0)

green =  explorer.create_pen(0,155,0)
red  = explorer.create_pen(155,0,0)
blue = explorer.create_pen(0,0,155)
yellow = explorer.create_pen(155,155,0)
lit_green =  explorer.create_pen(0,255,0)
lit_red  = explorer.create_pen(255,0,0)
lit_blue = explorer.create_pen(0,0,255)
lit_yellow = explorer.create_pen(255,255,0)
white = explorer.create_pen(200,200,200)
black = 0

buttons=["A","B","Y","X"]
half_width = int(width/2)
half_height = int(height/2)

def block(letter,x,y,colour):
    explorer.set_pen(colour)
    explorer.rectangle(x,y,half_width,half_height)
    explorer.set_pen(black)
    explorer.text(letter,x+50, y+50,4)
    
def blockA(active):
    if active:
        block("A",0,0,lit_green)
    else:
        block("A",0,0,green)
        
def blockX(active):
    if active:
        block("X",half_height,0,lit_red)
    else:
        block("X",half_height,0,red)
        
def blockB(active):
    if active:
        block("B",0,half_width,lit_yellow)
    else:
        block("B",0,half_width,yellow)
        
def blockY(active):
    if active:
        block("Y",half_height,half_width,lit_blue)
    else:
        block("Y",half_height,half_width,blue)

def all(active):
    blockA(active)
    blockB(active)
    blockX(active)
    blockY(active)
    
def say(string):
    x=int(half_width/2)
    y=int(height/3)
    h=half_width
    w=int(height/3)
    explorer.set_pen(black)
    explorer.rectangle(x,y,h,w)
    explorer.set_pen(white)
    explorer.text(string,x+10,y+10,15)
    explorer.update()
    
def lightup(block,sound):
    if block==1:
        blockA(True)
        tone=600
    if block==2:
        blockB(True)
        tone=700
    if block==3:
        blockY(True)
        tone=800
    if block==4:
        blockX(True)
        tone=900
    if sound:
        explorer.set_tone(tone)
        
def shhh():
    explorer.set_tone(20000)
    
def anykey():
    pressed=False
    if explorer.is_pressed(explorer.BUTTON_A):
        pressed=True
    if explorer.is_pressed(explorer.BUTTON_Y):
        pressed=True
    return pressed

def attract():
    i=1
    all(False)
    attracting=True
    while attracting:
        lightup(i,False)
        if i==4:
            i=0
        i=i+1
        say("Simon Press A Key")
        wait=100
        while wait>0:
            time.sleep(0.01)
            wait=wait-1
            if anykey():
                wait=0
                attracting=False 
        all(False)

explorer.set_pen(black)
explorer.clear()
explorer.update()

all(False)
explorer.update()

attract()

