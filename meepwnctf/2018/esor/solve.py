#!/usr/bin/env python
from pwn import *
from Crypto.Cipher import AES

if __name__ == '__main__':
    if len(sys.argv) == 1:
        s = process('./testpoodle_bf32226e5cec38a544501e160724e3f7.py')
    else:
        s = remote('206.189.92.209', 12345)

    s.sendlineafter('3. quit\n', '1')
    s.sendlineafter('prefix: ', '')
    s.sendlineafter('suffix: ', '')
    enc = s.recvline(False).decode('hex')
    iv = enc[:16]
    enc = enc[16:]
    key = '\xff' * 32
    aes = AES.new(key, AES.MODE_CBC, iv)
    print aes.decrypt(enc)
