#!/usr/bin/env python
import struct

def p64(x):
    return struct.pack('<Q', x)

def u64(x):
    return struct.unpack('<Q', x.ljust(8, '\0'))[0]

diff = ''.join(map(lambda x: chr(int(x, 0x10)), '00 00 00 00 00 00 00 00 42 09 4a 49 35 43 0a 41 f0 19 e6 0b f5 f2 0e 0b 2b 28 35 4a 06 3a 0a 4f 00 00 00 00 00 00 00 00'.split(' ')))
censored = 'zer0pts{********CENSORED********}'
flag = ''
for i in range(0, len(censored) + 7, 8):
    flag += p64(u64(censored[i:i+8]) + u64(diff[i:i+8]))
print flag
