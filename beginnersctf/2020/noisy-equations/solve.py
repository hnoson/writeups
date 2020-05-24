#!/usr/bin/env python
from pwn import *
import numpy as np

s = remote('noisy-equations.quals.beginners.seccon.jp', 3000)

coeffs1 = np.mat(eval(s.recvline(False)), dtype='float')
answers1 = np.array(eval(s.recvline(False)))

s = remote('noisy-equations.quals.beginners.seccon.jp', 3000)

coeffs2 = np.mat(eval(s.recvline(False)), dtype='float')
answers2 = np.array(eval(s.recvline(False)))

print ''.join([chr(int(round(x))) for x in np.dot(np.asarray(np.linalg.inv(coeffs1 - coeffs2)), answers1 - answers2)])
