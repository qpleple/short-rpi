# -*- coding: utf-8 -*-

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
  
    def println(self, line):
        print "println() not implemented"

    def feed(self, n):
        self.println('\n' * (n - 1))

    def print_text(self, text):
        for line in text.split('\n'):
            self.println(line)

    def word_wrap(self, content, line_length):
        pars = []
        for row in content:
            lines = []
            words = row.split(' ')
            line = ''
            for word in words:
                if len(word) + len(line) > line_length:
                    lines.append(line)
                    line = ''
                line += (' ' if line else '') + word
            lines.append(line)
            pars.append(lines)

        return pars

    def justify_line(self, line, line_length):
        if not line.strip():
            return ''

        words = line.split(' ')
        n = len(words) - 1
        spaces = [1] * n
        for i in range(line_length - len(line)):
            spaces[i % n] += 1
        
        new_line = words[0]
        for i, nb_space in enumerate(spaces):
            new_line += ' ' * nb_space + words[i+1]

        return new_line
