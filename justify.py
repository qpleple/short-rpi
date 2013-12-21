#!/usr/bin/python



def word_wrap(content, line_length):
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

def justify_line(line, line_length):
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


# insert 3
print '-' * 32
justify_line("aaaa aaaaaaa aaaaaa aaaaaa aa", 32)


content = open('posts/ttc3min/1.txt').readlines()
pars = word_wrap(content, 32)

for par in pars:
    for line in par[:-1]:
        print justify_line(line, 32)
    print par[-1]