#!/usr/bin/env python3

"""
Solution for the dominoes problem from The Guardian, 15th Jun 2020.

The
[problem](https://www.theguardian.com/science/2020/jun/15/can-you-solve-it-domino-dancing#comment-141590528)
is:

> Is it possible to cover an 8x8 chessboard with 32 dominos (which are each a
> 1x2 block) in such a way that any line parallel to a side of the chessboard
> always passes through the interior of at least one of the dominoes?

> If it is possible, draw an example. If it isn’t, prove it.
"""

import sys


def maybe_remove_line(lines, pos):
    """
    Try to remove `pos` from `lines` and return Boolean about it.

    :param lines: A set of 2-tuples of `int` values.
    :param pos: A 2-tuple of `int` values.
    :return: `True` if `pos` was removed from `lines`, `False` if it wasn't
        there.
    """
    try:
        lines.remove(pos)
    except KeyError:
        return False
    else:
        return True


def _assign_tile(canvas, x, y, chars):
    """
    Place a tile on the canvas.

    :param canvas: A "canvas" (list of lists of chars) to draw on.
    :param x, y: `int` coordinates of the top left corner of the tile.
    :param chars: A "drawing" (list of strings, each representing one "line" in
        the drawing) to put on the canvas.
    """
    for cy, c_line in enumerate(chars, start=y):
        for cx, c in enumerate(c_line, start=x):
            if canvas[cy][cx] != "+":
                canvas[cy][cx] = c


def print_tiles(n, tiles):
    """
    Print a canvas of horizontal (`"--"`) and vertical (`"|\\n|"`) tiles.

    :param n: Size of the canvas.
    :param tiles: A list of tiles, each being a 3-tuple `(x, y, d)` of two
        `int` values (position `(x, y)`) and a direction character (`"-"` for
        horizontal and `"|"` for vertical).
    """
    size_x = 3 * n + 1
    size_y = 2 * n + 1
    canvas = [[' '] * size_x for _ in range(size_y)]
    for y in range(0, size_y):
        canvas[y][0] = "+" if y in {0, size_y - 1} else "|"
        canvas[y][size_x - 1] = "+" if y in {0, size_y - 1} else "|"
    for x in range(1, size_x - 1):
        canvas[0][x] = "-"
        canvas[size_y - 1][x] = "-"
    for tile in tiles:
        if tile[2] == "-":
            _assign_tile(
                canvas,
                3 * tile[0],
                2 * tile[1],
                ["+-----+", "|     |", "+-----+"],
            )
        else:
            _assign_tile(
                canvas,
                3 * tile[0],
                2 * tile[1],
                ["+--+", "|  |", "|  |",  "|  |", "+--+"],
            )
    for line in canvas:
        print("".join(line))


def place_one(n, board=None, tiles=None, lines_x=None, lines_y=None):
    """
    Try to place one domino on the board.

    If the board is successfully finished, it gets printed and the script ends.

    :param n: An `int` size of the board.
    :param tiles: A list of domino tiles (see `print_tiles` for more details).
    :param lines_x: A set of `int` values from 1 to `n - 1`, representing the
        horizontal tiles that still don't cut any dominoes.
    :param lines_y: A set of `int` values from 1 to `n - 1`, representing the
        vertical tiles that still don't cut any dominoes.
    """
    if board is None:
        board = set()
        tiles = list()
        lines_x = set(range(1, n))
        lines_y = set(range(1, n))
    if 2 * len(tiles) == n * n:
        if lines_x or lines_y:
            return
        print("Found one:")
        print_tiles(n, tiles)
        sys.exit(0)
    try:
        x, y = next(
            (x, y)
            for y in range(n)
            for x in range(n)
            if (
                (x, y) not in board
                and (
                    x < n - 1 and (x + 1, y) not in board
                    or y < n - 1 and (x, y + 1) not in board
                )
            )
        )
    except StopIteration:
        return
    board.add((x, y))
    if x < n - 1 and (x + 1, y) not in board:
        board.add((x + 1, y))
        tiles.append((x, y, "-"))
        removed = maybe_remove_line(lines_y, x + 1)
        place_one(n, board, tiles, lines_x, lines_y)
        board.discard((x + 1, y))
        if removed:
            lines_y.add(x + 1)
        tiles.pop()
    if y < n - 1 and (x, y + 1) not in board:
        board.add((x, y + 1))
        tiles.append((x, y, "|"))
        removed = maybe_remove_line(lines_x, y + 1)
        place_one(n, board, tiles, lines_x, lines_y)
        board.discard((x, y + 1))
        if removed:
            lines_x.add(y + 1)
        tiles.pop()
    board.discard((x, y))


if __name__ == "__main__":
    try:
        n = int(sys.argv[1])
    except (IndexError, ValueError):
        n = 4
    print("n =", n)
    place_one(n)
