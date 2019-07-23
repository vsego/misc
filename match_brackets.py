#!/usr/bin/env python3

"""
Module for checking the matching of braces in expressions.

There are two functions here:
* `match_brackets_slow`: a slow and naive implementation, mainly used as a show
  for the idea on how to prove the other algorithms correctness;
* `match_brackets_greedy`: a greedy algorithm that works in linear time.

The "slow" algorithm should not be used. It is a show of the concept that the
brackets match if and only if the following two assumptions hold:
1. There is a matching pair in consecutive characters of `expr` (after
   stripping all the non-bracket characters).
2. If a matching pair is removed, the validity of the starting expression
   doesn't change.

The above can be used for a mathematically sound proof that the greedy
algorithm works fine. The potential issue with that algorithm lies in the
ambiguity of `"|"`: it can be both the opening and the closing bracket and the
greedy algorithm treats it as a closing one whenever possible.

Let us assume that the greedy algorithm gives a false negative. That means that
there is an `expr` where it is possible to match `"|"` as a closing bracket,
but that this wrongly returns `False` for the whole expression.

However, observing the sub-expression that was matched this way, we can remove
it from `expr`, and this does not change the validity of the `expr`, which
means that the rest can still be properly match. This is a contradiction with
the assumption that it causes a false negative.

In other words, there are no counter-examples for the greedy algorithm.

Obviously, for this to be a complete proof, the above two points that
the "slow" algorithm shows should be properly proven (which is left as
an exercise for the reader :-)).
"""


try:
    from colorama import Fore, Style
except ImportError:
    _reset = _title_code = _code = _ok = _fail = ""
else:
    _reset = Style.RESET_ALL
    _title_code = f"{Fore.YELLOW}{Style.BRIGHT}"
    _code = f"{Fore.WHITE}{Style.BRIGHT}"
    _ok = f"{Fore.GREEN}{Style.BRIGHT}ok{_reset}"
    _fail = f"{Fore.RED}{Style.BRIGHT}FAILED!{_reset}"


def _parse_brackets(brackets):
    """
    Return a `dict` of brackets from the given string.
    """
    return dict(zip(brackets[::2], brackets[1::2]))


def match_brackets_slow(expr, *, brackets="()[]{}||"):
    """
    Return `True` if `expr` has matching brackets; otherwise `False`.

    :param expr: A string expression to be parsed.
    :param brackets: A string of pairs of brackets to be matched (the pairs
        should have no intersections!).
    :return: A Boolean.
    """
    matches = _parse_brackets(brackets)
    pairs = {f"{b1}{b2}" for b1, b2 in matches.items()}

    # This is not a good way to remove non-brackets, but the function is not
    # meant to be used anyway, so we're focusing on readability.
    bracket_chars = set(matches.keys()) | set(matches.values())
    expr = "".join(c for c in expr if c in bracket_chars)

    while expr:
        old_expr = expr
        for pair in pairs:
            expr = expr.replace(pair, "")
        if old_expr == expr:
            return False

    return len(expr) == 0


def match_brackets_greedy(expr, *, brackets="()[]{}||"):
    """
    Return `True` if `expr` has matching brackets; otherwise `False`.

    :param expr: A string expression to be parsed.
    :param brackets: A string of pairs of brackets to be matched (the pairs
        should have no intersections!).
    :return: A Boolean.
    """
    matches = _parse_brackets(brackets)
    lefts = set(matches.keys())
    rights = set(matches.values())
    stack = list()

    for c in expr:
        found = False
        if c in rights:
            found = True
            if stack and matches[stack[-1]] == c:
                stack.pop()
                continue
        if c in lefts:
            stack.append(c)
        elif found:
            return False

    return len(stack) == 0


def _test(f, expr, expected_result, **kwargs):
    """
    Test `expr` and print the appropriate message.
    """
    success = f(expr, **kwargs) is expected_result
    cmd = f"{f.__name__}({repr(expr)}"
    if kwargs:
        cmd += ", " + ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
    cmd += ")"
    print(f"  Testing {_code}{cmd}{_reset}:", f"{_ok}." if success else _fail)
    if success:
        _test.ok += 1
    else:
        _test.failed += 1


if __name__ == "__main__":
    _test.ok = 0
    _test.failed = 0
    for f in (match_brackets_slow, match_brackets_greedy):
        print(f"Testing {_title_code}{f.__name__}{_reset}...")
        _test(f, "", True)
        _test(f, "Popocatepetl", True)
        _test(f, "(a)", True)
        _test(f, "(a{b}c)", True)
        _test(f, "3(5{7}11[13{17}19]23)29", True)
        _test(f, "a|b(c)d|e", True)
        _test(f, "||({})|()|", True)
        _test(f, "())(()", False)
        _test(f, "(()", False)
        _test(f, "|(|)", False)
        _test(f, "|(|)", True, brackets="()")
        _test(f, "|)|(", True, brackets=")(")
        _test(f, "|(|)", False, brackets=")(")
        _test(f, "()", False, brackets=")(")
    print(f"Total successes: {_test.ok}")
    print(f"Total failures:  {_test.failed}")
