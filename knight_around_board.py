#!/usr/bin/env python3

"""
A simple recursive program that finds one possible way for a knight
(a chess piece) to visit all the fields on a board, given its
starting position `start`.
"""

from math import ceil, log10

(rows, cols) = (5, 5)
start = (rows-1,cols-1)

board = [ [ 0 ] * cols for _ in range(rows) ]
cnt = rows * cols

def one_move(pos=start, step=1):
    """
    Make one move from the given position `pos`.
    """
    board[pos[0]][pos[1]] = step
    if step == cnt:
        fmt = "{{:{}d}}".format(ceil(log10(rows*cols))+1)*cols
        for i in range(rows):
            print(fmt.format(*board[i]))
        return True
    step += 1
    for move in ((-1,2),(1,2),(-2,1),(2,1),(-1,-2),(1,-2),(-2,-1),(2,-1)):
        new_pos = tuple(p + m for p,m in zip(pos, move))
        if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and board[new_pos[0]][new_pos[1]] == 0:
            if one_move(new_pos, step):
                return True
    board[pos[0]][pos[1]] = 0
    return False

if not one_move():
    print("There is no solution!")
