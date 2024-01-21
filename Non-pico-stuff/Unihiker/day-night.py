from unihiker import GUI  # Import the GUI module from the UniHiker library
import time  # Import the time library
from pinpong.board import Board, Pin, NeoPixel
Board().begin()

gui = GUI()  # Instantiate the GUI class and create an object

colors=[(0,0,0),(98,90,70),(95, 40, 0),(88, 57, 30),(100, 97, 100),(100, 100, 100),(100, 100, 97),(97,85,56),(20,40,78),(0,30,70),(10,10,70)]
currentcolor=0
futurecolor=currentcolor+1
colornames=['black','dawnone','dawntwo','dawnthree','carbonarc','sun','noon','duskone','dusktwo','blueone','bluetwo']


maxcolors=11
tick=0.1
timer=0
maxwait=50
maxfade=20
mode='wait'


ledring=NeoPixel(Pin((Pin.P21)),12)
ledring.brightness(100)
for lednumber in range(0,12):
    ledring[lednumber] = (255,0,0)
    time.sleep(0.05)
for lednumber in range(0,12):
    ledring[lednumber] = (0, 255,0)
    time.sleep(0.05)
for lednumber in range(0,12):
    ledring[lednumber] = (0,0,255)
    time.sleep(0.05)
for lednumber in range(0,12):
        ledring[lednumber] = (0,0,0)
        time.sleep(tick) 

gui.add_button(x=60, y=30, w=100, h=30, text=colornames[0], origin='center', onclick=lambda: clicked(0), state="enabled")
gui.add_button(x=60, y=80, w=100, h=30, text=colornames[1], origin='center', onclick=lambda: clicked(1), state="enabled")
gui.add_button(x=60, y=130, w=100, h=30, text=colornames[2], origin='center', onclick=lambda: clicked(2), state="enabled")
gui.add_button(x=60, y=180, w=100, h=30, text=colornames[3], origin='center', onclick=lambda: clicked(3), state="enabled")
gui.add_button(x=60, y=230, w=100, h=30, text=colornames[4], origin='center', onclick=lambda: clicked(4), state="enabled")
gui.add_button(x=60, y=280, w=100, h=30, text=colornames[5], origin='center', onclick=lambda: clicked(5), state="enabled")
gui.add_button(x=180, y=30, w=100, h=30, text=colornames[6], origin='center', onclick=lambda: clicked(6), state="enabled")
gui.add_button(x=180, y=80, w=100, h=30, text=colornames[7], origin='center', onclick=lambda: clicked(7), state="enabled")
gui.add_button(x=180, y=130, w=100, h=30, text=colornames[8], origin='center', onclick=lambda: clicked(8), state="enabled")
gui.add_button(x=180, y=180, w=100, h=30, text=colornames[9], origin='center', onclick=lambda: clicked(9), state="enabled")
gui.add_button(x=180, y=230, w=100, h=30, text=colornames[10], origin='center', onclick=lambda: clicked(10), state="enabled")


time.sleep(1)
for lednumber in range(0,12):
        ledring[lednumber] = colors[currentcolor]


def clicked(col):
    global futurecolor,currentcolor,timer,mode
    print('clicked',col, colornames[col]) 
    print('changed to', colornames[col])
    currentcolor=col
    futurecolor=col
    for lednumber in range(0,12):
        ledring[lednumber] = colors[currentcolor]
    timer=0
    mode='wait'




while True:  # Loop indefinitely
    if mode=='wait':
        if timer==0:
            print ('holding at:', colornames[currentcolor])
        time.sleep(tick)
        timer+=1

        if timer>=maxwait:
            timer=0
            mode='change'  

    if mode=='change':   
        time.sleep(tick * 10) 
        if timer==0:
            cred=colors[currentcolor][0]
            cgrn=colors[currentcolor][1]
            cblu=colors[currentcolor][2]
            fred=colors[futurecolor][0]
            fgrn=colors[futurecolor][1]
            fblu=colors[futurecolor][2]
            dred=(fred-cred)/maxfade
            dgrn=(fgrn-cgrn)/maxfade
            dblu=(fblu-cblu)/maxfade

            print (cred,cgrn,cblu)
            print (fred,fgrn,fblu)
            print (dred,dgrn,dblu)
            print ('fadingto:', colornames[futurecolor])
            print ('=====')
        for lednumber in range(0,12):
                ledring[lednumber] = (cred,cgrn,cblu)
        cred=int(cred+dred)
        cgrn=int(cgrn+dgrn)
        cblu=int(cblu+dblu) 
        if cblu>255:
            cblu=255
        if cblu<0:
            cblu=0

        if colornames[currentcolor]=='dawnone':
            print ('timer:',timer,'rgb:' ,cred,cgrn,cblu)

        timer+=1
        if timer >= maxfade:
            currentcolor=futurecolor
            for lednumber in range(0,12):
                ledring[lednumber] = colors[currentcolor]
            futurecolor+=1
            if futurecolor >= maxcolors:
                futurecolor = 0
            timer=0
            
            mode='wait'
