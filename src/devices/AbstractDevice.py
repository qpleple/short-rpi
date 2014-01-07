# -*- coding: utf-8 -*-

import re, sys

class AbstractDevice():
    font = 'default'

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

    def set_font(self, font):
        print "set_font() not implemented"

    def set_timeout(self, x):
        print "set_timeout() not implemented"

    def get_line_length(self):
        return 32 if self.font == 'default' else 42

    def feed(self, n):
        for _ in range(n):
            self.println()

    def print_text(self, text, justified=False):
        lines = []
        line_length = self.get_line_length()
        paragraphs = self.word_wrap(text, line_length)
        for paragraph in paragraphs:
            for i, line in enumerate(paragraph):
                if justified and i+1 < len(paragraph):
                    line = self.justify_line(line, line_length)
                lines.append(line)

        # print lines by batch of 50 and wait 10sec b/w each batch
        n = len(lines)
        for i in range(n // 50):
            start = 50 * i
            big_line = '\n'.join(lines[start:start+50])
            self.println(big_line)

            # wait only if it's not the last iteration
            if i+1 < n // 50:
                self.set_timeout(10)

        self.println('\n'.join(lines[start+50:]))


    def word_wrap(self, text, line_length):
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
