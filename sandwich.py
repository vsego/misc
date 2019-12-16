#!/usr/bin/env python3

"""
Solution to Guardian's Club Sandwich Problem.

The puzzle can be found
[here](https://www.theguardian.com/science/2019/dec/16/can-you-solve-it-the-club-sandwich-problem).
"""


def _rec(sol, cnts):
    """
    Recursive call for creating sandwich numbers.

    :param sol: A string containing the currently constructed number.
    :param cnts: A `dict` associating digits (as strings) with the number of
        times each of them is yet to be used.
    :return: Either a string sandwich number or `None` if one does not exist.
    """
    # Check if we've used all the digits.
    if all(cnt == 0 for cnt in cnts.values()):
        return sol
    # Which digit(s) *must* be added here.
    must = [
        d
        for i, d in enumerate(sol)
        if i + int(d) + 1 == len(sol) and cnts[d] > 0
    ]
    if len(must) > 1:
        # We can't put more than one digit anywhere, so this is a dead end.
        return None
    elif len(must) == 1:
        # Exactly one candidate, which is awesome!
        # No trial and error, just use that one.
        items = ((must[0], cnts[must[0]]),)
    else:
        # We'll need to try all of those we didn't use up completely.
        items = tuple((d, cnt) for d, cnt in cnts.items() if cnt > 0)

    # Let's append one digit.
    for d, cnt in items:
        if d in sol:
            # If we already used `d`, it has to conform with the sandwich
            # requirement (i.e., we cannot add it if it wouldn't wrap exactly d
            # other digits).
            try:
                if sol[-(int(d) + 1)] != d:
                    continue
            except IndexError:
                continue
        # We're gonna use this one, so reduce its count...
        cnts[d] -= 1
        # ...and call the recursion to fill up the next one.
        res = _rec(sol + d, cnts)
        # If we got a solution, that's it!
        if res is not None:
            return res
        # If not, we just got our digit back.
        cnts[d] += 1
    # Getting here means we didn't get a solution, so we return `None`.
    return None


def sandwich(digits, cnt):
    """
    Return a sandwich number.

    :param digits: An iterable of digits used to construct the number.
    :param cnt; How many times should each digit be used (exactly).
    :return: Either an `int` sandwich number or `None` if one does not exist.
    """
    result = _rec("", {str(d): cnt for d in digits})
    return None if result is None else int(result)


if __name__ == "__main__":
    print("Part 1:", sandwich("1234", 2))
    print("Part 2:", sandwich("123456789", 3))
