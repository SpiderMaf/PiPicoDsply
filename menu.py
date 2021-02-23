import time, random
import picoexplorer as explorer
#  
# This is the file that I saved as main.py to act as the beginnings of a boot menu, which will then call the bird game after a button click
#
width = explorer.get_width()
height = explorer.get_height()

display_buffer = bytearray(width * height * 2)  # 2-bytes per pixel (RGB565)
explorer.init(display_buffer)

#explorer.set_backlight(1.0)
explorer.set_audio_pin(0)

clicked = False;
unclicked = True;

while unclicked:
    explorer.set_pen(0, 0, 0)    
    explorer.clear()



    explorer.set_pen(155, 155, 155)
    explorer.text("Press B to flap the bird", 20, 110, 200)    
    if explorer.is_pressed(explorer.BUTTON_B):
        unclicked = False
 
        
    explorer.update()
    time.sleep(0.01)

explorer.set_pen(0, 0, 0)    
explorer.clear()
explorer.update()
