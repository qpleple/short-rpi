# -*- coding: utf-8 -*-
from AbstractDevice import AbstractDevice

import sys, tty, termios
from termcolor import colored

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class SimulatorDevice(AbstractDevice):
    def read(self):
        while True:
            c = get_char()
            if c == 'a':
                print "Btn: left"
                return 'left'
            elif c == 'z':
                print "Btn: middle"
                return 'middle'
            elif c == 'e':
                print "Btn: right"
                return 'right'
            elif c == 'A':
                print "Btn: LEFT"
                return 'LEFT'
            elif c == 'Z':
                print "Btn: MIDDLE"
                return 'MIDDLE'
            elif c == 'E':
                print "Btn: RIGHT"
                return 'RIGHT'
            elif ord(c) == 3:
                raise Exception('User interrupted')

    def led_on(self, led):
        print "Led:", led.upper()

    def led_off(self, led):
        print "Led:", led.lower()