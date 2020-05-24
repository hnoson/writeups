#!/usr/bin/env python

flag = ''
x = 1
for i, nstr in enumerate(open('./output.txt').read().split(' ')[:-1]):
    n = int(nstr)
    for c in range(0x100):
        y = pow(x*((i+1)^c), 463, 64711)
        if y == n:
            flag += chr(c)
            x = y % 128 + 1
            break
print flag
