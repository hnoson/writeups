#!/usr/bin/env python
from pwn import *
from Crypto.Util.number import *

s = remote('rsacalc.quals.beginners.seccon.jp', 10001)

s.recvuntil('N: ')
N = int(s.recvline(False))

def sign(data):
    s.sendlineafter('> ', '1')
    s.sendlineafter('data> ', long_to_bytes(data))
    s.recvuntil('Signature: ')
    return int(s.recvline(False), 0x10)

def exc(data, sig):
    s.sendlineafter('> ', '2')
    s.sendlineafter('data> ', long_to_bytes(data))
    s.sendlineafter('signature> ', hex(sig))

def extgcd(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b > 0:
        a, b, q = b, a % b, a // b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0, y0

def modinv(x, n):
    return extgcd(x, n)[0]

M = bytes_to_long('1337,F')

sig = sign(M * 2) * modinv(sign(2), N) % N
exc(M, sig)
s.stream()
