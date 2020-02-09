#!/usr/bin/env python

xs = [0] * (10 ** 7 + 1)
with open('./Given_File.txt') as f:
    for line in f:
        a, b, c = map(int, line.split(' '))
        a -= 1
        b -= 1
        xs[a] = (xs[a] + c) % 10
        xs[b] = (xs[b] - c) % 10
for i in range(len(xs)-1):
    xs[i+1] = (xs[i+1] + xs[i]) % 10
result = 1
for i in range(len(xs)-1):
    if xs[i] != 0:
        result = (result * xs[i]) % 999999937
print result
