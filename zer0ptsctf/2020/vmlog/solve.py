#!/usr/bin/env python
from pwn import *
import string

expected = open('./log.txt').read()
log = ''
flag = ''
while expected != log:
    for c in string.letters + string.digits + string.punctuation:
        s = process('python3 vm.py', shell=True)
        s.send(flag + c)
        time.sleep(0.2)
        log = s.recv()
        s.close()
        if expected.startswith(log):
            print log
            flag += c
            print flag
            break
print flag
