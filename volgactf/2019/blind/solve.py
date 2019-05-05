#!/usr/bin/env python
from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

n = 26507591511689883990023896389022361811173033984051016489514421457013639621509962613332324662222154683066173937658495362448733162728817642341239457485221865493926211958117034923747221236176204216845182311004742474549095130306550623190917480615151093941494688906907516349433681015204941620716162038586590895058816430264415335805881575305773073358135217732591500750773744464142282514963376379623449776844046465746330691788777566563856886778143019387464133144867446731438967247646981498812182658347753229511846953659235528803754112114516623201792727787856347729085966824435377279429992530935232902223909659507613583396967

def sign(cmd):
    s.sendlineafter('command:\r\n', 'a sign')
    s.sendlineafter('sign:\r\n', cmd.encode('base64')[:-1])
    return int(s.recvline(False))

def cat(signature, filename):
    s.sendlineafter('command:\r\n', '%s cat %s' % (str(signature), filename))
    return s.recvline(False)

def find_factor(x):
    i = 2
    while i * i <= x:
        if x % i == 0:
            return i
        i += 1
    exit(0)

s = remote('blind.q.2019.volgactf.ru', 7070)

filename = 'flag'
x = bytes_to_long(('cat %s' % filename))
z = find_factor(x / find_factor(x))
x /= z
sx = sign(long_to_bytes(x))
sz = sign(long_to_bytes(z))
print cat(sx * sz % n, filename)