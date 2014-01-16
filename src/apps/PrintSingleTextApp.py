# -*- coding: utf-8 -*-

from AbstractApp import AbstractApp
from termcolor import colored, cprint
import fileinput

class PrintSingleTextApp(AbstractApp):
    def run(self):
        text = ''
        for x in fileinput.input():
            text += x
        self.device.print_text(text)
          