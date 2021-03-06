import time, random
import picodisplay as display 
import framebuf as buf

# based on initial code demo for the PiMoroni PicoDisplay for the RaspberyPiPico


width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)
screen_buffer = buf.FrameBuffer(display_buffer,width,height,buf.RGB565)

ufo_array = bytearray(30 * 15 * 2)  # 2-bytes per pixel (RGB565)
ufoSprite = buf.FrameBuffer(ufo_array,30,15,buf.RGB565)


display.set_backlight(1.0)

ufogrid = ["000001111100000","000111111111000","001111111111100","011011011010110","111111111111111","001110011011100","000100000001000"]
green    =  display.create_pen(0,155,0)

class Ufo:
    def __init__(self, x, y, r, dx, dy, pen):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.pen = pen

def makeufo():
        x=0
        y=0
        r=2
        row = 0
        col=0
        for line in ufogrid:
            for pixel in line:
                colour = str(pixel)
                if colour != "0":
                    ufoSprite.fill_rect(x+(col*r),y+(row*r),r,r,green)
                col+=1
            row +=1
            col=0

def drawufo(x,y):
    screen_buffer.blit(ufoSprite,x,y,0) 

class Bat:
    def __init__(self, y):
        self.y = y     
        
class Missile:
    def __init__(self, x, y):
        self.x = y 
        self.y = y  
        self.active = False

def addAliens():
    for i in range(0, 25):
        area51.append(
            Ufo(
                random.randint(0, width),
                random.randint(0, height),
                2,
                random.randint(0, 255) / 128,
                random.randint(0, 255) / 128,
                display.create_pen(0, random.randint(75, 155), 0)     
            )
        )
        
# initialise shapes
makeufo()
area51 = []
addAliens()
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

        drawufo(int(ufo.x), int(ufo.y)) 

    
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
        addAliens()
        
    display.update()
    #display.set_led(0,0,0)
    #time.sleep(0.01)
