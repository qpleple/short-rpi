# -*- coding: utf-8 -*-

from AbstractDevice import AbstractDevice

import sys, tty, termios
from termcolor import colored, cprint

class SimulatorDevice(AbstractDevice):
    key_map = {
        'a': 'left', 'z': 'middle', 'e': 'right',
        'A': 'LEFT', 'Z': 'MIDDLE', 'E': 'RIGHT',
    }

    def read_char(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def read(self):
        while True:
            c = self.read_char()
            if c in self.key_map:
                print "Btn:", self.key_map[c]
                return self.key_map[c]
            elif ord(c) == 3:
                raise Exception('User interrupted')

    def print_text(self, text):
        cprint(text, 'yellow')

    def print_image(self, image):
        print "Image:", image

    def led_on(self, led):
        print "Led:", led.upper()

    def led_off(self, led):
        print "Led:", led.lower()