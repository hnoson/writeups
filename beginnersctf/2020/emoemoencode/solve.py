#!/usr/bin/env python
import struct
from hexdump import hexdump

print ''.join(open('./emoemoencode.txt').read().decode('utf-8').encode('utf-16le')[2::4])
