# -*- coding: utf-8 -*-

import time, Image, imp
import RPi.GPIO as GPIO
from AbstractDevice import AbstractDevice

Adafruit_Thermal = imp.load_source('Adafruit_Thermal', '../vendors/Python-Thermal-Printer/Adafruit_Thermal.py')

class PhysicalDevice(AbstractDevice):
    holdTime     = 2     # Duration for button hold
    tapTime      = 0.01  # Debounce time for button taps

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
        prevTime, prevState, pressed = {}, {}, {}

        for button, pin in self.buttons.items():
            prevState[button] = GPIO.input(pin)
            print "Initial state", button, ":", prevState[button]
            prevTime[button] = time.time()
            pressed[button] = False
        
        print "entering main loop"
        while(True):
            for button, pin in self.buttons.items():
                # Record change of state
                state = GPIO.input(pin)
                t = time.time()
                if state != prevState[button]:
                    print button, ": state = ", prevState[button], "->", state
                    prevState[button] = state
                    prevTime[button] = t
                    
                
                # Button held more than 'holdTime'?
                if (t - prevTime[button]) >= self.holdTime:
                    if pressed[button]:
                        # don't repeat action
                        pressed[button] = False
                        # Send back hold action for this button
                        return button.upper()
                # Not holdTime.  tapTime elapsed?
                elif (t - prevTime[button]) >= self.tapTime:
                    # Yes.  Debounced press or release...
                    # Button released?
                    if state:
                        if pressed[button]:
                            # don't repeat action
                            pressed[button] = False
                            # Tap triggered (button released)
                            # Send tapped hold action for this button
                            return button
                    else:
                        # Button pressed
                        # Enable tap and hold actions
                        pressed[button] = True

            # LED blinks while idle, for a brief interval every 2 seconds.
            # if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
            #     self.led_on('left')
            #     self.led_on('middle')
            #     self.led_on('right')
            # else:
            #     self.led_off('left')
            #     self.led_off('middle')
            #     self.led_off('right')

    def led_on(self, led):
        print "LED", led, "on"
        GPIO.output(self.leds[led], GPIO.HIGH)

    def led_off(self, led):
        print "LED", led, "off"
        GPIO.output(self.leds[led], GPIO.HIGH)

    def println(self, line=''):
        self.printer.println(line)

    def print_text(self, txt):
        print "print_text() not implemented"

    def print_image(self, path):
        print "Printing image", path
        image = Image.open(path)
        if not image:
            print "no image found"
        self.printer.printImage(image, True)