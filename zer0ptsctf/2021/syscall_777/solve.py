#!/usr/bin/env python
from z3 import *
from Crypto.Util.number import long_to_bytes

table = [
    [4127179254, 4126139894, 665780030, 666819390],
    [1933881070, 2002783966, 1601724370, 1532821474],
    [4255576062, 3116543486, 3151668710, 4290701286],
    [1670347938, 4056898606, 2583645294, 197094626],
    [2720551936, 1627051272, 1627379644, 2720880308],
    [2307981054, 3415533530, 3281895882, 2174343406],
    [2673307092, 251771212, 251771212, 2673307092],
    [4139379682, 3602496994, 3606265306, 4143147994],
    [4192373742, 4088827598, 3015552726, 3119098870],
    [530288564, 530288564, 3917315412, 3917315412],
    [4025255646, 2813168974, 614968622, 1827055294],
    [3747612986, 1340672294, 1301225350, 3708166042],
    [3098492862, 3064954302, 3086875838, 3120414398],
    [2130820044, 2115580844, 2130523044, 2145762244]
]

flag = [BitVec('flag%d' % i, 32) for i in range(0xe)]

s = Solver()

s.add(
    flag[0] == 0x3072657a,
    flag[1] == 0x7b737470
)
for i in range(0xe):
    for j in range(4):
        s.add((flag[i] >> (j*8)) & 0xff < 128)

mem = [0] * 12
for i in range(0xe):
    mem[0] = flag[i]
    mem[1] = flag[(i + 1) % 0xe] ^ mem[0]
    mem[2] = flag[(i + 2) % 0xe] ^ mem[1]
    mem[3] = flag[(i + 3) % 0xe] ^ mem[2]
    mem[4] = mem[0] + mem[1] + mem[2] + mem[3]
    mem[5] = mem[0] - mem[1] + mem[2] - mem[3]
    mem[6] = mem[0] + mem[1] - mem[2] - mem[3]
    mem[7] = mem[0] - mem[1] - mem[2] + mem[3]
    mem[8] = (mem[4] | mem[5]) ^ (mem[6] & mem[7])
    mem[9] = (mem[5] | mem[6]) ^ (mem[7] & mem[4])
    mem[10] = (mem[6] | mem[7]) ^ (mem[4] & mem[5])
    mem[11] = (mem[7] | mem[4]) ^ (mem[5] & mem[6])

    s.add(Or(
        [And([mem[j+8] == table[i][j] for j in range(4)]) for i in range(14)]
    ))

if s.check() == sat:
    m = s.model()
    fs = map(lambda x: m.evaluate(x).as_long(), flag)
    flag = 0
    for f in fs[::-1]:
        flag = (flag << 32) + f
    print(long_to_bytes(flag)[::-1])
