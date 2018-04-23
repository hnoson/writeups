#!/usr/bin/env python
from pwn import *
from hashlib import sha256
import re
import itertools
import string
import chess.uci
import random
import copy

def proofofwork():
    fol, chal = re.match(r'.*xxxx.(\w*).*==(\w*)', s.recvline(False)).groups()
    for x in itertools.product(string.letters + string.digits, repeat = 4):
        xxxx = ''.join(x)
        sha = sha256()
        sha.update(xxxx + fol)
        if sha.hexdigest() == chal:
            s.sendline(xxxx)
            return
    print 'Not found'
    exit(-1)

def extract_move(prev,now):
    for i in range(8):
        for j in range(8):
            if prev[i][j] != now[i][j]:
                if now[i][j] == '.':
                    fr = chr(ord('a') + j) + chr(ord('8') - i)
                else:
                    to = chr(ord('a') + j) + chr(ord('8') - i)
    return chess.Move.from_uci(fr + to)

def move(board,uci):
    fj = ord(uci[0]) - ord('a')
    fi = ord('8') - ord(uci[1])
    tj = ord(uci[2]) - ord('a')
    ti = ord('8') - ord(uci[3])
    board[ti][tj] = board[fi][fj]
    board[fi][fj] = '.'

def print_board(board):
    for i in range(8):
        for j in range(8):
            sys.stdout.write(board[i][j] + ' ')
        print ''

if __name__ == '__main__':
    context.log_level = 'DEBUG'
    s = remote('47.89.11.82', 10012)
    proofofwork()
    engine = chess.uci.popen_engine('stockfish')
    info_handler = chess.uci.InfoHandler()
    engine.info_handlers.append(info_handler)
    for g in range(20):
        prev = None
        print s.recvuntil('game starts\n')
        log.info('Game %d:' % g)
        board = chess.Board()
        while True:
            line = s.recvline(False)
            if line == 'ilegal move':
                board.pop()
            elif line == 'you win':
                break
            else:
                now = [line.split(' ')] + [s.recvline(False).split(' ') for i in range(7)]
                # print_board(now)
                if prev is not None:
                    board.push(extract_move(prev,now))
            prev = copy.deepcopy(now)
            engine.position(board)
            bestmove, ponder = engine.go(movetime=4000)
            print info_handler.info['score'][1]
            if bestmove is None:
                legal_moves = list(board.legal_moves)
                print legal_moves
                bestmove = legal_moves[random.randint(0,len(legal_moves)-1)]
            s.sendlineafter('input your move(like e2e4):\n',bestmove.uci())
            move(prev,bestmove.uci())
            board.push(bestmove)
            print_board(prev)
        log.info('Win')
    s.stream()
