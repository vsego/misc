#!/usr/bin/env python3

"""
[Nonogram](https://en.wikipedia.org/wiki/Nonogram) solver.

The input is a list of strings:
* The first line contains width and height of the board, separated by the space
  character.
* The next width of lines contain space-separated hints for the vertical lines.
* The next height of lines contain space-separated hints for the horizontal
  lines.
* (optional) The next height of lines contains a drawing of the semi-solved
  board, if one wants to start from a starting semi-solution. The characters
  used are defined in the class below and are, by default, as follows:
  * empty tile: `.`,
  * unknown tile: ` `,
  * occupied tile: `@`.
"""

import itertools
import re
import sys
import time


class NonogramNoSolutionError(Exception):
    """
    Raised when trying to solve Nonogram with no solutions.
    """


class NonogramSolver:
    """
    [Nonogram](https://en.wikipedia.org/wiki/Nonogram) solver.
    """

    TILE_EMPTY = "."
    TILE_UNKNOWN = " "
    TILE_OCCUPIED = "@"

    def __init__(self, definition):
        try:
            self.width, self.height = self._line2list(definition[0])
        except (IndexError, TypeError, ValueError):
            raise ValueError(
                "the first line of the definition must contain only width and"
                " height as two ints separated by one or more spaces",
            )

        if len(definition) == self.width + self.height + 1:
            self.board = [
                [self.TILE_UNKNOWN] * self.width for _ in range(self.height)
            ]
        elif len(definition) == self.width + 2 * self.height + 1:
            f = self.width + self.height + 1
            t = self.width + 2 * self.height + 1
            self.board = self._get_board(definition[f:t])
        else:
            raise ValueError(
                "definition must contain width + height + 1 or"
                " width + 2 * height + 1 lines",
            )

        self.vertical = [
            self._line2list(line) for line in definition[1:self.width + 1]
        ]
        self.horizontal = [
            self._line2list(line)
            for line in definition[self.width + 1:self.width + self.height + 1]
        ]
        if self._sum_hints(self.vertical) != self._sum_hints(self.horizontal):
            raise ValueError(
                "the sums of vertical and horizontal hints must match",
            )

        self.iterations = None
        self.time = None

    @staticmethod
    def _line2list(line):
        """
        Return a list of numbers from a space-separated string of numbers.
        """
        return [int(v) for v in line.strip().split()]

    @staticmethod
    def _sum_hints(hints):
        """
        Return a sum of all elements of a list of lists of `int` values.
        """
        return sum(sum(line) for line in hints)

    @classmethod
    def from_file(cls, fname):
        """
        Create an instance of `NonogramSolver` and populate it from a file.
        """
        with open(fname) as f:
            return cls(list(f))

    def _get_board(self, lines):
        """
        Return a board (a list of lists of tiles) from given list of strings.
        """
        if len(lines) != self.height:
            raise ValueError("invalid number of lines in the board")
        lines = [line.rstrip("\n") for line in lines]
        try:
            invalid_line_idx = next(
                idx
                for idx, line in enumerate(lines)
                if len(line) > self.width
            )
        except StopIteration:
            pass
        else:
            raise ValueError(
                f"invalid number of columns in board's line"
                f" {invalid_line_idx + 1}",
            )
        return [
            list(line) + [self.TILE_UNKNOWN] * (self.width - len(line))
            for line in lines
        ]

    def print_board(self):
        """
        Print the current state of the board to standard output.
        """
        for line_idx, line in enumerate(self.board):
            if line_idx and line_idx % 5 == 0:
                print()
            print(re.sub(r".{5}", r"\g<0>  ", "".join(line))[:-1])

    @classmethod
    def _get_hint(cls, line):
        """
        Return a line of the board as a list of `int` values containing hints.
        """
        result = list()
        is_occupied = False
        for tile in line:
            if tile == cls.TILE_OCCUPIED:
                if is_occupied:
                    result[-1] += 1
                else:
                    is_occupied = True
                    result.append(1)
            else:
                is_occupied = False
        return result

    @classmethod
    def _solve_line(cls, line, hints):
        """
        Solve one line as much as possible.

        The algorithm tries all possible solution candidates that conform with
        `hints`. Those tiles that get the same value (empty or occupied) for
        all of the solution candidates are considered a part of the solution.
        The `line` is then updated with these elements.

        If no new elements are found, the method returns `None`.
        """
        line_try = list(line)
        occupied_cnt = sum(1 for tile in line if tile == cls.TILE_OCCUPIED)
        hints_cnt = sum(hints)
        if hints_cnt == occupied_cnt:
            return None
        tries = {
            idx: (cls.TILE_EMPTY, cls.TILE_OCCUPIED)
            for idx, tile in enumerate(line)
            if tile == cls.TILE_UNKNOWN
        }
        intersection = None
        for one_try in itertools.product(*tries.values()):
            new_cnt = sum(1 for tile in one_try if tile == cls.TILE_OCCUPIED)
            if occupied_cnt + new_cnt != hints_cnt:
                continue
            for idx, tile in zip(tries.keys(), one_try):
                line_try[idx] = tile
            if cls._get_hint(line_try) == hints:
                if intersection is None:
                    intersection = one_try
                else:
                    intersection = tuple(
                        i_tile if i_tile == t_tile else cls.TILE_UNKNOWN
                        for i_tile, t_tile in zip(intersection, one_try)
                    )
        if intersection is None:
            return None
        if all(tile == cls.TILE_UNKNOWN for tile in intersection):
            return None
        else:
            for idx, tile in zip(tries.keys(), intersection):
                line_try[idx] = tile
            return line_try

    @classmethod
    def _line_is_solved(cls, line, hints):
        """
        Return `True` if the line's number of occupied tiles matches `hints`.

        *Note:* This method assumes that the tiles don't contradict `hints` and
        only compares the total number of occupied tiles. The reason for this
        is simplicity because it is used on (semi-)solved lines which are
        already guaranteed not to contradict `hints`.
        """
        total_occupied = sum(1 for tile in line if tile == cls.TILE_OCCUPIED)
        return total_occupied == sum(hints)

    @classmethod
    def _fill_done_line(cls, line):
        """
        Replace all of the unknown tiles in the line with empty ones.
        """
        line[:] = [
            cls.TILE_EMPTY if tile == cls.TILE_UNKNOWN else tile
            for tile in line
        ]

    def _try_horizontal_lines(self, board, done_h):
        """
        Try solving all horizontal lines (each of them once).
        """
        result = False
        for idx, (line, hints) in enumerate(zip(board, self.horizontal)):
            if idx in done_h:
                continue
            line_try = self._solve_line(line, hints)
            if line_try is not None:
                line[:] = line_try
                result = True
                if self._line_is_solved(line, hints):
                    self._fill_done_line(line)
                    done_h.add(idx)
        return result

    def _fill_finished_vertical_lines(self, board, done_v):
        """
        Replace unknown tiles with empty ones in all finished vertical lines.
        """
        for idx, hints in enumerate(self.vertical):
            if idx in done_v:
                continue
            column = [line[idx] for line in board]
            if self._line_is_solved(column, hints):
                self._fill_done_line(column)
                for line, c_tile in zip(board, column):
                    line[idx] = c_tile
                done_v.add(idx)

    def _try_vertical_lines(self, board, done_v):
        """
        Try solving all vertical lines (each of them once).
        """
        result = False
        for idx, hints in enumerate(self.vertical):
            if idx in done_v:
                continue
            column = [line[idx] for line in board]
            line_try = self._solve_line(column, hints)
            if line_try is not None:
                if self._line_is_solved(line_try, hints):
                    self._fill_done_line(line_try)
                    done_v.add(idx)
                for line, lt_tile in zip(board, line_try):
                    line[idx] = lt_tile
                result = True
        return result

    def _fill_finished_horizontal_lines(self, board, done_h):
        """
        Replace unknown tiles with empty ones in all finished horizontal lines.
        """
        for idx, (line, hints) in enumerate(zip(board, self.horizontal)):
            if self._line_is_solved(line, hints):
                self._fill_done_line(line)
                done_h.add(idx)

    def solve(self):
        """
        Solve the current board as much as possible.
        """
        board = self.board
        done_h = set()
        done_v = set()
        start_time = time.time()
        for iteration in range(self.width * self.height):
            got_something_horz = self._try_horizontal_lines(board, done_h)
            if got_something_horz:
                self._fill_finished_vertical_lines(board, done_v)

            got_something_vert = self._try_vertical_lines(board, done_v)
            if got_something_vert:
                self._fill_finished_horizontal_lines(board, done_h)

            if not (got_something_horz or got_something_vert):
                break
        end_time = time.time()
        self.time = end_time - start_time
        self.iterations = iteration + 1


if __name__ == "__main__":
    try:
        solver = NonogramSolver.from_file(sys.argv[1])
    except IndexError:
        print(f"Syntax: {sys.argv[0]} filename")
        sys.exit(1)
    solver.solve()
    solver.print_board()
    print(
        f"Solved in {solver.time:.3f}s, using {solver.iterations} iterations.",
    )
