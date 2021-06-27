#!/usr/bin/env python3
from pwn import *
import base64

s = remote('babank.2021.ctfz.one', 1337)

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def makeMAC(data):
    s.sendlineafter('>', f'authenticate_command {base64.b64encode(data).decode()}')
    s.recvuntil('MAC: ')
    return bytes.fromhex(s.recvline(False).decode())

def exec_command(command, tag):
    s.sendlineafter('>', f'execute_command {base64.b64encode(command).decode()} {tag.hex()}')

command1 = b't{from:"me",to:"admin",amount:"1",comment:""}'
command1 = command1[:-2] + b'A' * (0x10 - len(command1) % 0x10) + command1[-2:]
mac1 = makeMAC(command1)

command2 = b't{from:"admin",to:"me",amount:"1000",comment:""}'
command2 = command2[:-2] + b'A' * (0x10 - len(command2) % 0x10) + command2[-2:]
mac2 = b'\0' * 0x10
for i in range(0, len(command2), 0x10):
    mac2 = makeMAC(command1 + xor(mac1, xor(command2[i:i+0x10], mac2)))

exec_command(command2, mac2)
s.stream()
