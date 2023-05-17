import numpy as np

from math import sqrt
from time import sleep
from typing import List, Tuple, Generator
from argparse import ArgumentParser


"""

    A python commandline implementation of Conway's Game of Life (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

"""


class Life:
    """
    Attributes
    ----------
    pattern: List[Tuple[int]]
        A list of coordinates of alive cells on the minimum possible plain.

    scale: int
        Size of the plain.


    Methods
    -------
    play() -> Generator
        Yeilds a string of the plain going to the next generation each time it's iterated over or passed to next().
    """

    def __init__(self, pattern: List[Tuple[int]], scale: int = 2) -> None:
        size = (40, 45, 50, 55, 60)[scale - 1]

        self.length, self.width = size, size * 2

        self.first_gen = self._empty_plain()
        self._adjust(pattern)

    def play(self) -> Generator:
        """
        Yeilds a string of the plain, going to the next generation each time it's iterated over or passed to next().
        """

        gen = 1
        curr_gen = self.first_gen

        while True:
            plain = "\n"
            plain += f"Generation: {gen}\n"
            next_gen = self._evolve(curr_gen)

            for row in next_gen:
                plain += "".join(map(lambda cell: str(cell), row)) + "\n"

            curr_gen = next_gen
            gen += 1

            yield plain

    def _empty_plain(self) -> List[List[int]]:
        """
        Returns an empty plain.
        """

        return np.zeros((self.length, self.width), np.int0)

    def _adjust(self, pattern: List[Tuple[int]]) -> None:
        """
        Adjusts the positioning of a pattern relative to the size of the plain.

        Parameters
        ----------
        pattern: List[Tuple[int]]
            A list of coordinates of alive cells on the minimum possible plain.
        """

        adjust_values = (int(sqrt(self.length) + 2) * 2, int(sqrt(self.width) + 2) * 4)

        for row, column in pattern:
            adjusted_row, adjusted_column = (
                row + adjust_values[0],
                column + adjust_values[1],
            )

            self.first_gen[adjusted_row][adjusted_column] = 1

    def _neighbors(self, coordinates: Tuple) -> List[Tuple[int]]:
        """
        Returns a list of the coordinates of neighbors of a cell relative to the size of the plain.

        Parameters
        ----------
        coordinates: tuple
            The coordinates of a cell on the plain.
        """

        row, column = coordinates

        directions = [
            (row - 1, column),
            (row - 1, column + 1),
            (row, column + 1),
            (row + 1, column + 1),
            (row + 1, column),
            (row + 1, column - 1),
            (row, column - 1),
            (row - 1, column - 1),
        ]

        return [
            (neighbor_row, neighbor_column)
            for neighbor_row, neighbor_column in directions
            if (
                (0 <= neighbor_row < self.length)
                and (0 <= neighbor_column < self.width)
            )
        ]

    def _evolve(self, curr_gen: List[List[int]]) -> List[List[int]]:
        """
        Returns the next generation of a given generation.

        Parameters
        ----------
        curr_gen: List[List[int]]
            A generation of cells on the plain.
        """

        next_gen = self._empty_plain()
        alive, dead = 1, 0

        for row in range(self.length):
            for column in range(self.width):
                cell, coordinates = curr_gen[row][column], (row, column)
                alive_neighbors = 0

                for neighbor_row, neighbor_column in self._neighbors(coordinates):
                    if curr_gen[neighbor_row][neighbor_column] == alive:
                        alive_neighbors += 1

                if cell == dead:
                    match alive_neighbors:
                        case 0 | 1 | 2:
                            next_gen[row][column] = dead

                        case 3:
                            next_gen[row][column] = alive

                elif cell == alive:
                    match alive_neighbors:
                        case 0 | 1:
                            next_gen[row][column] = dead

                        case 2 | 3:
                            next_gen[row][column] = alive

                        case _:
                            next_gen[row][column] = dead

        return next_gen


if __name__ == "__main__":
    patterns = {
        "block": [(1, 1), (1, 2), (2, 1), (2, 2)],
        "bee_hive": [(1, 2), (1, 3), (2, 1), (2, 4), (3, 2), (3, 3)],
        "loaf": [(1, 2), (1, 3), (2, 1), (2, 4), (3, 3), (3, 5), (4, 3)],
        "boat": [(1, 1), (1, 2), (2, 1), (2, 3), (3, 2)],
        "tub": [(1, 2), (2, 1), (2, 3), (3, 2)],
        "blinker": [(1, 2), (2, 2), (3, 2)],
        "toad": [(2, 1), (2, 2), (2, 3), (1, 2), (1, 3), (1, 4)],
        "beacon": [(1, 1), (1, 2), (2, 1), (3, 4), (4, 3), (4, 4)],
        "polsar": [
            (0, 2),
            (0, 3),
            (0, 4),
            (0, 8),
            (0, 9),
            (0, 10),
            (2, 0),
            (2, 5),
            (2, 7),
            (2, 12),
            (3, 0),
            (3, 5),
            (3, 7),
            (3, 12),
            (4, 0),
            (4, 5),
            (4, 7),
            (4, 12),
            (5, 2),
            (5, 3),
            (5, 4),
            (5, 8),
            (5, 9),
            (5, 10),
            (7, 2),
            (7, 3),
            (7, 4),
            (7, 8),
            (7, 9),
            (7, 10),
            (8, 0),
            (8, 5),
            (8, 7),
            (8, 12),
            (9, 0),
            (9, 5),
            (9, 7),
            (9, 12),
            (10, 0),
            (10, 5),
            (10, 7),
            (10, 12),
            (12, 2),
            (12, 3),
            (12, 4),
            (12, 8),
            (12, 9),
            (12, 10),
        ],
        "pentadecathlon": [
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 0),
            (1, 4),
            (2, 0),
            (2, 4),
            (3, 1),
            (3, 2),
            (3, 3),
            (8, 1),
            (8, 2),
            (8, 3),
            (9, 0),
            (9, 4),
            (10, 0),
            (10, 4),
            (11, 1),
            (11, 2),
            (11, 3),
        ],
        "glider": [(2, 0), (2, 1), (2, 2), (1, 2), (0, 1)],
        "lwss": [(0, 3), (1, 4), (2, 0), (2, 4), (3, 1), (3, 2), (3, 3), (3, 4)],
        "mwss": [
            (0, 4),
            (1, 5),
            (2, 0),
            (2, 5),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5),
        ],
        "hwss": [
            (0, 5),
            (1, 6),
            (2, 0),
            (2, 6),
            (3, 1),
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5),
            (3, 6),
        ],
        "r_petomino": [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)],
        "die hard": [(1, 0), (1, 1), (2, 1), (0, 6), (2, 5), (2, 6), (2, 7)],
        "acorn": [(0, 1), (1, 3), (2, 0), (2, 1), (2, 4), (2, 5), (2, 6)],
        "flint": [(2, 1), (2, 2), (2, 3), (1, 3), (1, 0)],
        "ti": [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (5, 2),
        ],
    }

    parser = ArgumentParser(prog="GameOfLife", description="CommandLine Game of Life.")

    parser.add_argument(
        "-p",
        "--pattern",
        help=f"lexicon: {tuple(patterns.keys())}",
    )

    parser.add_argument(
        "-s",
        "--scale",
        help="size of the plain on a scale of 1-5.",
    )

    parser.add_argument(
        "-r",
        "--rate",
        help="rate of evolution on a scale of 1-10.",
    )

    parser.add_argument(
        "-g",
        "--gen",
        help="number of generations.",
    )

    args = parser.parse_args()

    pattern = (
        args.pattern if args.pattern != None and args.pattern in patterns else "polsar"
    )

    scale = args.scale if args.scale != None and 1 <= int(args.scale) <= 5 else 1

    gen = args.gen if args.gen != None and 0 < int(args.gen) else 50

    rate = args.rate if args.rate != None and 1 <= float(args.rate) <= 10 else 8

    game = Life(patterns.get(pattern), int(scale)).play()

    for _ in range(int(gen)):
        print(next(game))
        sleep(1 - float(rate) / 10)
