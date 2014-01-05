# -*- coding: utf-8 -*-

from AbstractDevice import AbstractDevice

from __future__ import print_function
import subprocess, time, Image, socket, imp, os, sys
import random
import RPi.GPIO as GPIO
from random import randint

Adafruit_Thermal = imp.load_source('Adafruit_Thermal', 'vendors/Python-Thermal-Printer/Adafruit_Thermal.py')

class PhysicalDevice(AbstractDevice):
    holdTime     = 2     # Duration for button hold (shutdown)
    tapTime      = 0.01  # Debounce time for button taps
    nextInterval = 0.0   # Time of next recurring operation
    lastId       = '1'   # State information passed to/from interval script

    def __init__(self):
        self.leds = {'left': 24, 'middle': 18, 'right': 17}
        self.buttons = {'left': 25, 'middle': 23, 'right': 22}
        self.printer = Adafruit_Thermal.Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

        GPIO.setmode(GPIO.BCM)

        for led, pin in self.leds.items():
            print "setup led", led, "on OUT"
            GPIO.setup(pin, GPIO.OUT)

        for button, pin in self.buttons.items():
            print "setup button", button, "on OUT"
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read(self):
        # Poll initial button state and time
        prevButtonState = GPIO.input(buttonPin)
        prevButtonState2 = GPIO.input(buttonPin2)
        prevButtonState3 = GPIO.input(buttonPin3)
        prevTime        = time.time()
        prevTime2       = time.time()
        prevTime3       = time.time()
        tapEnable       = False
        tapEnable2      = False
        tapEnable3      = False
        holdEnable      = False
        holdEnable2     = False
        holdEnable3     = False

        # Main loop
        while(True):

            # Poll current buttons states and time
            buttonState = GPIO.input(buttonPin)
            buttonState2 = GPIO.input(buttonPin2)
            buttonState3 = GPIO.input(buttonPin3)
            t = time.time()

            # Has button1 state changed?
            if buttonState != prevButtonState:
                prevButtonState = buttonState   
                prevTime        = t
            else:                            
              if (t - prevTime) >= holdTime: 
                if holdEnable == True:        
                  hold()                      
                  holdEnable = False          
                  tapEnable  = False          
              elif (t - prevTime) >= tapTime: 
                if buttonState == True:      
                  if tapEnable == True:       
                    tap()                     
                    tapEnable  = False        
                    holdEnable = False
                else:                         
                  tapEnable  = True           
                  holdEnable = True

            # Has button2 state changed?
            if buttonState2 != prevButtonState2:
              prevButtonState2 = buttonState2   # Yes, save new state/time
              prevTime2        = t
            else:                             # Button state unchanged
              if (t - prevTime2) >= holdTime:  # Button held more than 'holdTime'?
                # Yes it has.  Is the hold action as-yet untriggered?
                if holdEnable2 == True:        # Yep!
                  hold()                      # Perform hold action (usu. shutdown)
                  holdEnable2 = False          # 1 shot...don't repeat hold action
                  tapEnable2  = False          # Don't do tap action on release
              elif (t - prevTime) >= tapTime: # Not holdTime.  tapTime elapsed?
                # Yes.  Debounced press or release...
                if buttonState2 == True:       # Button released?
                  if tapEnable2 == True:       # Ignore if prior hold()
                    tap2()                     # Tap triggered (button released)
                    tapEnable2  = False        # Disable tap and hold
                    holdEnable2 = False
                else:                         # Button pressed
                  tapEnable2  = True           # Enable tap and hold actions
                  holdEnable2 = True
            
            # Has button3 state changed?
            if buttonState3 != prevButtonState3:
              prevButtonState3 = buttonState3  
              prevTime3        = t
            else:                            
              if (t - prevTime3) >= holdTime: 
                if holdEnable3 == True:       
                  hold()                     
                  holdEnable3 = False          
                  tapEnable3  = False         
              elif (t - prevTime) >= tapTime: 
                if buttonState3 == True:      
                  if tapEnable3 == True:   
                    tap3()                     
                    tapEnable3  = False 
                    holdEnable3 = False
                else:         
                  tapEnable3  = True   
                  holdEnable3 = True

            # LED blinks while idle, for a brief interval every 2 seconds.
            if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
              GPIO.output(ledPin, GPIO.HIGH)
              GPIO.output(ledPin2, GPIO.HIGH)
              GPIO.output(ledPin3, GPIO.HIGH)
            else:
              GPIO.output(ledPin, GPIO.LOW)
              GPIO.output(ledPin2, GPIO.LOW)
              GPIO.output(ledPin3, GPIO.LOW)

    def led_on(self, led):
        print "LED", led, "on"
        GPIO.output(self.leds[led], GPIO.HIGH)

    def led_off(self, led):
        print "LED", led, "off"
        GPIO.output(self.leds[led], GPIO.HIGH)

    def println(self, line=''):
        print "println() not implemented"

    def print_text(self, txt):
        print "print_text() not implemented"

    def print_image(self, path):
        print "Printing image", path
        image = Image.open(path)
        if not image:
            print "no image found"
        self.printer.printImage(image, True)

    def feed(self, n):
        print "feed() not implemented"