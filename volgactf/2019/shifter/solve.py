#!/usr/bin/env python
from itertools import product
from Crypto.Util.number import long_to_bytes

def check(register, branches, bits):
    for b in bits:
        x = 0
        for i, v in enumerate(branches):
            x ^= register[i] & v
        if x != b:
            return False
        register = register[1:] + [x]
    return True

def str2bin(s):
    return [int(b) for b in bin(int(s.encode('hex'), 16))[2:]]

def xor(a, b):
    return map(lambda (x, y): x ^ y, zip(a, b))

def next_bits(register, branches):
    while True:
        yield register[0]
        x = 0
        for i, v in enumerate(branches):
            x ^= register[i] & v
        register = register[1:] + [x]

enc = str2bin(open('encrypted.txt').read().decode('base64'))
start = xor(str2bin('<!DOCTYPE '), enc)

for n in range(2, 17):
    register = start[:n]
    for branches in product([0, 1], repeat=n):
        if not check(register, branches, start[n:]):
            continue
        flag_bits = [c ^ b for c, b in zip(enc, next_bits(register, branches))]
        flag = long_to_bytes(int('0b' + ''.join(map(str, flag_bits)), 2))
        print flag
