#!/usr/bin/env python3

"""
A programmatic solution for a fun probability problem.

Source: https://twitter.com/DrFrostMaths/status/1247632591408242688

Team A and team B play series. The first team to win three games wins the
series. Each team is equally likely to win each game, there are no ties, and
the outcomes of the individual games are independent. If team B wins the second
game and team A wins the series, what is the probability that team B wins the
first game?

(A) 1/5    (B) 1/4    (C) 1/3    (D) 1/2    (E) 2/3
"""

from fractions import Fraction


def cnt(seq, c):
    """
    Return number of occurrences of character `c` in string `seq`.
    """
    return sum(1 for ch in seq if ch == c)


def f(seq="", p=Fraction(1)):
    """
    Solve the problem.
    """
    if cnt(seq, "A") >= 3:
        return int(seq[0] == "B") * p, p
    elif cnt(seq, "B") >= 3:
        return 0, 0
    p /= 2
    r1 = r2 = 0
    for c in "B" if len(seq) == 1 else "AB":
        r = f(f"{seq}{c}", p)
        r1 += r[0]
        r2 += r[1]
    return r1, r2


if __name__ == "__main__":
    r1, r2 = f()
    print(r1 / r2)
