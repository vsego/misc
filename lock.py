#!/usr/bin/env python3

"""
A programmatic solution for a lock problem.

The lock has a 3-digit code. To unlock it, consider these clues:
* 682: exactly one digit is exactly where it should be;
* 614: exactly one digit is correct, but in the wrong place;
* 206: exactly two digits are correct, but in the wrong place;
* 738: all the digits are wrong;
* 380: exactly one digit is correct, but in the wrong place.
"""


def well_placed(passwd, code, chk):
    """
    Return `True` if `chk` digits of `code` are correctly placed.

    :param passwd: A string containing the password against which the check is
        done.
    :param code: A string containing the code to check.
    :param chk: An `int` containing the expected value.
    :return: A Boolean value saying if the check is passing or not.
    """
    return (chk == sum(1 for c1, c2 in zip(passwd, code) if c1 == c2))


def only_correct(passwd, code, chk):
    """
    Return `True` if `chk` digits of `code` are present but incorrectly placed.

    :param passwd: A string containing the password against which the check is
        done.
    :param code: A string containing the code to check.
    :param chk: An `int` containing the expected value.
    :return: A Boolean value saying if the check is passing or not.
    """
    res = sum(1 for i, c in enumerate(passwd) if c in code)
    return res == chk and well_placed(passwd, code, 0)


if __name__ == "__main__":
    for passwd in range(1000):
        passwd = f"{passwd:03d}"
        if (
            well_placed(passwd, "682", 1)
            and only_correct(passwd, "614", 1)
            and only_correct(passwd, "206", 2)
            and only_correct(passwd, "738", 0)
            and only_correct(passwd, "380", 1)
        ):
            print(passwd)
