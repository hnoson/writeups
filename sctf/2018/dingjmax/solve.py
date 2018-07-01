#!/usr/bin/env python
import sys

a = 0
b = 0
c = [i for i in range(0x40)]
d = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_!'

def combine(x, y):
    return d[(d.find(x) ^ d.find(y)) % 0x40]

def rnd(num):
    global a, b

    for i in range(num):
        a = (a + 1) % 0x40
        b = (c[a] + b) % 0x40
        c[a], c[b] = c[b], c[a]
    index = c[(c[a] + c[b]) % 0x40]
    return d[index]

if __name__ == '__main__':
    with open('./pattern', 'r') as f:
        pattern = f.read().split('\n')[:-1]

    flag = list('qN7BuRx4rElDv84dgNaaNBanZf0HSHFjqOvbkFfgTRg3r')

    for i in range(0xa514):
        num = (i * 0xcccccccccccccccd) >> 68
        if ((num << 2) + num) << 2 == i:
            pos = pattern[num].find('o')
            if pos >= 0:
                rnd(ord('dfjk'[pos]) * (i + 20 * 19))
                sys.stdout.write('\r[*] %#x' % (i + 20 * 19))
                sys.stdout.flush()
                for j, char in enumerate(flag):
                    flag[j] = combine(char, rnd(1))
    print '\nSCTF{%s}' % ''.join(flag)
