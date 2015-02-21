#!/usr/bin/env python3

"""
A recursive solution to the Pardoner's Puzzle from
http://math-fail.com/2015/02/the-pardoners-puzzle.html

Copyright (c) Vedran Šego <vsego@vsego.org>
"""

import sys

n = 8
pos = (6, 2)  # starting position (col, row)
max_steps = 15
# The list of neighbour towns not directly connected
# Each connection is a set of neighbour tuples
no_connection = [ {(7,3),(7,4)} ]

# For testing
#n = 4
#pos = (0, 0)  # starting position (col, row)
#max_steps = 7
#no_connection = [ {(0,1),(0,2)} ]

# Remember all the coordinates, each associated with
# the step in which it is visited (zero == "not visited")
towns = { (i, j): 0 for i in range(n) for j in range(n) }
towns[pos] = 1
n2 = n*n

def towns_bad(towns, steps_left):
    """
    Returns `True` if a solution is obviously impossible, i.e.,
    1. if there are more zeros than can be visited no matter how are they arranged, or
    2. if the zeros are split into two unconnected regions.
    """
    chk = [ pos for pos, steps in towns.items() if steps == 0 ]
    # Are there too many zeros? (this could be computed directly)
    d = n
    max_possible = 0
    for k in range(steps_left+1):
        max_possible += d
        if k % 2 == 0:
            d -= 1
    if len(chk) > max_possible:
        return True
    # Are all the zeros connected?
    if not chk:
        return False
    removed = [ chk[0] ]
    del chk[0]
    while removed:
        pos = removed.pop()
        for i in range(-1, 2, 2):
            for neighbour in [ (pos[0]+i, pos[1]), (pos[0], pos[1]+i) ]:
                if neighbour in chk:
                    removed.append(neighbour)
                    chk.remove(neighbour)
    return bool(chk)

def try_dir(direction, pos, steps_left, towns, no_connection, visited):
    """
    Try visit all the fields going from the position `pos` in the direction `direction`.
    """
    org_pos = pos
    while True:
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if 0 <= new_pos[0] < n and 0 <= new_pos[1] < n and towns[new_pos] == 0:
            next_step = { pos, new_pos }
            if any( nc == next_step for nc in no_connection):
                break
            pos = new_pos
            visited += 1
            towns[pos] = visited
            if towns_bad(towns, steps_left):
                #print("Stopped with %d steps left." % steps_left)
                break
        else:
            break
    if pos != org_pos:
        #one_step(pos, steps_left, towns, no_connection, visited)
        while pos != org_pos:
            if pos in towns:
                one_step(pos, steps_left, towns, no_connection, visited, not_there=direction)
                towns[pos] = 0
                visited -= 1
            pos = (pos[0] - direction[0], pos[1] - direction[1])

def print_towns(towns):
    """
    Print the order in which the towns are visited.
    """
    for i in range(n):
        for j in range(n):
            print("{:3d}".format(towns[(i,j)]), end="")
        print()

def one_step(pos, steps_left, towns, no_connection, visited, not_there = None):
    """
    Try to visit all that you can, starting from the position `pos`
    in `steps_left` number of steps,
    skipping `no_connection` connections,
    except in the `not_there` or its opposite direction.
    """
    #print("\nSteps left: %d\n" % steps_left); print_towns(towns); print()
    if visited >= n2:
        print_towns(towns)
        sys.exit(0)
    if steps_left <= 0:
        #print_towns(towns); print()
        return
    steps_left -= 1
    if not_there is None:
        for i in range(-1, 2, 2):
            try_dir((i,0), pos, steps_left, towns, no_connection, visited)
            try_dir((0,i), pos, steps_left, towns, no_connection, visited)
    else:
        if not_there[0] == 0:
            for i in range(-1, 2, 2):
                try_dir((i,0), pos, steps_left, towns, no_connection, visited)
        else:
            for i in range(-1, 2, 2):
                try_dir((0,i), pos, steps_left, towns, no_connection, visited)

one_step(pos, max_steps, towns, no_connection, 1)
