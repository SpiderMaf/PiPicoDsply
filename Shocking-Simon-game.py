import time, random
import picoexplorer as exp
from machine import Pin



width = exp.get_width()
height = exp.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
exp.init(display_buffer)

#exp.set_backlight(1.0)
exp.set_audio_pin(0)

green =  exp.create_pen(0,155,0)
red  = exp.create_pen(155,0,0)
blue = exp.create_pen(0,0,155)
yellow = exp.create_pen(155,155,0)
lit_green =  exp.create_pen(0,255,0)
lit_red  = exp.create_pen(255,0,0)
lit_blue = exp.create_pen(0,0,255)
lit_yellow = exp.create_pen(255,255,0)
white = exp.create_pen(200,200,200)
black = 0

buttons=["A","B","Y","X"]
half_width = width//2
half_height = height//2
leda = Pin(4, Pin.OUT)
ledy = Pin(3, Pin.OUT)
ledx = Pin(2, Pin.OUT)
ledb = Pin(5, Pin.OUT)
wrong = Pin(7, Pin.OUT)

def block(letter,x,y,colour):
    exp.set_pen(colour)
    exp.rectangle(x,y,half_width,half_height)
    exp.set_pen(black)
    exp.text(letter,x+50, y+50,4)
    
def blockA(active):
    if active:
        block("A",0,0,lit_green)
        leda.on()
    else:
        block("A",0,0,green)
        leda.off()

        
def blockX(active):
    if active:
        block("X",half_height,0,lit_red)
        ledx.on()
    else:
        block("X",half_height,0,red)
        ledx.off()
        
def blockB(active):
    if active:
        block("B",0,half_width,lit_yellow)
        ledb.on()

    else:
        block("B",0,half_width,yellow)
        ledb.off()

        
def blockY(active):
    if active:
        block("Y",half_height,half_width,lit_blue)
        ledy.on()
    else:
        block("Y",half_height,half_width,blue)
        ledy.off()

def all(active):
    blockA(active)
    blockB(active)
    blockX(active)
    blockY(active)
    
def say(string):
    x=half_width//2
    y=height//3
    h=half_width
    w=height//3
    exp.set_pen(black)
    exp.rectangle(x,y,h,w)
    exp.set_pen(white)
    exp.text(string,x+10,y+10,15)
    exp.update()
    
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
        exp.set_tone(tone)
        
def shhh():
    exp.set_tone(-1)
    
def anykey():
    key=""
    if exp.is_pressed(exp.BUTTON_A):
        while exp.is_pressed(exp.BUTTON_A):
            pass
        key="A"
    if exp.is_pressed(exp.BUTTON_B):
        while exp.is_pressed(exp.BUTTON_B):
            pass
        key="B"
    if exp.is_pressed(exp.BUTTON_X):
        while exp.is_pressed(exp.BUTTON_X):
            pass
        key="X"
    if exp.is_pressed(exp.BUTTON_Y):
        while exp.is_pressed(exp.BUTTON_Y):
            pass
        key="Y"
    return key

def attract():
    i=1
    all(False)
    attracting=True
    while attracting:
        lightup(i,False)
        if i==4:
            i=0
        i += 1
        say("Simon Press A Key")
        wait=100
        while wait>0:
            time.sleep(0.01)
            wait=wait-1
            press=anykey()
            if press!="":
                wait=0
                attracting=False 
        all(False)

def game():
    all(False)
    say("Simon Says")
    playing = True
    difficulty = 1
    colours=[]
    while playing:
        for i in range(0,difficulty):
            colours.append(random.randint(1,4))
            shhh()
            time.sleep(1)
            lightup(colours[i],True)
            say("Simon Says")
            time.sleep(1)
            shhh()
            all(False)
            say("Simon Says")
        say("Your turn")
        i=0
        while i < difficulty:
            button=""
            while button=="":
                button=anykey()
            if button==buttons[colours[i]-1]:
                lightup(colours[i],True)
                say("Your Turn")
                i+=1
            else:
                exp.set_tone(150)
                wrong.off()
                say("Wrong!")
                playing=False
                i=difficulty+1
            time.sleep(1)
            all(False)
            wrong.on()
            say("Your turn")
            shhh()
        if playing:
            difficulty=difficulty+1
                

exp.set_pen(black)
exp.clear()
exp.update()

all(False)
exp.update()

while True:
    attract()
    game()
