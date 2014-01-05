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

  def print_text(self, txt):
    print "print_text() not implemented"

  def print_image(self, path):
    print "print_image() not implemented"

  def feed(self, n):
    print "feed() not implemented"