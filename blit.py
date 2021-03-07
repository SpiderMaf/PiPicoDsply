#From my video:
#experimenting with the framebuffer_blit

import random
import picodisplay as display
#from micropython import const
import framebuf as buf

# based on initial code demo for the PiMoroni PicoDisplay for the RaspberyPiPico
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)
plane_buf = bytearray(20 * 10 * 2)  # 2-bytes per pixel (RGB565)
planeSprite = buf.FrameBuffer(plane_buf,20,10,buf.RGB565)
screen_buffer = buf.FrameBuffer(display_buffer,width,height,buf.RGB565)

display.set_backlight(1.0)

#colours
brightwhite = display.create_pen(255,255,255)
white =  display.create_pen(155,155,155)   
red     =  display.create_pen(155, 0,0)  
green    =  display.create_pen(0,155,0)
brown      =  display.create_pen(210,105,30)
black  =  display.create_pen(0,0,0)

def drawplane():
    x=0
    y=0
    #draw the plane
    planeSprite.fill_rect(x,y,4,5,red)
    planeSprite.fill_rect(x+2,y+5,18,5,brightwhite)
    planeSprite.fill_rect(x+18,y+5,2,2,black)

def showplane(x,y):
    screen_buffer.blit(planeSprite,x,y)

drawplane()

go = True


while go:
    display.set_pen(black)    
    display.clear()
    #print(red)
    
    print(display_buffer[0])
    print(display_buffer[1])   
    #draw the plane
    showplane(50,50)

        
    display.update()
#    print(dir(framebuf))
#    display_buffer.blit(fbuf,0,0)
    go = False

