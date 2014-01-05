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
                cprint("Btn: " + self.key_map[c], 'yellow')
                return self.key_map[c]
            elif ord(c) == 3:
                raise Exception('User interrupted')

    def println(self, line=''):
        print '| {:<32} |'.format(line[:32])

    def print_image(self, image):
        self.println('{:^32}'.format('[' + str(image) + ']'))

    def led_on(self, led):
        cprint("Led: " + led.upper(), 'yellow')

    def led_off(self, led):
        cprint("Led: " + led.lower(), 'yellow')