#!/usr/bin/env python
import struct

enc = ''.join(map(lambda x: chr(int(x, 0x10)), '38 01 40 1a 00 00 00 00 67 b8 9a 27 00 00 00 00 69 29 7d 17 00 00 00 00 f5 46 6e 0e 00 00 00 00 f8 21 26 51 00 00 00 00 73 ce 96 2e 00 00 00 00 96 b4 84 04 00 00 00 00 6e 4f 41 73 00 00 00 00 96 b4 84 04 00 00 00 00 e9 74 c2 01 00 00 00 00 96 b4 84 04 00 00 00 00 62 c7 7d 63 00 00 00 00 4a 7a 14 15 00 00 00 00 5e 89 e9 1f 00 00 00 00 5e 89 e9 1f 00 00 00 00 eb 01 2b 86 00 00 00 00 cd 06 5a 77 00 00 00 00 f5 46 6e 0e 00 00 00 00 f5 46 6e 0e 00 00 00 00 66 24 6a 3e 00 00 00 00 6d ab 00 03 00 00 00 00 12 cc 67 5a 00 00 00 00 01 7e 16 34 00 00 00 00 eb 01 2b 86 00 00 00 00 6d ab 00 03 00 00 00 00 96 b4 84 04 00 00 00 00 eb 01 2b 86 00 00 00 00 6d ab 00 03 00 00 00 00 4d da ef 11 00 00 00 00 f8 21 26 51 00 00 00 00 f5 46 6e 0e 00 00 00 00 69 29 7d 17 00 00 00 00 73 ce 96 2e 00 00 00 00 4a 7a 14 15 00 00 00 00 12 cc 67 5a 00 00 00 00 73 ce 96 2e 00 00 00 00 4d 14 80 78 00 00 00 00 6b ed 69 5a 00 00 00 00'.split(' ')))

def u64(x):
    return struct.unpack('<Q', x)[0]

table = {}
for i in range(0x100):
    table[pow(i, 0x5beb, 0x8bae6fa3)] = chr(i)
flag = ''.join([table[u64(enc[i:i+8])] for i in range(0, len(enc), 8)])
print flag