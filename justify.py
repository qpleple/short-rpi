#!/usr/bin/python

pars = open('posts/ttc3min/1.txt').readlines()


line_width = 32
lines = []
for par in pars:
    words = par.split(' ')
    line = ''
    for word in words:
        if len(word) + len(line) > line_width:
            lines.append(line)
            line = ''
        line += (' ' if line else '') + word
    lines.append(line)

for line in lines:
    print line