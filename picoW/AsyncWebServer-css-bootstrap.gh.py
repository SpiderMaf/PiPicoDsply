# This code based on original code from Raspberry Pi
# Connecting to the internet with pico w doc
#

# Please see explanation on my youtube at:
# https://www.youtube.com/watch?v=O69cvP3Z-CA

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
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Pico W</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    </head>
    <body>
    <div class="container px-4 p-3 text-center border text-bg-light">
    <h1>SpiderMaf's Pico W</h1>
        <p>%s</p>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
    </div>
    </body>
</html>
"""

webdocs="/webroot/"

cssstring = """body {background-color:black;}
h1 {color:coral;}
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
    css = request.find('.css')
    print( 'led on = ' + str(led_on))
    print( 'led off = ' + str(led_off))
    
    
    stateis = ""
    if led_on == 6:
        print("led on")
        rightgo.value(1)
        leftgo.value(0)
        stateis = "Traffic can move from right <a class=""btn btn-primary"" role=""button"" href=""/light/off"">CHANGE DIRECTION</a> "
    
    if led_off == 6:
        print("led off")
        rightgo.value(0)
        leftgo.value(1)
        stateis = "Traffic can move from left  <a class=""btn btn-primary"" role=""button"" href=""/light/on"">CHANGE DIRECTION</a> "
    
    if ((led_off == -1) & (led_on == -1)):
        stateis = """<a class="btn btn-success" role="button" href="/light/on">Move traffic from left</a> <br><br> <a class="btn btn-danger" role="button" href="/light/off">Move traffic from right</a>""" 
    
    
    response = html % stateis
    
    if css > 0:
        #b'GET /stylefile.css HTTP/1.1\r\n'
        
        requestedfile  = request[6:css+4]
        print("CSS requested:" + requestedfile)
        f = open(webdocs + requestedfile)
        response = f.read()
        f.close()
        
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text/css\r\n\r\n')
        writer.write(response)
    else:
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



