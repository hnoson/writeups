#!/usr/bin/env sage
from sage.crypto.util import bin_to_ascii

with open('./pubkey.txt') as f:
    bs = eval(f.read())
with open('./ciphertext.txt') as f:
    c = int(f.read())

n = len(bs)
M = Matrix(QQ, n+1)
for i in range(n):
    M[i,i] = 1
    M[i,-1] = bs[i]
    M[-1,i] = 1/2
M[-1,-1] = c

B = M.LLL()

for i in range(n+1):
    if all(map(lambda x: x in [-1/2, 1/2], B[i][:-1])) and B[i][-1] == 0:
        print bin_to_ascii([1/2-B[i][j] for j in range(n)][::-1])
        break
