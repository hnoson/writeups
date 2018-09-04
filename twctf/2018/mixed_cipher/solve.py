#!/usr/bin/env python
from pwn import *
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
import string
import random

class MT19937:
    n, w, m, r= 624, 32, 397, 31
    a = 0x9908b0df
    mask = (1 << r) - 1
    f = 1812433253
    u, d = 11, 0xffffffff
    s, b = 7, 0x9d2c5680
    t, c = 15, 0xefc60000
    l = 18
    index = 0

    def __init__(self, seed=0):
        self.index = self.n
        self.mt = [0] * self.n
        self.mt[0] = seed
        for i in range(1, self.n):
            self.mt[i] = (self.f * (self.mt[i-1] ^ (self.mt[i-1] >> self.w - 2)) + i) & ((1 << self.w) - 1)

    def random(self):
        if self.index == self.n:
            self.index = 0
            for i in range(self.n):
                x = (self.mt[i] & ~self.mask) + (self.mt[(i + 1) % self.n] & self.mask)
                z = x >> 1
                if x % 2 == 1:
                    z = z ^ self.a
                self.mt[i] = self.mt[(i + self.m) % self.n] ^ z
        y = self.mt[self.index]
        y ^= y >> self.u & self.d
        y ^= y << self.s & self.b
        y ^= y << self.t & self.c
        y ^= y >> self.l
        self.index += 1
        return y

class MT19937Predictor(MT19937):
    def __init__(self):
        self.index = 0
        self.mt = [0] * self.n

    def setint32(self, y):
        def bits(a, b):
            return (1 << b) - (1 << a)

        def reverse_lshift(y, b, m):
            for i in range(b, self.w, b):
                y ^= (y << b & m) & bits(i, i + b)
            return y

        def reverse_rshift(y, b, m):
            for i in range(b, self.w, b):
                y ^= (y >> b & m) & bits(max(0, self.w - (i + b)), self.w - i)
            return y

        y = reverse_rshift(y, self.l, bits(0, self.w))
        y = reverse_lshift(y, self.t, self.c)
        y = reverse_lshift(y, self.s, self.b)
        y = reverse_rshift(y, self.u, self.d)
        self.mt[self.index] = y
        self.index += 1

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def encrypt(data):
    s.sendlineafter('key\n', '1')
    s.sendlineafter('text: ', data)
    s.recvuntil('RSA: ')
    rsa = bytes_to_long(s.recvline(False).decode('hex'))
    s.recvuntil('AES: ')
    aes = s.recvline(False).decode('hex')
    return rsa, aes

def decrypt(data):
    s.sendlineafter('key\n', '2')
    s.sendlineafter('text: ', long_to_bytes(data).encode('hex'))
    s.recvuntil('RSA: ')
    return bytes_to_long(s.recvline(False).decode('hex')) & 0xff

def get_flag():
    s.sendlineafter('key\n', '3')
    s.recvuntil('coming!\n')
    return s.recvline(False).decode('hex')[0x10:]

def get_key():
    s.sendlineafter('key\n', '4')
    s.recvuntil(':)\n')
    return bytes_to_long(s.recvline(False).decode('hex'))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        s = process('./server.py')
    else:
        s = remote('crypto.chal.ctf.westerns.tokyo', 5643)

    e = 65537
    n = bytes_to_long('A') ** e - encrypt('A')[0]
    for i in range(7):
        n = gcd(n, bytes_to_long(str(i)) ** e - encrypt(str(i))[0])

    encrypted_key = get_key()
    first_byte = decrypt(encrypted_key)
    l = 0
    r = n
    while l + 1 < r:
        m = (l + r) // 2
        encrypted_key *= 2 ** e
        encrypted_key %= n
        if decrypt(encrypted_key) & 1:
            l = m
        else:
            r = m
    key = long_to_bytes((r & ~0xff) | first_byte)

    predictor = MT19937Predictor()
    for i in range(624 // 4):
        iv = bytes_to_long(encrypt('A')[1][:16])
        for i in range(4):
            predictor.setint32(iv & 0xffffffff)
            iv >>= 32

    encrypted_flag = get_flag()
    iv = ''.join(reversed([long_to_bytes(predictor.random()) for i in range(4)]))
    aes = AES.new(key, AES.MODE_CBC, iv)
    m = aes.decrypt(encrypted_flag)
    print m[:-ord(m[-1])]
