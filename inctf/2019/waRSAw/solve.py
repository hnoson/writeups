#!/usr/bin/env python
from pwn import *
from Crypto.Util.number import *

def decrypt(c):
    s.sendlineafter('choice: ', '2')
    s.sendlineafter('(in hex): ', long_to_bytes(c).encode('hex'))
    s.recvuntil('(in hex):  ')
    return bytes_to_long(s.recvline(False).decode('hex'))

e = 65537

l, r = 0, 1 << 1024
while l + 1 < r:
    if len(sys.argv) == 1:
        s = process('python encrypt.py', shell=True)
    else:
        s = remote('18.217.237.201', 3197)

    s.recvuntil('(in hex):  ')
    c = bytes_to_long(s.recvline(False).decode('hex'))
    s.recvuntil('modulus:  ')
    n = int(s.recvline(False))
    
    x = 2
    m = n // x
    while m < l or r < m:
        x *= 2
        if m < l:
            m += n // x
        else:
            m -= n // x

    if decrypt(c * pow(x, e, n) % n) == 1:
        l = m
    else:
        r = m
    print l
    print r
    print long_to_bytes(l)
    s.close()

if len(sys.argv) == 1:
    s = process('python encrypt.py', shell=True)
else:
    s = remote('18.217.237.201', 3197)

s.recvuntil('(in hex):  ')
c = bytes_to_long(s.recvline(False).decode('hex'))
s.recvuntil('modulus:  ')
n = int(s.recvline(False))

for i in range(l - 0x10000, l + 0x10000):
    if pow(i, e, n) == c:
        print long_to_bytes(i)
        break
