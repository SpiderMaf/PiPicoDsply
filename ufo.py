import time, random
import picodisplay as display 

# based on initial code demo for the PiMoroni PicoDisplay for the RaspberyPiPico


width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)

display.set_backlight(1.0)

ufogrid = ["000001111100000","000111111111000","001111111111100","011011011010110","111111111111111","001110011011100","000100000001000"]


#Lack of capitalisation on ufo meant that the reset routine didnt work with TypeError: 'ufo' object isn't callable.  
#This was because the main loop through ufos overwrote the class once the game started.  So capital Ufo for the class makes it a different object than ufo
class Ufo:
    def __init__(self, x, y, r, dx, dy, pen):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.pen = pen

def drawufo(x,y,r,ufopen):
        #display.circle(int(x), int(y), int(r))
        x=int(x)
        y=int(y)
        r=2
        row = 0
        col=0
        for line in ufogrid:
            for pixel in line:
                colour = str(pixel)
                if colour != "0":
                    display.set_pen(ufopen)
                    display.rectangle(x+(col*r),y+(row*r),r,r)
                col+=1
            row +=1
            col=0
            
        

class Bat:
    def __init__(self, y):
        self.y = y     
        
class Missile:
    def __init__(self, x, y):
        self.x = y 
        self.y = y  
        self.active = False

# initialise shapes
area51 = []
for i in range(0, 25):
    area51.append(
        Ufo(
            random.randint(0, width),
            random.randint(0, height),
            random.randint(0, 10) + 3,
            random.randint(0, 255) / 128,
            random.randint(0, 255) / 128,
            display.create_pen(0, random.randint(75, 155), 0)  
            
        )
    )
bat = Bat(1)
missile = Missile (width-20,0)
    
while True:
    display.set_pen(0, 0, 0)    
    display.clear()
    
    for ufo in area51:        
        ufo.x += ufo.dx
        ufo.y += ufo.dy
        
        
        if ufo.x < 0 or ufo.x > width:
            ufo.dx *= -1
        if ufo.y < 0 or ufo.y > height:
            ufo.dy *= -1
            
        if missile.active:
            if (ufo.x > missile.x - ufo.r and ufo.x < missile.x + ufo.r) and (ufo.y > missile.y - ufo.r and ufo.y < missile.y + ufo.r):
                missile.active=False
                display.set_pen(255,255,255)
                display.circle(int(ufo.x), int(ufo.y), int(ufo.r)+5)
                ufo.dx =0
                ufo.dy =0
                ufo.x = 500
                ufo.y = 500
        
        
        display.set_pen(ufo.pen)
        drawufo((ufo.x), int(ufo.y), int(ufo.r),ufo.pen)

        

    
    if display.is_pressed(display.BUTTON_Y) and bat.y < height - 25:
        bat.y = bat.y +1
    if display.is_pressed(display.BUTTON_X) and bat.y > 0:
        bat.y = bat.y -1 
        
    display.set_pen(100,100,100)
    display.rectangle(width-10,bat.y,10,20)
    
    if missile.active:
        display.rectangle(missile.x,missile.y, 20,5)
        if missile.x > -10:
            missile.x -= 4
        else:
            missile.active=False
 
    if display.is_pressed(display.BUTTON_A):
        if not missile.active:
            missile.x = width-20
            missile.y = bat.y+10
            missile.active=True 
        
    
    if display.is_pressed(display.BUTTON_B):
        area51 = []
        for i in range(0, 25):
            area51.append(
                Ufo(
                    random.randint(0, width),
                    random.randint(0, height),
                    random.randint(0, 10) + 3,
                    random.randint(0, 255) / 128,
                    random.randint(0, 255) / 128,
                    display.create_pen(0, random.randint(75, 155), 0)  
            
                )
        )
    display.update()
    #display.set_led(0,0,0)
    #time.sleep(0.01)

