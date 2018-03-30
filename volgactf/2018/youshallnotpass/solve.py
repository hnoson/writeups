#!/usr/bin/env python
from z3 import *
import commands
import re

def fcommon(a,b,op):
    code = '%s %s ' % (a,op)
    if b.find('[') != -1:
        if b.find('+') != -1:
            reg, offset = re.search('\[(.*)\+(.*)\]', b).groups()
            code += '%s[%d]' % (reg, int(offset,16) // 8)
        else:
            code += '%s[0]' % re.search('\[(.*)\]', b).group(1)
    else:
        code += b
    return code

def fmov(a,b):
    return fcommon(a,b,'=')

def fadd(a,b):
    return fcommon(a,b,'+=')

def fsub(a,b):
    return fcommon(a,b,'-=')

def fmul(a,b,c = None):
    if c is None:
        return fcommon(a,b,'*=')
    code = a + ' = '
    if b.find('[') != -1:
        if b.find('+') != -1:
            reg, offset = re.search('\[(.*)\+(.*)\]', b).groups()
            code += '%s[%d] * %s' % (reg, int(offset,16) // 8, c)
        else:
            code += '%s[0] * %s' % (re.search('\[(.*)\]', b).group(1), c)
    else:
        code += '%s * %s' % (b,c)
    return code

def flea(a,b):
    code = a + ' = ' + re.search('\[(.*)\]', b).group(1)
    return code

def fshl(a,b):
    return '%s = %s << %s' % (a,a,b)

def fneg(a):
    return '%s = -%s' % (a,a)

def fcmp(a,b):
    return '%s == %s' % (a,b)

def get_instructions():
    found = False
    blocks = []
    for line in commands.getoutput('objdump -d -M intel --no-show-raw-insn ysnp').split('\n'):
        if line.find('mov    rax,QWORD PTR [r14]') != -1:
            block = []
            found = True
        if found:
            block.append(line.split('\t')[-1])
        if found and line.find('cmp') != -1:
            blocks.append(block)
            found = False
    return blocks

def addconstraints(s):
    for i in range(length):
        s.add(X[i] >= 0x20, X[i] <= 0x7e)
    known = "VolgaCTF{"
    for i in range(len(known)):
        s.add(X[i] == ord(known[i]))
    s.add(X[length-1] == ord('}'))

    ops = {'mov': fmov, 'add': fadd, 'sub': fsub, 'imul': fmul, 'lea': flea, 'shl': fshl, 'neg': fneg, 'cmp': fcmp}
    blocks = get_instructions()
    r14 = [X]
    for block in blocks:
        for line in block:
            op, operand = re.search(r'([a-z]+) *(.+)',line).groups()
            operand = operand.split(',')
            code = ops[op](*operand)
            if op == 'cmp':
                s.add(eval(code))
            else:
                exec(code)

length = 45

X = [BitVec('x%d' % i,8) for i in range(length)]

s = Solver()
addconstraints(s)

flag = list('*' * length)
if s.check() == sat:
    m = s.model()
    for i in range(length):
        flag[i] = chr(m.evaluate(X[i]).as_long())
    print ''.join(flag)
