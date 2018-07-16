#!/usr/bin/env python
from pwn import *
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

def cbrt(x):
    l = 1
    r = 2 ** 1024
    while l + 1 < r:
        m = (l + r) // 2
        if m ** 3 <= x:
            l = m
        else:
            r = m
    return l

if __name__ == '__main__':
    s = remote('178.128.17.82', 31333)

    s.sendlineafter('3. Get flag\n', '2')
    pubkey = RSA.importKey(s.recvuntil('-----END PUBLIC KEY-----'))
    template = 'Your OTP for transaction #731337 in ABCXYZ Bank is %04dxxxxx.'
    s.sendlineafter('3. Get flag\n', '3')
    s.recvuntil('encrypted dat: ')
    enc = bytes_to_long(s.recvline(False).decode('hex'))
    for i in range(10000):
        num = (bytes_to_long(template % i) ** pubkey.e) // pubkey.n
        otp = long_to_bytes(cbrt(enc + num * pubkey.n))
        if otp.endswith('.') and otp[-10:-1].isdigit():
            s.sendline(otp[-10:-1])
            s.recvuntil('>>> ')
            print s.recvline(False)
            exit(0)
