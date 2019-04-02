#!/usr/bin/env python
from pwn import *

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extgcd(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a / b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0, y0

def modinv(x, n):
    return extgcd(x, n)[0]

s = remote('lg.q.2019.volgactf.ru', 8801)

s.recvline()
s.recvline()

nums = [int(s.recvline(False)) for _ in range(7)]
diffs = map(lambda a, b: a - b, nums[:-1], nums[1:])
n = reduce(gcd, [abs(diffs[i] * diffs[i+3] - diffs[i+1] * diffs[i+2]) for i in range(len(diffs) - 3)])
m = diffs[1] * modinv(diffs[0], n) % n
c = (nums[1] - nums[0] * m) % n
pred = (nums[-1] * m + c) % n
s.sendline(str(pred))
s.interactive()
