#!/usr/bin/env python

encoded = "zmu}jnd{o{f_ndo{{_hz_{ga"
table = "_`qwertyuiop{}asdfghjklzxcvbnm|"

o = [chr(i) for i in range(0x5f,0x7d+1)]
t = [chr(i) for i in range(0x5f,0x7d+1)]
for i in range(len(t)):
    t[i] = table[ord(t[i]) - 0x5f]
for i in range(len(t)):
    t[i] = table[ord(t[i]) - 0x5f]
for i in range(len(t)):
    t[i] = table[ord(t[i]) - 0x5f]
d = {}
for i,c in enumerate(t):
    d[c] = i
print ''.join([o[d[c]] for c in encoded])
