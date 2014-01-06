# -*- coding: utf-8 -*-

import re, sys

class AbstractDevice():
    def read(self):
        """
        waits for an action and returns 'left', 'middle' or 'right'
        when a button is pressed and 'LEFT', 'MIDDLE' or 'RIGHT' when a
        button is held
        """
        print "read() not implemented"
  
    def led_on(self, led):
        print "led_on() not implemented"
  
    def led_off(self, led):
        print "led_off() not implemented"
  
    def print_image(self, path):
        print "print_image() not implemented"
  
    def println(self, line=''):
        print "println() not implemented"

    def feed(self, n):
        for _ in range(n):
            self.println()

    def print_text(self, text):
        paragraphs = self.word_wrap(text)
        for paragraph in paragraphs:
            for line in paragraph:
                self.println(line)

    def word_wrap(self, text, line_length=32):
        output = []
        paragraphs = text.splitlines()
        for paragraph in paragraphs:
            lines = []
            line = ''
            words = re.split("\s+", paragraph)
            for word in words:
                if len(word) + 1 + len(line) > line_length:
                    lines.append(line)
                    line = ''
                line += (' ' if line else '') + word

            lines.append(line)
            output.append(lines)

        return output

    def justify_line(self, line, line_length):
        if not line.strip():
            return ''

        words = re.split("\s+", line)
        n = len(words) - 1
        spaces = [1] * n
        for i in range(line_length - len(line)):
            spaces[i % n] += 1
        
        new_line = words[0]
        for i, nb_space in enumerate(spaces):
            new_line += ' ' * nb_space + words[i+1]

        return new_line
