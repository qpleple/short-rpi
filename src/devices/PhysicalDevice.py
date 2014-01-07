# -*- coding: utf-8 -*-

import time, Image, imp
import RPi.GPIO as GPIO
from AbstractDevice import AbstractDevice

Adafruit_Thermal = imp.load_source('Adafruit_Thermal', '../vendors/Python-Thermal-Printer/Adafruit_Thermal.py')

class PhysicalDevice(AbstractDevice):
    holdTime = 2     # Duration for button hold
    tapTime = 0.01  # Debounce time for button taps
    heatTime = 60

    def __init__(self):
        self.leds = {'left': 24, 'middle': 18, 'right': 17}
        self.buttons = {'left': 25, 'middle': 23, 'right': 22}
        self.printer = Adafruit_Thermal.Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
        # set heat time to 150
        self.printer.begin(self.heatTime)

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

        states = {}
        for button, pin in self.buttons.items():
            prevState[button] = self.btn_state(button)
            states[button] = []
            print "initial state", button, ":", prevState[button]
            
        print "entering main loop..."
        while(True):
            for button, pin in self.buttons.items():
                state = self.btn_state(button)
                t = time.time()

                if state != prevState[button]:
                    prevState[button] = state
                    states[button].append({'state': state, 'time': t})

                    # second change of state to 'released' before holdTime timeout: it's a tap!
                    if len(states[button]) >= 2 and states[button][-1]['state'] == 'released':
                        return button

                # state 'pressed' held during holdTime, it's a hold!
                if state == 'pressed' and len(states[button]) >= 1 and t - states[button][-1]['time'] > self.holdTime:
                    return button.upper()

            if t - int(t) < 0.25 :
                self.led_on('left')
                self.led_on('middle')
                self.led_on('right')
            else:
                self.led_off('left')
                self.led_off('middle')
                self.led_off('right')
    
    def set_font(self, font):
        if font == 'default':
            self.printer.writeBytes(0x1B, 0x21, 0x0)
            self.printer.setLineHeight(32)
        elif font == 'fontb':
            self.printer.writeBytes(0x1B, 0x21, 0x1)
            self.printer.setLineHeight(28)
        else:
            raise Exception('Unknown font: ' + font)
        
        self.font = font

    def btn_state(self, button):
        return 'released' if GPIO.input(self.buttons[button]) else 'pressed'

    def led_on(self, led):
        GPIO.output(self.leds[led], GPIO.HIGH)

    def led_off(self, led):
        GPIO.output(self.leds[led], GPIO.LOW)

    def println(self, line=''):
        self.printer.println(line.encode('cp437', 'replace'))

    def print_image(self, path):
        print "Printing image", path
        image = Image.open(path)
        if not image:
            print "no image found"

        self.printer.begin(150)
        self.printer.printImage(image, True)
        self.printer.begin(self.heatTime)

    def set_timeout(self, x):
        self.printer.timeoutSet(x)