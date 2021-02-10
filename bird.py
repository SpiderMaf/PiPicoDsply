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
skyblue = display.create_pen(50,50,115)
black  =  display.create_pen(0,0,0)

birdgrid=["00000011111100000","00001144441510000","00014444415551000","00014444415515100","01111444415515100","15555144415555100","15555514441555100","14555414444111110","01444144441333331","00111222213111110","00001222221333100","00000112222111100","00000001111000000"]

def drawbird(x,y,zoom):
    #draw the bird
    row = 0
    col = 0
    for line in birdgrid:
        #print(line)
        for pixel in line:
            #print(pixel)
            colour = str(pixel)
            if colour != "0":
                if colour == "1":
                    display.set_pen(black)
                if colour == "2":
                    display.set_pen(green)
                if pixel == "3":
                    display.set_pen(brown)
                if pixel == "4":
                    display.set_pen(red)
                if pixel == "5":
                    display.set_pen(white)
                display.rectangle(x+(col*zoom),y+(row*zoom),zoom,zoom)
            col+=1
        row+=1
        col=0
            
class Bird:
    def __init__(self, x,y):
        self.x = x 
        self.y = y
        self.flying = True
        self.crashed = False
        
class Pillar:
    def __init__(self, x,hole):
        self.x = x
        self.holetop=hole
        self.holebottom =hole+75
       
bird = Bird(5,20)
colonade = []
score = 0

# reset
def reset():
    x=0
    for i in range(0,3):
        hole = random.randint(1,height-100)
        colonade.append(
            Pillar(
                x +100,
                hole
                )
            )
        x += int(width/3)

reset()


while bird.flying:
    display.set_pen(skyblue)    
    display.clear()
        
    
    #draw the pillars
    for pillar in colonade:
        display.set_pen(white)
        display.rectangle(pillar.x,0,10,height)
        display.set_pen(skyblue)
        display.rectangle(pillar.x,pillar.holetop,10,75)  
        if not bird.crashed:
            if pillar.x >-10:
                    pillar.x -=1
            else:
                pillar.x=width
                hole = random.randint(1,height-100)
                pillar.holetop=hole
                pillar.holebottom=hole+75
                score += 1
            if pillar.x < 39 and pillar.x>6:
                if bird.y < pillar.holetop or bird.y+28 > pillar.holebottom:
                    bird.crashed=True

    #draw the bird
    drawbird(bird.x,bird.y,2)
    
    display.set_pen(white)
    display.text(str(score),width-70,5,1,5)
    
    #move the bird 
    if not bird.crashed:
        if display.is_pressed(display.BUTTON_A):
            #flap!
            if bird.y > -22:
                bird.y -= 3
        else:
            if bird.y < height-25:
                bird.y += 3
        
    if display.is_pressed(display.BUTTON_B):
        colonade=[]
        reset()
        #Thanks to Stephan who pointed out was easy to get a massive high score 
        # because I had forgotten to reset the score, so to reset it I need to add:
        score = 0
        bird.y=20
        bird.crashed=False
        
    display.update()


