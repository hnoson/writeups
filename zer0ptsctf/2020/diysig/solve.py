#!/usr/bin/env python
from pwn import *
from Crypto.Util.number import long_to_bytes

with open('./chall.txt') as f:
    enc = int(f.readline()[6:], 0x10)
    sig = int(f.readline()[6:], 0x10)

def pubkey():
    s = remote('18.179.178.246', 3001)
    s.sendlineafter('> ', '3')
    s.recvuntil('N := ')
    n = int(s.recvline(False), 0x10)
    s.recvuntil('E := ')
    e = int(s.recvline(False), 0x10)
    s.close()
    return n, e

def verify(enc):
    s = remote('18.179.178.246', 3001)
    s.sendlineafter('> ', '2')
    s.sendlineafter('ENC : ', hex(enc)[2:])
    s.sendlineafter('SIG : ', '00')
    s.recvuntil('!= ')
    ret = int(s.recvline(False), 0x10)
    s.close()
    return ret

n, e = pubkey()

l, r = 0, n
while l + 1 < r:
    enc = enc * pow(2, e) % n
    m = (l + r) // 2
    if verify(enc) % 2 == 1:
        l = m
    else:
        r = m
print long_to_bytes(l)
