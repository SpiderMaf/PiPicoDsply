#Commented code from SpiderMaf's video at https://youtu.be/ZgV_4lQDIc4 

import picoexplorer as display
import time
import math
import framebuf
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)

purple = display.create_pen(255,0,255)
black = display.create_pen(0,0,0)

class Point(object):
    def __init__(self,x,y):
        self.X=x
        self.Y=y
    def __str__(self):
        return "Point(%s,%s)"%(self.X,self.Y)
        
class Triangle(object):
    def __init__(self,p1,p2,p3):
        self.P1=p1
        self.P2=p2
        self.P3=p3
    def __str__(self):
        return "Triangle(%s,%s,%s)"%(self.P1,self.P2,self.P3)
    
    # Not got this part to work yet - Any ideas?
    def draw():
        pointline(P1,P2)
        pointline(P2,P3)
        pointline(P3,P1)
        



# Following four procedures (horiz,vert,box,line) taken from:
# Tony Goodhew 
# https://forums.pimoroni.com/t/pico-micropython-image/15967/22
#
#
def horiz(l,t,r):  # left, top, right
    n = r-l+1        # Horizontal line
    for i in range(n):
        display.pixel(l + i, t )
        

def vert(l,t,b):   # left, top, bottom
    n = b-t+1        # Vertical line
    for i in range(n):
        display.pixel(l, t+i)

def box(l,t,r,b):  # left, top, right, bottom
    horiz(l,t,r)   # Empty rectangle
    horiz(l,b,r)
    vert(l,t,b)
    vert(r,t,b)

def line(x,y,xx,yy): # (x,y) to (xx,yy)
    if x > xx:
        t = x  # Swap co-ordinates if necessary
        x = xx
        xx = t
        t = y
        y = yy
        yy = t
    if xx-x == 0:  # Avoid div by zero if vertical
        vert(x,min(y,yy),max(y,yy))
    else:          # Draw line one dot at a time L to R
        n=xx-x+1
        grad = float((yy-y)/(xx-x))  # Calculate gradient
        for i in range(n):
            y3 = y + int(grad * i)
            display.pixel(x+i,y3)  # One dot at a time
            
#Calls the line procedure above but uses start and end points 
def pointline(p1,p2):
    line(p1.X,p1.Y,p2.X,p2.Y)            

def update():
    display.update()    

# Clears screen to black and sets pen for the rest of the drawing    
display.set_pen(155,155,155)
display.clear()
display.set_pen(purple)

# Now lets play with the built in objects
display.circle(100,100,50)
display.rectangle(0,00,25,25)
display.rectangle(0,0,25,25)
display.pixel_span(0,200,120)
#Use this for vertical line
display.rectangle(120,0,1,25)

#should be diagonal across the screen
line(0,0,240,240)

# Create and print a point
p=Point(200,200)
print(p)
pointline(p,Point(100,50))

# Create and print a triangle
t=Triangle(Point(0,0),Point(120,120),Point(0,240))
print(t)
update()
display.set_pen(155,155,155)
display.clear()
display.set_pen(purple)

# Draw a triangle between the three points
pointline(Point(0,0),Point(120,120))
pointline(Point(120,120),Point(0,240))
pointline(Point(0,240),Point(0,0))

# Didnt show in video but next job is to make a drawTriangle which accepts a triangle object as input.

update()
