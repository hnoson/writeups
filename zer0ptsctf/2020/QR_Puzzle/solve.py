#!/usr/bin/env python
import re

qr = [list(line.strip()) for line in open('./encrypted.qr')]
for key in open('./key'):
    op, col, row = map(int, re.search('(\d*)#\((\d*),(\d*)', key).groups())

    if op == 0:
        qr[row][col], qr[row][col-1] = qr[row][col-1], qr[row][col]
    elif op == 1:
        qr[row][col], qr[row][col+1] = qr[row][col+1], qr[row][col]
    elif op == 2:
        qr[row][col], qr[row-1][col] = qr[row-1][col], qr[row][col]
    else:
        qr[row][col], qr[row+1][col] = qr[row+1][col], qr[row][col]

def convert(c):
    if c == '0':
        return ' '
    elif c == '1':
        return u'\u2588'
    else:
        return c

print ''.join(map(convert, '\n'.join(map(''.join, qr))))
