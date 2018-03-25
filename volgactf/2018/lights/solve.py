#!/usr/bin/env python
import re
import sys

with open('trace.txt') as f:
    data = f.read()

a = {'25': '.', '75': '-'}
lst = map(lambda x: a[x], re.findall(r', ([1-9]{2})0000000',data))
for i in range(0,len(lst),2):
    sys.stdout.write(str(lst[i]))
    if i + 1 < len(lst) - 1 and lst[i + 1] == '-':
        sys.stdout.write(' ')
print ''
