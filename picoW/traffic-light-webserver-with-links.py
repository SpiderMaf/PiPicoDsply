# This code based on original code from Raspberry Pi
# Connecting to the internet with pico w doc
#

# Please see explanation on my youtube at:
# https://www.youtube.com/watch?v=H8RL_Ul1BBE

import network
import socket
import time

from machine import Pin
import uasyncio as asyncio

rightgo = Pin(15, Pin.OUT)
leftgo = Pin(14, Pin.OUT)
onboard = Pin("LED", Pin.OUT, value=0)

ssid = "Wifiname"
password = "yourpassword"

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title>
    </head>
    <body> <h1>SpiderMaf's Pico W</h1>
        <p>%s</p>        
    </body>
</html>
"""

wlan = network.WLAN(network.STA_IF)

def connect_to_network():
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power-save mode
    wlan.connect(ssid, password)
    
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1

        print('waiting for connection...')
        time.sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()

        print('ip = ' + status[0])


async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    
    request = str(request_line)
    led_on = request.find('/light/on')
    led_off = request.find('/light/off')
    print( 'led on = ' + str(led_on))
    print( 'led off = ' + str(led_off)) 
    
    stateis = ""
    if led_on == 6:
        print("led on")
        rightgo.value(1)
        leftgo.value(0)
        stateis = "Traffic can move from right <a href=""/light/off"">CHANGE DIRECTION</a> "
    
    if led_off == 6:
        print("led off")
        rightgo.value(0)
        leftgo.value(1)
        stateis = "Traffic can move from left  <a href=""/light/on"">CHANGE DIRECTION</a> "
    
    if ((led_off == -1) & (led_on == -1)):
        stateis = """<a href="/light/on">Move traffic from left</a> <br><br> <a href="/light/off">Move traffic from right</a>""" 
        
    response = html % stateis
    
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")
    
async def main():
    print('Connecting to Network...')
    connect_to_network()
    
    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
        onboard.on()
        print("heartbeat")
        await asyncio.sleep(0.25)
        onboard.off()
        await asyncio.sleep(5)
        
try:
    asyncio.run(main())
finally:
    syncio.new_event_loop()

