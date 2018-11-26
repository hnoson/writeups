#!/usr/bin/env python
from pwn import *
from Crypto.Util.number import *
from itertools import product
import gmpy
import hashlib
import string
import math

def encrypt(m, pubkey):
    m = bytes_to_long(m)
    e, n = pubkey
    assert m < n
    while True:
        r = random.randint(1, n - 1)
        if gcd(r, n) == 1:
            c = (pow(r, e, n**2) * (r**2 + m*n)) % n ** 2
            break
    return c

def makekey(nbit):
    D = getRandomRange(1, nbit**3)
    p = gmpy.next_prime(fprime + D)
    q = getPrime(nbit)
    pubkey = (0x10001, int(p*q))
    return pubkey

def auth(s):
    s.recvuntil('such that ')
    hashtype = s.recvuntil('(X)[-6:] = ')[:-11]
    chal = s.recvline(False)
    print hashtype, chal
    for length in range(1, 10):
        for x in product(string.digits + string.letters, repeat=length):
            x = ''.join(x)
            m = hashlib.new(hashtype)
            m.update(x)
            if m.hexdigest()[-6:] == chal:
                print x
                s.sendline(x)
                return

def get_info(s):
    s.sendline('P')
    s.recvuntil('pubkey = ')
    e, n = eval(s.recvline(False))
    s.sendline('C')
    s.recvuntil('enc = ')
    enc = int(s.recvline(False))
    return e, n, enc

def main():
    ns = []
    while True:
        print len(ns)
        s = remote('37.139.4.247', 36032)
        auth(s)
        e, n, enc = get_info(s)
        p = 1
        for x in ns:
            p = gmpy.gcd(n, x)
            if p != 1:
                q = n // p
                break
        if p != 1:
            break
        ns.append(n)
        s.close()
    assert p * q == n
    print 'p =', p
    print 'q =', q
    print 'n =', n
    print 'enc =', enc
    totient = (p - 1) * (q - 1)
    r = pow(enc % n, gmpy.invert(2 * e, totient), n)
    m = ((enc * gmpy.invert(r ** e, n ** 2) % n ** 2) - r ** 2) % n ** 2 // n
    m = long_to_bytes(m)
    print m
    s.sendline('S')
    s.sendline(m)
    s.interactive()

main()
