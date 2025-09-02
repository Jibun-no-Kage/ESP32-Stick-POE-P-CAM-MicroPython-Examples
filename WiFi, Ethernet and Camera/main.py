#!micropython
# -*- coding: UTF-8 -*-
# vim:fileencoding=UTF-8:ts=4

#--------------------------------------------------------------------------------
# Known Issue(s)...
#
#   Hard or soft reset of board required to force Ethernet interface to do 
#   a complete initialize.  LAN module does not apparently release the CS
#   resource in a correct manner, this in turn breaks the SPI deinitialize
#   routine.  And MicroPython LAN interface does not support a disconnect
#   routine.
#
#--------------------------------------------------------------------------------

from machine import Pin, Timer, SPI
from sys import print_exception

_RELEASE_ = '08/31/2025'
_TITLE_ = 'Wireless And Wired Camera Stream Example'
_VERSION_ = '1.0.3'
_AUTHOR_ = 'Jibun no Kage'

# Constants...
ZERO = const(0)
ONE = const(1)
TWO = const(2)

BUFFER = const(1024)
PORT = const(80)

RETURN = '\r\n'
SPACE = ' '
NULL = ''
COLON = ':'

# WiFi Network And Password...
NETWORK = '*****'
PASSWORD = '*****'

# Attempt Connect...
ATTEMPTS = const(30)

# Types...
WIRELESS = 'Wireless'
WIRED = 'Wired'

# Ethernet Device..
W5500 = {
    'Interrupt': 38,
    'Carrier': 39,
    'Reset': ZERO
}

# Serial Peripheral Interface...
PERIPHERAL = {
    'Rate': 40*1000*1000,
    'Bus': ONE,
    'Clock': 21,
    'MOSI': ONE,
    'MISO': 14
}

#
PAGE = """<!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{}</title>
        </head>
        <body>
            <div>
                <p>
                    {}
                </p>
            <div>
        </body>
    </html>
"""

# Globals...
theDiode = None
theWireless = None
theWired = None
theBus = None
theTimer = None

#
def Session(theCamera, theClient):
    from time import time
    
    global TITLE, BUFFER, theDiode, ZERO, ONE, TWO, RETURN, SPACE, PAGE, _TITLE_, _VERSION_, _RELEASE_, _AUTHOR_
        
    #
    try:
        
        #
        theRequest = theClient.recv(BUFFER)
        if (theRequest is None):
            Exception('No Request?')
        
        #
        theRequest = theRequest.decode().replace(RETURN, SPACE).lower()
        print(f"Session Request '{theRequest}'")
        
        if ('host' in theRequest):
            print(f"Session Interface '{theRequest.split(COLON)[ONE].split(SPACE)[ONE]}'")
        
        # Reset...
        if ('get /reset' in theRequest):
            from machine import reset as Reset
            from time import sleep
            
            #
            print('Session Reset')
            
            #
            theClient.sendall(b'HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n' + PAGE.format(_TITLE_, 'Reset'))
            
            # Give Client Time To Send Before Reset...
            sleep(TWO)
            
            #
            Reset()
            
        # Stream...
        elif ('get /stream' in theRequest):
            theClient.send(b'HTTP/1.1 200 OK\nContent-Type: multipart/x-mixed-replace; boundary=frame\n\n')              

            theFrames = ZERO
            theFrame = ZERO
            theTime = ZERO
            
            #
            print('Session! Stream')
            
            #
            theCamera.init()
            
            # Turn On...
            theDiode.value(True)
            
            #
            while theCamera:
                try:
                    theCapture = theCamera.capture()
                    if (theCapture is not None):
                        theFrames += ONE
                        
                        #
                        if (theTime != time()):
                            print(f"Stream Time {time()} Frame {theFrames} ({theFrames - theFrame} Frames/Second)")

                            theTime = time()
                            theFrame = theFrames

                        #
                        theClient.send(b'--frame\nConnect-Type: image/jpeg\n\n' + theCapture + b'\n')
                        
                    else:
                        break

                except KeyboardInterrupt:
                    print('Stream Keyboard Interrupt')
                    
                    #
                    raise
                    
        # Default...
        else:
            print('Session! Default')
            
            #
            theClient.sendall(b'HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n' + PAGE.format(_TITLE_, f"{_TITLE_} * {_VERSION_} * {_RELEASE_} * {_AUTHOR_}"))

    except KeyboardInterrupt:
        print('Session Keyboard Interrupt')
            
        #
        raise
        
    except OSError as theError:
        print(theError)
            
    except Exception as theException:
        print_exception(theException)
    
    finally:
        if (theClient is not None):
            theClient.close()
            
        # Turn Off...
        theDiode.value(False)
        
        #
        theCamera.deinit()

#
def Stream():
    from camera import Camera, FrameSize, PixelFormat
    from sys import print_exception
    from socket import socket, SOL_SOCKET, SO_REUSEADDR, getaddrinfo
    
    global PORT, ONE, ZERO
    
    theCamera = None
    theSocket = None
    
    #
    try:

        #
        theCamera = Camera(frame_size=FrameSize.HD, pixel_format=PixelFormat.JPEG, init=False)
        if (theCamera is None):
            raise Exception('No Camera?')
    
        # Use 0.0.0.0 For All Interfaces...
        theAddress = getaddrinfo('0.0.0.0', PORT)[ZERO][-ONE]
        theSocket = socket()
        if (theSocket is None):
            raise Exception('No Socket?')
    
        #
        theSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, ONE)
        theSocket.bind(theAddress)
        theSocket.listen(ONE)

        #
        theAddress, thePort = theAddress
        
        #
        print(f"Socket Open {theAddress} Port {thePort}")

        #
        theClient = None
        
        #
        while True:
            try:
                #
                print(f"Client Connect?")
                
                theClient, theAddress = theSocket.accept()
                if (theClient is None):
                    raise Exception('No Client?')
                
                #
                theAddress, thePort = theAddress
                print(f"Client Connect! {theAddress} Port {thePort}")
                
                #
                Session(theCamera, theClient)
               
            except KeyboardInterrupt:
                print('Client Accept Keyboard Interrupt')
                
                #
                raise

            except Exception as theException:
                print_exception(theException)

            finally:
                if (theClient is not None):
                    theClient.close()

                    #
                    print('Client Disconnect!')

    #
    except KeyboardInterrupt:
        print('Stream Keyboard Interrupt')
        
        #
        raise
    
    except Exception as theException:
        print_exception(theException)
        
    finally:
        if (theSocket is not None):
            print('Socket Close')
            
            #
            theSocket.close()
        
        if (theCamera is not None):
            # No Camera Close Method... Let Garage Collection Handle Object...
            theCamera = None
    
#
def Configuration(theType, theInterface):
    theIp,theMask,theGate,theServer = theInterface.ifconfig()
    theMAC = theInterface.config('mac').hex(':').upper()
    
    #
    print(f"{theType} Ip Address {theIp}, Subnet Mask {theMask}, Gateway {theGate}, Name Server {theServer}, MAC {theMAC}")

#
def Connect(theType, theInterface, theAttempts):
    from time import sleep

    global ATTEMPTS
    
    #
    while (not(theInterface.isconnected())) and (theAttempts):
        print(f"{theType} Connect? Attempt {ATTEMPTS - theAttempts}")
        
        #
        sleep(ONE)
        theAttempts -= ONE

    #
    theConnectOrNot = theInterface.isconnected()
    print(f"{theType} Connect! {theConnectOrNot}")
    
    #
    return theConnectOrNot

#
def Blink(theTimer):
    global theDiode
    
    #
    theDiode.value(not (theDiode.value()))
    
    #
    print(f"Blink {'On' if (theDiode.value()) else 'Off'}")

#
def Start():
    global theTimer, theDiode

    #
    theDiode = Pin(2, Pin.OUT) # On Board Diode GPIO 2
    if (theDiode is None):
        raise Exception('No Diode?')

    #
    theDiode.value(True)
    
    #
    theTimer = Timer(False) # Hardware Timer...
    if (theTimer is None):
        raise Exception('No Timer?')
    
    # Start Timer With 1 Second Interval Repeat...
    theTimer.init(period=1000, mode=Timer.PERIODIC, callback=Blink)

    #
    print('Blink On')
    
#
def Stop():
    global theTimer, theDiode
    
    #
    if (theTimer is not None):
        theTimer.deinit()

    #
    if (theDiode is not None):
        if (theDiode.value()):
            theDiode.value(False)
            
            #
            print('Blink Off')

#
def Main():
    from network import WLAN, STA_IF, LAN, PHY_W5500 # WiFi And Ethernet
    
    global ONE, ATTEMPTS, WIRED, WIRELESS, PERIPHERAL, theWired, theWireless, theBus
    
    #
    try:

        #
        print(f"{_TITLE_} * {_VERSION_} * {_RELEASE_} * {_AUTHOR_}")
        
        # Start Blink On Board Diode...
        Start()

        # Wireless ESP32 Generic...
        theWireless = WLAN(STA_IF)
        if (theWireless is None):
            raise Exception('No Wireless Interface?')
        theWireless.active(True)
        
        #
        theWireless.connect(NETWORK, PASSWORD)       
        
        #
        if (not(Connect(WIRELESS, theWireless, ATTEMPTS))):
            raise Exception('No Wireless Connect?')
    
        Configuration(WIRELESS, theWireless)
        
        # Wired (Ethernet) ESP32 Stick POE P CAM W5500 Pins, int=39, carrier=39, SPI Bus 1, clock=21, miso=14, mosi=1 Pins...
        theBus = SPI(PERIPHERAL['Bus'], baudrate=PERIPHERAL['Rate'], sck=Pin(PERIPHERAL['Clock']), mosi=Pin(PERIPHERAL['MOSI']), miso=Pin(PERIPHERAL['MISO']))
        if (theBus is None):
            raise Exception('No Bus?')
        
        #
        print(repr({theBus}))

        #
        theWired = LAN(phy_type=PHY_W5500, spi=theBus, phy_addr=ONE, cs=Pin(W5500['Carrier']), int=Pin(W5500['Interrupt']), reset=Pin(W5500['Reset']))
        if (theWired is None):
            raise Exception('No Wired Interface?')
        theWired.active(True)

        #
        if (not(Connect(WIRED, theWired, ATTEMPTS))):
            raise Exception('No Wired Connect?')
        
        #
        Configuration(WIRED, theWired)
        
        # Stop Blink...
        Stop()
        
        #
        print(f'Reset Board When Ethernet Stream Frame Rate Slow...')
        
        #
        Stream()

    except KeyboardInterrupt:
        print('Main Keyboard Interrupt')
    
    except Exception as theException:
        print_exception(theException)
        
    finally:
        
        # Stop Blink...
        Stop()    
            
        #
        if (theWireless is not None):
            theWireless.disconnect()
            theWireless.active(False)
            
        if (theWired is not None):
            # LAN Object As No Disconnect
            theWired.active(False)
            
        if (theBus is not None):
            try:
                theBus.deinit()
            except:
                pass

#
if (__name__ == '__main__'):
    Main()

    
