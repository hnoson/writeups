#!/usr/bin/env python3
import pickle
import hashlib

from copy import deepcopy

class Key:
    PRIVATE_INFO = ['P', 'Q', 'D', 'DmP1', 'DmQ1']
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            assert self.bits % 8 == 0

    def ispub(self):
        return all(not hasattr(self, key) for key in self.PRIVATE_INFO)

    def ispriv(self):
        return all(hasattr(self, key) for key in self.PRIVATE_INFO)

    def pub(self):
        p = deepcopy(self)
        for key in self.PRIVATE_INFO:
            if hasattr(p, key):
                delattr(p, key)
        return p

    def priv(self):
        raise NotImplementedError()

def egcd(a1, a2):
    x1, x2 = 1, 0
    y1, y2 = 0, 1
    while a2:
        q = a1 // a2
        a1, a2 = a2, a1 - q * a2
        x1, x2 = x2, x1 - q * x2
        y1, y2 = y2, y1 - q * y2
    return (x1, y1, a1)

def bytes2num(data):
    return sum(x << (8 * i) for i, x in enumerate(data))

def num2bytes(data, size):
    assert 0 <= data and (data >> (size * 8)) == 0
    return bytes(data >> (8 * i) & 0xff for i in range(size))

def xor(d1, d2):
    return bytes(
        d1[i % len(d1)] ^ d2[i % len(d2)]
        for i in range(max(len(d1), len(d2)))
    )


def random_oracle(source, length, hash=hashlib.sha256):
    return b''.join(
        hash(source + num2bytes(idx, 4)).digest()
        for idx in range((length - 1) // hash().digest_size + 1)
    )[:length]

def unpad(data, hash=hashlib.sha256):
    if data[-1] != 0: return None
    data = data[:-1]

    k = hash().digest_size
    Xlen = len(data) - k
    X, Y = data[:Xlen], data[-k:]
    Y = xor(Y, random_oracle(X, k, hash))
    X = xor(X, random_oracle(Y, Xlen, hash))
    if all(b == 0 for b in X[-k:]):
        return X[:-k]
    return None

def decrypt(key, data):
    assert key.ispriv() and len(data) * 8 == key.bits
    data = bytes2num(data)
    assert 0 <= data and data < key.N
    v1 = pow(data, key.DmP1, key.P)
    v2 = pow(data, key.DmQ1, key.Q)
    data = (v2 * key.P * key.iPmQ + v1 * key.Q * key.iQmP) % key.N
    return unpad(num2bytes(data, key.bits // 8))

def isqrt(x):
    l, r = 0, x
    while l + 1 < r:
        m = (l + r) // 2
        if m * m <= x:
            l = m
        else:
            r = m
    return l

key = pickle.load(open('key.sad.pub', 'rb'))
b = 1 + key.N
key.P = (b - isqrt(b * b - 4 * key.N * key.iPmQ * key.iQmP)) // (2 * key.iPmQ)
key.Q = key.N // key.P

d = egcd(key.E, (key.P - 1) * (key.Q - 1))[0]
key.DmP1 = d % (key.P - 1)
key.DmQ1 = d % (key.Q - 1)
key.D = d % ((key.P - 1) * (key.Q - 1))

print(decrypt(key, open('flag.enc', 'rb').read()))
