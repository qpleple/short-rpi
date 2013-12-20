#!/usr/bin/python

# Main script for Adafruit Internet of Things Printer 2.  Monitors button
# for taps and holds, performs periodic actions (Twitter polling by default)
# and daily actions (Sudoku and weather by default).
# Written by Adafruit Industries.  MIT license.
#
# MUST BE RUN AS ROOT (due to GPIO access)
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, Image, socket
from Adafruit_Thermal import *
from random import randint

ledPin       = 18
buttonPin    = 23
ledPin2      = 24
buttonPin2   = 25
ledPin3      = 17
buttonPin3   = 22
holdTime     = 2     # Duration for button hold (shutdown)
tapTime      = 0.01  # Debounce time for button taps
nextInterval = 0.0   # Time of next recurring operation
lastId       = '1'   # State information passed to/from interval script
printer      = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)


# Called when button1 (au milieu) is briefly tapped.  Imprime les Tres tres court version 3 minutes.
def tap():
  GPIO.output(ledPin, GPIO.HIGH)  # LED on while working
  printer.printImage(Image.open('gfx/logonb.png'), True)
  printer.feed(2)
  a=randint(1,10)
  s=str(a)
  f=open("ttc3min/ttc3min_"+s+".txt", "r")
  line=f.readline()
  printer.doubleHeightOn()
  printer.println(line)
  printer.doubleHeightOff()
  time.sleep(2)
  line=f.readline()
  while line:
    printer.println(line)
    line=f.readline()
    time.sleep(2)
  f.close()
  time.sleep(3)
  printer.feed(2)
  printer.printImage(Image.open('gfx/logonb.png'), True)
  printer.feed(2)
  printer.println("pour plus de lecture RDV sur    http://short-edition.com/")
  printer.feed(4)
  GPIO.output(ledPin, GPIO.LOW)

# Called when button2 (gauche) is briefly tapped.  Imprime les Tres tres court version 1 minute.
def tap2():
  GPIO.output(ledPin2, GPIO.HIGH)  # LED on while working
  printer.printImage(Image.open('gfx/logonb.png'), True)
  printer.feed(2)
  a=randint(1,7)
  s=str(a)
  f=open("ttc1min/ttc1min_"+s+".txt", "r")
  line=f.readline()
  printer.doubleHeightOn()
  printer.println(line)
  printer.doubleHeightOff()
  line=f.readline()
  while line:
    printer.println(line)
    line=f.readline()
    time.sleep(1)
  f.close()
  printer.feed(2)
  printer.printImage(Image.open('gfx/logonb.png'), True)
  printer.feed(2)
  printer.println("pour plus de lecture RDV sur    http://short-edition.com/")
  printer.feed(4)
  GPIO.output(ledPin2, GPIO.LOW)

# Called when button3 is briefly tapped.  Imprime les poemes.
def tap3():
  GPIO.output(ledPin3, GPIO.HIGH)  # LED on while working
  printer.printImage(Image.open('gfx/logonb.png'), True)
  printer.feed(2)
  a=randint(1,6)
  s=str(a)
  f=open("poemes/poeme_"+s+".txt", "r")
  line=f.readline()
  printer.doubleHeightOn()
  printer.println(line)
  printer.doubleHeightOff()
  line=f.readline()
  while line:
    printer.println(line)
    line=f.readline()
    time.sleep(0.1)
  f.close()
  printer.feed(2)
  time.sleep(2)
  printer.printImage(Image.open('gfx/logonb.png'), True)
  printer.feed(2)
  printer.println("pour plus de lecture RDV sur    http://short-edition.com/")
  printer.feed(4)
  GPIO.output(ledPin3, GPIO.LOW)

# Called when button is held down.  Prints image, invokes shutdown process.
def hold():
  GPIO.output(ledPin, GPIO.HIGH)
  GPIO.output(ledPin2, GPIO.HIGH)
  GPIO.output(ledPin3, GPIO.HIGH)
  printer.printImage(Image.open('gfx/goodbye.png'), True)
  printer.feed(3)
  subprocess.call("sync")
  subprocess.call(["shutdown", "-h", "now"])
  GPIO.output(ledPin, GPIO.LOW)
  GPIO.output(ledPin2, GPIO.LOW)
  GPIO.output(ledPin3, GPIO.LOW)

# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
GPIO.setmode(GPIO.BCM)

# Enable LEDs and buttons (w/pull-up on latter)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ledPin2, GPIO.OUT)
GPIO.setup(buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ledPin3, GPIO.OUT)
GPIO.setup(buttonPin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LEDs on while working
GPIO.output(ledPin, GPIO.HIGH)
GPIO.output(ledPin2, GPIO.HIGH)
GPIO.output(ledPin3, GPIO.HIGH)

# Processor load is heavy at startup; wait a moment to avoid
# stalling during greeting.
time.sleep(30)

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
  t           = time.time()

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

  # LED blinks while idle, for a brief interval every 2 seconds.
  if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
    GPIO.output(ledPin, GPIO.HIGH)
  else:
    GPIO.output(ledPin, GPIO.LOW)

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

  # LED blinks while idle, for a brief interval every 2 seconds.
  if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
    GPIO.output(ledPin2, GPIO.HIGH)
  else:
    GPIO.output(ledPin2, GPIO.LOW)
  
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
    GPIO.output(ledPin3, GPIO.HIGH)
  else:
    GPIO.output(ledPin3, GPIO.LOW)

