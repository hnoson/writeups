#!/usr/bin/env python
from pwn import *

def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)

def extgcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0, y0

def smallest(x):
    n = 2
    while x % n > 0:
        n += 1
    return n

if __name__ == '__main__':
    if len(sys.argv) == 1:
        s = process(['python3', 'LCG.py'])
    else:
        s = remote('lcg.eatpwnnosleep.com', 12345)
    
    a = [0] * 32
    for i in range(8):
        s.sendline('1')
        a[i] = int(s.recvline(False))

    d = 0xdeadbeef
    b = [0] * 6
    for i in range(6):
        b[i] = a[i + 2] - a[i + 1] + d * (a[i + 1] - a[i])
    c = [0] * 4
    for i in range(4):
        c[i] = b[i + 1] * b[i + 1] - b[i] * b[i + 2]
        c[i] = c[i] if c[i] > 0 else -c[i]
    m = reduce(gcd, c, c[0])
    while m > 1 << 64:
        m //= smallest(m)
    k = -1
    for i in range(5):
        if gcd(b[i], m) == 1:
            u, v = extgcd(b[i], m)
            k = u * b[i + 1] % m
            break
    if k == -1:
        exit(0)
    x = (k - d) % m
    y = k * d % m
    z = (a[2] - x * a[1] - y * a[0]) % m
    for i in range(8, 32):
        a[i] = (x * a[i - 1] + y * a[i - 2] + z) % m
        s.sendline(str(a[i]))
    s.stream()
