import time, random
import picodisplay as display 

# based on initial code demo for the PiMoroni PicoDisplay for the RaspberyPiPico


width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)

display.set_backlight(1.0)


class Ball:
    def __init__(self, x, y, r, dx, dy, pen):
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy
        self.pen = pen
        
class Bat:
    def __init__(self, y):
        self.y = y       

# initialise shapes
balls = []
for i in range(0, 50):
    balls.append(
        Ball(
            random.randint(0, width),
            random.randint(0, height),
            random.randint(0, 10) + 3,
            random.randint(0, 255) / 128,
            random.randint(0, 255) / 128,
            display.create_pen(0, 0, 155)  
            
        )
    )
bat = Bat(1)
    
while True:
    display.set_pen(0, 0, 0)    
    display.clear()
    
    for ball in balls:        
        ball.x += ball.dx
        ball.y += ball.dy
        
        if ball.x <= 0:
           if ball.y > bat.y + 25  or ball.y < bat.y: 
                #display.set_led(255,0,0)
                ball.dx =0
                ball.dy =0
                ball.x = 500
                ball.y = 500
        
        if ball.x < 0 or ball.x > width:
            ball.dx *= -1
        if ball.y < 0 or ball.y > height:
            ball.dy *= -1
            
        display.set_pen(ball.pen)
        display.circle(int(ball.x), int(ball.y), int(ball.r))
        
    if display.is_pressed(display.BUTTON_Y) and bat.y < height - 25:
        bat.y = bat.y +1
    if display.is_pressed(display.BUTTON_X) and bat.y > 0:
        bat.y = bat.y -1 
        
    display.set_pen(100,100,100)
    display.rectangle(0,bat.y,10,25)
    
    
    if display.is_pressed(display.BUTTON_B):
        display.set_led(0,0,0)
    display.update()

