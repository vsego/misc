#!/usr/bin/env python3

"""
A solver for [sorting elves problem](https://www.theguardian.com/science/2016/dec/19/can-you-solve-it-are-you-more-sorted-than-a-german-elf-at-christmas).
"""

from itertools import permutations

num_of_elves = 4
sorters = [
    {
        # Comparators
        # Elements are either En (elves[n]) or CnS (comparator n, output side S (L or R))
        'c': [ "E0,E1", "E2,E3", "C0R,C1L", "C0L,C2L", "C1R,C2R", ],
        # Targets
        't': [ "C3L", "C3R", "C4L", "C4R", ],
    },
    {
        'c': [ "E0,E1", "E2,E3", "C0L,C1L", "C0R,C1R", ],
        't': [ "C2L", "C2R", "C3L", "C3R", ],
    },
    {
        'c': [ "E0,E3", "E1,C0L", "C0R,E2", "C1L,C2L", "C1R,C2R", ],
        't': [ "C3L", "C3R", "C4L", "C4R", ],
    },
    {
        'c': [ "E0,E1", "E2,E3", "C0L,C1L", "C0R,C1R", "C2R,C3L", ],
        't': [ "C2L", "C4L", "C4R", "C3R", ],
    },
]

sorted_elves = tuple(range(1,num_of_elves+1))
new_row = [0] * num_of_elves

def test_sorter(sorter):
    """
    Prints failed inputs and returns `False` if there are any,
    and `True` otherwise.
    """
    def get_value(elves, val):
        if ',' in val:
            val1,val2 = val.split(',')
            val1 = get_value(elves, val1)
            val2 = get_value(elves, val2)
            return min(val1,val2), max(val1,val2)
        if val[0] == 'E':
            return elves[int(val[1])]
        (wc,wr) = list(val[1:]) # which_comparator, which_result
        wc = int(wc)
        if cache[wc] is None:
            cache[wc] = get_value(elves, sorter['c'][int(wc)])
        val = cache[wc]
        if wr == 'L': return val[0]
        if wr == 'R': return val[1]
        raise ValueError()
    ok = True
    for elves in permutations(sorted_elves):
        cache = [None] * len(sorter['c'])
        target = [
            get_value(elves, val)
                for val in sorter['t']
        ]
        if any(x>y for x,y in zip(target, target[1:])):
            ok = False
            print("   ", elves, "->", target)
    if ok: print("    OK!")
    return ok

for idx,sorter in enumerate(sorters):
    print("Machine #%d..." % (idx+1))
    test_sorter(sorter)
