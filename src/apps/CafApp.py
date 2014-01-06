# -*- coding: utf-8 -*-

import os, random, subprocess
from AbstractApp import AbstractApp

class CafApp(AbstractApp):
    def print_random_post(self, directory):
        dir_path = os.path.join('../posts', directory)
        (_, _, filenames) = os.walk(dir_path).next()
        path = os.path.join(dir_path, random.choice(filenames))
        
        with open(path) as f:
            text = f.read()

        self.device.feed(1)
        self.device.print_image('../ressources/logo-384.bmp')
        self.device.feed(1)
        self.device.print_text(text)
        self.device.feed(2)

    def shutdown(self):
        self.device.led_off('left')
        self.device.led_off('middle')
        self.device.led_off('right')
        
        self.device.print_text("Ok !\nLaisse moi 30sec pour m'éteindre")
        self.device.feed(2)

        # subprocess.call("sync")
        # subprocess.call(["shutdown", "-h", "now"])

    def main_loop(self):
        while True:
            action = self.device.read()
            if action == 'left':
                self.device.led_on('left')
                self.print_random_post('ttc1min')
                self.device.led_off('left')
            elif action == 'middle':
                self.device.led_on('middle')
                self.print_random_post('ttc3min')
                self.device.led_off('middle')
            elif action == 'right':
                self.device.led_on('right')
                self.print_random_post('poemes')
                self.device.led_off('right')
            elif action in ['LEFT', 'MIDDLE', 'RIGHT']:
                self.shutdown()

    def run(self):
        try:
            self.main_loop()
        except Exception, e:
            self.device.println("Error:")
            self.device.print_text(str(e))

            self.device.feed(1)
            self.device.println("I'm done.")
            self.device.feed(3)
