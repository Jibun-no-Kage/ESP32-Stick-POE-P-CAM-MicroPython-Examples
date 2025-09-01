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

_RELEASE_ = '08/31/2025'
_TITLE_ = 'Wireless And Wired Camera Stream Example'
_VERSION_ = '1.0.3'
_AUTHOR_ = 'Jibun no Kage'

from machine import Pin, Timer, SPI
from sys import print_exception

# Constants...
ZERO = const(0)
ONE = const(1)

# WiFi Network And Password...
NETWORK = 'Media'
PASSWORD = 'M3d!@ T3@m'

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

# Globals...
theDiode = None
theWireless = None
theWired = None
theBus = None
theTimer = None
    
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
    from time import sleep
    
    global RATE, ONE, ATTEMPTS, WIRED, WIRELESS, SPI, theWireless, theWired, theBus
    
    #
    try:

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
        print(f'Ping Wireless And Wired Interfaces...')

        #
        while True:
            sleep(ONE)
            
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
    