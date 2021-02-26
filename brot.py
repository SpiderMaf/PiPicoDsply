import picoexplorer as display 

# based on initial code demo for the PiMoroni PicoDisplay for the RaspberyPiPico


width = display.get_width()
height = display.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)

#Removed as this was removed so errors in newer picoexplorer versions
#display.set_backlight(1.0)


iterations = 80

def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < iterations:
        z = z*z + c
        n += 1
    return n
#Change the zoom below to zoom in - the smaller the number the greater the zoom.  
#Zoom too much on the wrong part may give no visible part of the fractal on the display
#the smaller the zoom amount the longer the picture may take to generate.
zoom = 1
# Plot window
RealStart = -2 * zoom
RealEnd= 1 * zoom
ImaginaryStart = -1 *zoom
ImaginaryEnd = 1 *zoom

palette = []
display.clear()
#One of the issues on the video was it was displaying the old images whilst generating the new one
#So added the update below to send a clear screen to the display
display.update()
go = True

while go:
    for x in range(0, width):
        for y in range(0, height):
            c = complex(RealStart + (x / width) * (RealEnd - RealStart),ImaginaryStart + (y / height) * (ImaginaryEnd - ImaginaryStart))
            m = mandelbrot(c)
            colour = 255 - int(m * 255 / iterations)
            display.set_pen(colour,0,155)
            display.pixel(x, y)
        #uncomment this line if you want to see the progress the plot has made if you are not updating the screen every x    
        #print(x)
        #if you put the display update here it will update every x line
        display.update()
    #if you put the display update here it will update at the end of processing (maybe 2 to 3 minutes in)
    #display.update()    
    go = False
        


