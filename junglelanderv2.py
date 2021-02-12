import random
import picodisplay as display 

# based on initial code demo for the PiMoroni PicoDisplay for the RaspberyPiPico
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)

display.set_backlight(1.0)

#colours
brightwhite = display.create_pen(255,255,255)
white =  display.create_pen(155,155,155)   
red     =  display.create_pen(155, 0,0)  
green    =  display.create_pen(0,155,0)
brown      =  display.create_pen(210,105,30)
black  =  display.create_pen(0,0,0)

def drawplane(x,y):
    #draw the plane
    display.set_pen(red)
    display.rectangle(x,y,4,5)
    display.set_pen(white)
    display.rectangle(x+2,y+5,18,5)
    display.set_pen(black)
    display.rectangle(x+18,y+5,2,2)


def drawtree(x,h):
    #draw the trees
    x=x*10
    h=h*10
    display.set_pen(brown)
    display.rectangle(x+3,height-h,4,h)
    display.set_pen(green)
    display.rectangle(x,height-h,10,10)
    

class Tree:
    def __init__(self, x, treeheight):
        self.x = x
        self.treeheight=treeheight
        
class Plane:
    def __init__(self, x,y):
        self.x = x 
        self.y = y
        self.flying = True
        self.crashed = False
        
class Missile:
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.active = False

plane = Plane(0,0)
missile = Missile(0,0)
jungle = []
a_pressed = False
b_pressed = False

# reset
def plantjungle():
    #plant the trees
    x=0
    for i in range(0,25):
        jungle.append(
            Tree(
                x,
                random.randint(1,10)
                )
        )
        x += 1

plantjungle()

while plane.flying:
    display.set_pen(black)    
    display.clear()
    
    for tree in jungle:        
        drawtree(tree.x,tree.treeheight)
        
        if missile.active:
            if missile.x >= tree.x *10 and missile.x <= ((tree.x+1)*10)-1:
                if missile.y >=  height - tree.treeheight*10:
                    missile.active=False
                    tree.treeheight -= 5
                    display.set_pen(brightwhite)
                    display.circle(missile.x,missile.y,10)
        
        if plane.x +20 == tree.x * 10 and plane.y +10 == height-(tree.treeheight *10):
            plane.crashed = True
            display.set_pen(brightwhite)
            display.circle(plane.x+10,plane.y+5,10)
        
    #draw the plane
    drawplane(plane.x,plane.y)
   
    #move the plane   
    if not plane.crashed:
        if plane.x < width:
            plane.x += 1            
        else:
            if plane.y < height -10:
                plane.y += 5
                plane.x = 0
            else:
                plane.flying = False
    
    if missile.active:
        display.set_pen(brightwhite)
        display.rectangle(missile.x,missile.y,5,5)
        if missile.y < height:
            missile.y +=3
        else:
            missile.active=False
 
    if display.is_pressed(display.BUTTON_A):
        if not a_pressed :
            a_pressed =True
            if not missile.active and not plane.crashed:
                #fire missile
                missile.active=True
                missile.x = plane.x+5
                missile.y = plane.y+10
    else:
        a_pressed = False
            
    
    if display.is_pressed(display.BUTTON_B):
        if not b_pressed:
            b_pressed=True
            jungle = []
            plane = Plane(0,0)
            plantjungle()
    else:
        b_pressed=False
        
    display.update()

