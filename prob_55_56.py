#!/usr/bin/env python3

"""
Experimental verification of a probability experiment.

The experiment is run as follows: keep rolling the dice until two consecutive
throws give either (5, 5) or (5, 6). The question is: which outcome is more
likely to happen?
"""

import argparse
from multiprocessing import Pool, cpu_count
import random
import sys


def experiment(k):
    """
    Run experiment once and return the number that ended it.
    """
    prev = None
    while True:
        curr = random.randint(1, 6)
        if (prev, curr) == (5, 5):
            return 55
        elif (prev, curr) == (5, 6):
            return 56
        prev = curr


def experiments(n, procs):
    """
    Run `n` experiments on `procs` processors and return the result.
    """
    cnts = {55: 0, 56: 0}
    with Pool(procs) as p:
        for key in p.map(experiment, range(n)):
            cnts[key] += 1
    return cnts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument("n", type=int, help="Number of experiments to run.")
    parser.add_argument(
        "--procs", "-p",
        type=int,
        default=cpu_count(),
        help="Number of parallel processes to run.",
    )
    args = parser.parse_args()
    print(f"Running {args.procs} processes in parallel.")
    cnts = experiments(args.n, args.procs)
    print("\n".join(f"{key}:  {value}" for key, value in cnts.items()))
