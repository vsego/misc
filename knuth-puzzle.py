#!/usr/bin/env python3

"""
A program to solve Knuth's Puzzle:
https://twitter.com/nhigham/status/752947988977311744

It uses a fairly simple approach of solving what is completely
deterministic, and it will fail if a problem has multiple solutions.
"""

puzzle = {
    "|": [1,1,1,5,1,5,1,5,1,1,5,3,3,3,1,6,1,4,3,3,4],
    "-": [19,7,12,6,13,0,1],
    "/": [1,1,1,1,1,2,2,3,4,3,3,3,2,3,4,3,3,2,3,3,2,3,2,2,1,0,0],
    "\\": [0,0,0,0,0,1,3,3,4,3,2,2,2,3,3,4,2,3,3,3,3,3,4,3,2,1,1],
}

dirs = {"|": (0,1), "-": (1,0), "/": (1,-1), "\\": (1,1), }
marks_pos = {
    "|": lambda x,y: x,
    "-": lambda x,y: y,
    "/": lambda x,y: x+y,
    "\\": lambda x,y: (n-y-1)+x,
}
ch_mistery = "?"
ch_w = " "
ch_b = "█"

def xy_sum(x, y, d, set_ch=None):
    while (0 <= x < m) and (0 <= y < n):
        x += d[0]
        y += d[1]
    x -= d[0]
    y -= d[1]
    sum_w, sum_b, sum_mistery, new = (0, 0, 0, 0)
    while (0 <= x < m) and (0 <= y < n):
        if solution[x][y] == ch_w:
            sum_w += 1
        elif solution[x][y] == ch_b:
            sum_b += 1
        else:
            sum_mistery += 1
            if set_ch is not None:
                solution[x][y] = set_ch
                new += 1
        x -= d[0]
        y -= d[1]
    return (sum_w, sum_b, sum_mistery, new)

#for dc,mark_list in puzzle.items():
#    print("{}: {}".format(dc, sum(mark_list)))
m,n = [len(puzzle[c]) for c in "|-"]
solution = [[ch_mistery] * n for _ in range(m)]
missing = m*n

try:
    while True:
        om = missing
        for x in range(m):
            for y in range(n):
                for dc,dd in dirs.items():
                    (sum_w, sum_b, sum_mistery, new) = xy_sum(x, y, dd)
                    if sum_mistery == 0:
                        continue
                    mark = puzzle[dc][marks_pos[dc](x, y)]
                    if sum_b > mark:
                        raise StopIteration()
                    if sum_b == mark:
                        (sum_w, sum_b, sum_mistery, new) = \
                            xy_sum(x, y, dd, ch_w)
                    elif sum_b + sum_mistery == mark:
                        (sum_w, sum_b, sum_mistery, new) = \
                            xy_sum(x, y, dd, ch_b)
                    missing -= new
                    if missing <= 0:
                        raise StopIteration()
        if missing == om:
            break
except StopIteration:
    pass
for y in range(n):
    print("".join(solution[x][y] for x in range(m)))
xy = [(0,y) for y in range(n)] + [(x,n-1) for x in range(1,m)] 
for x,y in xy:
    for dc,dd in dirs.items():
        (sum_w, sum_b, sum_mistery, new) = xy_sum(x, y, dd)
        mark = puzzle[dc][marks_pos[dc](x, y)]
        if sum_b > mark or sum_b + sum_mistery < mark:
            print("Error at {}: dir='{}', sum_w = {}, sum_b = {}, sum_m = {}, mark = {}".format(
                (x, y), dc, sum_w, sum_b, sum_mistery, mark
            ))
