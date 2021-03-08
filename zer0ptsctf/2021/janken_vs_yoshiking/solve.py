#!/usr/bin/env python
from pwn import *

if len(sys.argv) == 1:
    s = process('python -u server.py', shell=True)
else:
    s = remote('crypto.ctf.zer0pts.com', 10463)

s.recvuntil('g: ')
g = int(s.recvuntil(',')[:-1])
s.recvuntil('p: ')
p = int(s.recvline(False))

n = p - 1
for i in range(2, 0x10000):
    if (p - 1) % i == 0:
        if pow(g, i, p) == 1:
            n = min(n, i)
        elif pow(g, (p - 1) // i, p) == 1:
            n = min(n, (p - 1) // i)
assert n < p - 1
assert pow(2, n, p) != 1
assert pow(3, n, p) != 1

for _ in range(100):
    s.recvuntil('commitment is=')
    _, c2 = eval(s.recvline(False))
    m_n = pow(c2, n, p)
    if m_n == 1:
        hand = 3
    elif pow(2, n, p) == m_n:
        hand = 1
    else:
        hand = 2
    s.sendlineafter('your hand(1-3): ', str(hand))
s.stream()
