#!/usr/bin/env python
from Crypto.Util.number import long_to_bytes

lol = lambda x, l, b: (x >> (b-l)) | ((x & ((1<<(b-l))-1)) << l)

flag = 0
for i, line in enumerate(open('./chall.txt')):
    flag |= (int(line) & 1) << i
print long_to_bytes(flag)
