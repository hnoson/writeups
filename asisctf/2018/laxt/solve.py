#!/usr/bin/env python
from pwn import *
from itertools import combinations_with_replacement, permutations
import hashlib
import string

s = remote('37.139.4.247', 19153)

s.recvuntil('such that ')
hashtype = s.recvuntil('(X)[-6:] = ')[:-11]
chal = s.recvline(False)
print hashtype, chal
for x in combinations_with_replacement(string.letters + string.digits, 8):
    x = ''.join(x)
    m = hashlib.new(hashtype)
    m.update(x)
    if m.hexdigest()[-6:] == chal:
        print x
        s.sendline(x)
        break

s.sendline('C')
s.recvuntil('n = ')
n = s.recvline(False)
print n
table = [''] * 101
for x in range(7): # 0: 1234, 1: 1(23)4, 2: (12)34, 3:12(34), 4: (12)(34), 5: 1(234), 6: (123)4
    for digits in permutations(n):
        for ops in combinations_with_replacement(list('%&*+-/^|') + ['', '**', '<<', '>>'], 3):
            if ops.count('**') > 1:
                continue
            for tilde in combinations_with_replacement(['', '~'], 4):
                exp = ''
                if x in [2, 4, 6]:
                    exp += '('
                exp += tilde[0] + digits[0]
                if x in [1, 5]:
                    exp += ops[0] if ops[0] != '' else '*'
                    exp += '('
                else:
                    exp += ops[0]
                exp += tilde[1] + digits[1]
                if x in [2, 3, 4]:
                    if x != 3:
                        exp += ')'
                    exp += ops[1] if ops[1] != '' else '*'
                    if x != 2:
                        exp += '('
                else:
                    exp += ops[1]
                exp += tilde[2] + digits[2]
                if x in [1, 6]:
                    exp += ')'
                    exp += ops[2] if ops[2] != '' else '*'
                else:
                    exp += ops[2]
                exp += tilde[3] + digits[3]
                if x in [3, 4, 5]:
                    exp += ')'
                try:
                    val = eval(exp)
                    if int(val) == val and val >= 0 and val <= 100 and table[val] == '':
                        table[val] = exp
                except Exception:
                    pass

for i in range(101):
    if table[i] == '':
        exit(0)

print table
for i in range(101):
    s.sendlineafter('%d\n' % i, table[i])
s.interactive()
