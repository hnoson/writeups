#!/usr/bin/env python

f = open('./c')
f.readline()
e, n = eval(f.readline())
f.readline()
f.readline()
table = {}
for i in range(0x100):
    table[pow(i, e, n)] = i
flag = ''
for c in eval(f.readline()):
    flag += chr(table[c])
print flag
