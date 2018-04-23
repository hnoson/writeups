#!/usr/bin/env python
from pwn import *

def query(l,r):
    global count
    count += 1
    s.sendline('? %d %d' % (l,r))
    return int(s.recvline(False))

def dfs(l,r,n):
    ret = []
    x = query(l,(l+r)//2)
    if x:
        if (l+r)//2 - l == 1:
            ret += [l] * x
        else:
            ret += dfs(l,(l+r)//2,x)
    if x == n:
        return ret
    if r - (l+r)//2 == 1:
        ret += [(l+r)//2] * (n - x)
    else:
        ret += dfs((l+r)//2,r,n-x)
    return ret

if __name__ == '__main__':
    s = remote('47.89.18.224',10011)

    for i in range(10):
        count = 0
        s.recvuntil('n = ')
        n = int(s.recvline(False))
        log.info('Level %d: n = %d' % (i,n))
        ans = dfs(0,1024,n)
        s.sendline('! ' + ' '.join(map(str,ans)))
        log.info('Answer: ' + ' '.join(map(str,ans)))
        log.info('Count: %d' % count)
    s.stream()
