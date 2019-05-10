#!/usr/bin/env python3

"""
A crude solver for [Move Here Move There]
(https://www.newgrounds.com/portal/view/718498).
"""

board = {
    (0, 0): "X",
    (3, 0): "X",
    (4, 0): [(-3, 3)],
    (6, 0): "X",
    (0, 1): "X",
    (4, 2): "X",
    (0, 4): [(4, 0)],
    (3, 4): [(3, -3)],
    (4, 4): [(1, 0), (-1, 1)],
    (1, 5): "X",
    (3, 5): [(-1, -1)],
    (5, 5): "X",
}
pieces = [
    [(-1, -1), (0, 4)],
    [(2, -2), (-1, -1)],
    [(4, 0)],
    [(0, -5)],
    [(2, 2)],
    [(0, 3)],
    [(-2, -2)],
    [(-5, 0)],
]
start = (3, 4)
maxes = (6, 5)


def move(pos, piece):
    """
    Return new position after moving by one piece.

    :param pos: A 2-tuple of `int`s, describing the starting position.
    :param piece: A list of 2-tuples of `int`s, describing one piece's moves.
    :raise ValueError: Raised if the move is impossible.
    :return: A 2-tuple of `int`s describing the new position.
    """
    for jmp in piece:
        pos = (pos[0] + jmp[0], pos[1] + jmp[1])
        if not (0 <= pos[0] <= maxes[0] and 0 <= pos[1] <= maxes[1]):
            raise ValueError()
    return pos


def step(pos, pieces, history):
    """
    Execute one step.

    :param pos: A 2-tuple of `int`s, describing the starting position.
    :param pieces: A list of lists of 2-tuples of `int`s, describing still
        unused pieces.
    :param history: A list of lists of 2-tuples of `int`s, describing already
        used pieces.
    """
    if not pieces and all(v == "X" for v in board.values()):
        print(f"{pos}: {history}")
        return
    try:
        nxt = board[pos]
    except KeyError:
        for pidx, piece in enumerate(pieces):
            try:
                pos2 = move(pos, piece)
            except ValueError:
                continue
            else:
                board[pos] = "X"
                step(pos2, pieces[:pidx] + pieces[pidx + 1:], history + [piece])
                del board[pos]
    else:
        if nxt == "X":
            return
        try:
            pos2 = move(pos, nxt)
        except ValueError:
            return
        else:
            board[pos] = "X"
            step(pos2, pieces, history)
            board[pos] = nxt


step(start, pieces, list())
