import picoexplorer as display
import time
import math
import random
import framebuf
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)

purple = display.create_pen(255,0,255)
black = display.create_pen(0,0,0)

class Point:
    def __init__(self,x,y):
        self.X=x
        self.Y=y
    def __str__(self):
        return "Point(%s,%s)"%(self.X,self.Y)
        
class Triangle:
    def __init__(self,p1,p2,p3):
        self.P1=p1
        self.P2=p2
        self.P3=p3

    def __str__(self):
        return "Triangle(%s,%s,%s)"%(self.P1,self.P2,self.P3)
    
    def draw(self):
        print("I should draw now")
        self.fillTri()
    #filled triangle routines ported From http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html      
    def sortVerticesAscendingByY(self):    
        if self.P1.Y > self.P2.Y:
            vTmp = self.P1
            self.P1 = self.P2
            self.P2 = vTmp
        
        if self.P1.Y > self.P3.Y:
            vTmp = self.P1
            self.P1 = self.P3
            self.P3 = vTmp

        if self.P2.Y > self.P3.Y:
            vTmp = self.P2
            self.P2 = self.P3
            self.P3 = vTmp
        

    def fillTri(self):
        #filled triangle routines ported From http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html 
        self.sortVerticesAscendingByY()
        if self.P2.Y == self.P3.Y:
            fillBottomFlatTriangle(self.P1, self.P2, self.P3)
        else:
            if self.P1.Y == self.P2.Y:
                fillTopFlatTriangle(self.P1, self.P2, self.P3)
            else:
                newx = int(self.P1.X + (float(self.P2.Y - self.P1.Y) / float(self.P3.Y - self.P1.Y)) * (self.P3.X - self.P1.X))
                newy = self.P2.Y                
                pTmp = Point( newx,newy )
                fillBottomFlatTriangle(self.P1, self.P2, pTmp)
                fillTopFlatTriangle(self.P2, pTmp, self.P3)

def fillBottomFlatTriangle(p1,p2,p3):
    #filled triangle routines ported From http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html 
    slope1 = float(p2.X - p1.X) / float (p2.Y - p1.Y)
    slope2 = float(p3.X - p1.X) / float (p3.Y - p1.Y)

    x1 = p1.X
    x2 = p1.X + 0.5
    for scanlineY in range(p1.Y,p2.Y):
        display.pixel_span(int(x1), scanlineY, int(x2)-int(x1))
        x1 += slope1
        x2 += slope2


def fillTopFlatTriangle(p1,p2,p3):
    #filled triangle routines ported From http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html 
    slope1 = float(p3.X - p1.X) / float(p3.Y - p1.Y)
    slope2 = float(p3.X - p2.X) / float(p3.Y - p2.Y)

    x1 = p3.X
    x2 = p3.X + 0.5

    for scanlineY in range (p3.Y,p1.Y-1,-1):
        display.pixel_span(int(x1), scanlineY, int(x2)-int(x1))
        x1 -= slope1
        x2 -= slope2

        
display.set_pen(0,0,0)
display.clear()
display.set_pen(purple)

t=Triangle(Point(30,60),Point(0,110),Point(120,200))
fillBottomFlatTriangle(Point(60,0),Point(0,110),Point(110,110))

fillTopFlatTriangle(Point(0,120),Point(110,120),Point(110,240))

display.update()

display.set_pen(0,0,0)
display.clear()
display.set_pen(purple)
t.fillTri()


display.update()
print(t)
