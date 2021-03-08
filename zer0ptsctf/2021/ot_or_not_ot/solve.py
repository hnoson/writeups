#!/usr/bin/env python
from pwn import *
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes, bytes_to_long

if len(sys.argv) == 1:
    s = process('python -u server.py', shell=True)
else:
    s = remote('crypto.ctf.zer0pts.com', 10130)

s.recvuntil('flag: ')
enc = b64decode(s.recvline(False))
iv = enc[:0x10]
c = enc[0x10:]
s.recvuntil('p = ')
p = int(s.recvline(False))
s.recvuntil(' = ')
length = int(s.recvline(False))

key = ''
for _ in range((length + 1) // 2):
    s.recvuntil('t = ')
    t = int(s.recvline(False))

    s.sendlineafter('a = ', '18')
    s.sendlineafter('b = ', str(pow(2, p - 2, p)))
    s.sendlineafter('c = ', str(t))
    s.sendlineafter('d = ', '3')
    
    s.recvuntil('x = ')
    x = int(s.recvline(False))
    s.recvuntil('y = ')
    y = int(s.recvline(False))
    s.recvuntil('z = ')
    z = int(s.recvline(False))

    for i in range(2):
        for j in range(2):
            if ((x ^ i) * (y ^ j) - z ** 2) % p == 0:
                key = str(i) + key
                key = str(j) + key
key = long_to_bytes(int(key, 2))

aes = AES.new(key, AES.MODE_CBC, iv)
print(aes.decrypt(c))
