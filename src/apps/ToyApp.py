# -*- coding: utf-8 -*-

from AbstractApp import AbstractApp
from termcolor import colored, cprint

class ToyApp(AbstractApp):
  
  def run(self):
    while True:
        action = self.device.read()
        
        if action == 'right':
            self.device.led_on('right')
        elif action == 'RIGHT':
            self.device.led_off('right')
