#!/usr/bin/python3

"""
Print all expressions with `nums` evaluating to `n` and return their count.

Usage: `./prog.py n num1 num2 ...`
"""

import sys
from typing import TypeAlias, Literal, get_args, Optional


T_ops = Literal["+", "-", "/", "*"]
ops = get_args(T_ops)
T_postfix: TypeAlias = tuple[int | T_ops, ...]


def postfix(expr: T_postfix) -> tuple[Optional[str], Optional[int | float]]:
    """
    Return infix version and value of the given expression.
    """
    stack: list[str | float | int]
    infix: str = ""
    result: int | float = 0
    for run_eval in (False, True):
        stack = list()
        for token in expr:
            if isinstance(token, str):
                try:
                    value2 = stack.pop()
                    value1 = stack.pop()
                except IndexError:
                    raise ValueError(
                        f"invalid postfix expression: {repr(expr)}",
                    )
                sub_expr = f"({value1}{token}{value2})"
                if run_eval:
                    try:
                        stack.append(eval(sub_expr))
                    except ZeroDivisionError:
                        return None, None
                else:
                    stack.append(sub_expr)
            else:
                stack.append(token)
        if len(stack) != 1:
            raise ValueError(f"invalid postfix expression: {repr(expr)}")
        r = stack.pop()
        if run_eval and isinstance(r, (float, int)):
            result = int(r) if isinstance(r, float) and r.is_integer() else r
        elif not run_eval and isinstance(r, str):
            infix = str(r)

    return str(infix)[1:-1], result


def solve(
    n: int,
    nums: tuple[int, ...],
    expr: Optional[T_postfix] = None,
    nums_cnt: int = 0,
    ops_cnt: int = 0,
) -> int:
    """
    Print all expressions with `nums` evaluating to `n` and return their count.
    """
    result = 0
    if expr is None:
        expr = tuple()
    if nums:
        new_nc = nums_cnt + 1
        for i, num in enumerate(nums):
            result += solve(
                n, nums[:i] + nums[i + 1:], expr + (num,), new_nc, ops_cnt,
            )
    new_oc = ops_cnt + 1
    if nums_cnt > new_oc:
        for op in ops:
            result += solve(n, nums, expr + (op,), nums_cnt, new_oc)
    elif nums_cnt == new_oc:
        infix, value = postfix(expr)
        if value == n:
            print(infix)
            result += 1
    return result


if __name__ == "__main__":
    try:
        n = int(sys.argv[1])
        nums = tuple(int(arg) for arg in sys.argv[2:])
    except (IndexError, ValueError):
        print("Usage: {sys.args[0]} target num1 num2 ...")
    else:
        total = solve(n, nums)
        print("Total solutions:", total)
