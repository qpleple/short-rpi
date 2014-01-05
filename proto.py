#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess, time, Image, socket, imp, os, sys
import random
import RPi.GPIO as GPIO
from random import randint
Adafruit_Thermal = imp.load_source('Adafruit_Thermal', 'vendors/Python-Thermal-Printer/Adafruit_Thermal.py')

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
printer      = Adafruit_Thermal.Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

def print_logo():
  printer.printImage(Image.open('ressources/logo-384.bmp'), True)

def get_random_post(directory):
  dir_path = os.path.join('posts', directory)
  (_, _, filenames) = os.walk(dir_path).next()
  path = os.path.join(dir_path, random.choice(filenames))

  print('Post : ' + path)
  with open(path) as f:
    lines = f.readlines()

  return lines

def print_random_post(directory):
  # print_logo()
  # printer.feed(2)

  lines = get_random_post(directory)

  # titre
  printer.justify('C')
  printer.setSize('L')
  printer.println(lines[0])
  printer.justify('L')
  printer.setSize('S')

  # printer.doubleHeightOn()
  # printer.println(lines[0])
  # printer.doubleHeightOff()

  time.sleep(2)
  for line in lines[1:]:
    printer.println(line)
    time.sleep(2)
  
  printer.feed(4)

# Called when button1 (au milieu) is briefly tapped.  Imprime les Tres tres court version 3 minutes.
def tap():
  GPIO.output(ledPin, GPIO.HIGH)
  print_random_post('ttc3min')
  GPIO.output(ledPin, GPIO.LOW)

# Called when button2 (gauche) is briefly tapped.  Imprime les Tres tres court version 1 minute.
def tap2():
  GPIO.output(ledPin2, GPIO.HIGH)
  print_random_post('ttc1min')
  GPIO.output(ledPin2, GPIO.LOW)

# Called when button3 is briefly tapped.  Imprime les poemes.
def tap3():
  GPIO.output(ledPin3, GPIO.HIGH)
  print_random_post('poemes')
  GPIO.output(ledPin3, GPIO.LOW)

# Called when button is held down.  Prints image, invokes shutdown process.
def hold():
  GPIO.output(ledPin, GPIO.HIGH)
  GPIO.output(ledPin2, GPIO.HIGH)
  GPIO.output(ledPin3, GPIO.HIGH)
  printer.println("Ok !")
  printer.println("Laisse moi 30sec pour m'éteindre")
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
# time.sleep(30)

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


try:
  print("Entering main loop")

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
except Exception, e:
  print(e)
  printer.println(str(e))