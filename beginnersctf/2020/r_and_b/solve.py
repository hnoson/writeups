#!/usr/bin/env python

enc = open('./encoded_flag').read()

def rot13(s):
    ret = ''
    for c in s:
        if 'A' <= c and c <= 'Z':
            ret += chr((ord(c) - ord('A') + 13) % 26 + ord('A'))
        elif 'a' <= c and c <= 'z':
            ret += chr((ord(c) - ord('a') + 13) % 26 + ord('a'))
        else:
            ret += c
    return ret

while True:
    if enc[0] == 'R':
        enc = rot13(enc[1:])
    elif enc[0] == 'B':
        enc = enc[1:].decode('base64')
    else:
        break
print enc
