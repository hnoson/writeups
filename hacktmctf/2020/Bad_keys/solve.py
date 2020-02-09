#!/usr/bin/env python
from pwn import *
from Crypto.Util.number import *
import gmpy2
import random

e, N = eval(open('./RSA_PUB').read())
c = eval(open('./flag.enc').read())

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def egcd(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def factorN(n, e, d):
    k = abs(e * d - 1)
    t = 0
    while k % 2 == 0:
        k //= 2
        t += 1
    for i in range(100):
        g = random.randint(2, n - 1)
        x = pow(g, k, n)
        for j in range(t-1):
            y = pow(x, 2, n)
            if y == 1:
                p = gcd(x - 1, n)
                q = n // p
                return (p, q)
            elif y == n - 1:
                break
    assert False

def prev_prime(x):
    x -= 1
    while not gmpy2.is_prime(x):
        x -= 1
    return x

s = remote('138.68.67.161', 60005)
s.sendlineafter('>', 'k')
s.recvuntil('n ))\n')
(_, _), (d, n) = eval(s.recvline())
p, q = factorN(n, e, d)
if not str(p).startswith('121177'):
    p = q
assert str(p).startswith('121177')
# p = 12117717634661447128647943483912040772241097914126380240028878917605920543320951000813217299678214801720664141663955381289172887935222185768875580129863163
for i in range(100000):
    if N % p == 0:
        print p
        break
    p = prev_prime(p)

q = N // p
assert p * q == N
phi = (p - 1) * (q - 1)
d = egcd(e, phi)[1] % phi
print long_to_bytes(pow(c, d, N))
