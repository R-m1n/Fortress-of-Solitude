from math import sqrt
from time import sleep
from typing import Dict, List, Tuple, Generator
from argparse import ArgumentParser


"""

    A python commandline implementation of Conway's Game of Life (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

"""


class Life:
    """
    Attributes
    ----------
    length: int
        The number of rows on the grid.
    width: int
        The number of columns on the grid.
    first_gen: List[List[str]]
        A grid of cells with the initial pattern's positioning adjusted to its size.

    Methods
    -------
    play() -> Generator[str, None, None]
        Yields the string of a generation of cells, going to the next generation each time it's iterated over or passed to next().

    Examples
    --------
    ```python
    game = Life(2, [(1, 2), (2, 2), (3, 2)]).play()
    for i in range(10):
        print(f"Generation: {i + 1}\\n" + next(game))
        sleep(0.2)

    another_game = Life(5, [(2, 0), (2, 1), (2, 2), (1, 2), (0, 1)]).play()
    i = 0
    for gen in another_game:
        if i == 100:
            break

        print(f"Generation: {i + 1}\\n" + gen)
        i += 1
    ```
    """

    LIVE, DEAD = "1", "0"

    def __init__(
        self, scale: int = 2, pattern: List[Tuple[int, int]] | None = None
    ) -> None:
        """
        Parameters
        ----------
        scale: int, 2
            Determines the size of the grid; each number on the scale (n mod 5) correspondes to a specific length and width.
        pattern: List[Tuple[int]], optional
            A list of coordinates of live cells on the minimum possible grid.
        """

        size = (45, 50, 55, 60, 65)[(scale - 1) % 5]

        self.length, self.width = size, size * 2

        self.first_gen = (
            self._adjust(self._new_grid(), pattern) if pattern else self._new_grid()
        )

    def __str__(self) -> str:
        return self._chain(self.first_gen)

    def __len__(self):
        return self.length * self.width

    def play(self) -> Generator[str, None, None]:
        """
        Yields the string of a generation of cells, going to the next generation each time it's iterated over or passed to next().
        """

        curr_gen = self.first_gen

        while True:
            curr_gen = self._evolve(curr_gen)

            yield self._chain(curr_gen)

    def _new_grid(self) -> List[List[str]]:
        """
        Returns a grid of dead cells, with instance attributes length and width as its dimentions.
        """

        return [
            [self.DEAD for column in range(self.width)] for row in range(self.length)
        ]

    def _adjust(
        self, grid: List[List[str]], pattern: List[Tuple[int, int]]
    ) -> List[List[str]]:
        """
        Adjusts the positioning of a pattern on the grid, relative to the size of the grid.

        Parameters
        ----------
        grid: List[List[str]]
            A generation of cells.
        pattern: List[Tuple[int]]
            A list of coordinates of live cells on the minimum possible grid.
        """

        adjust_values = (int(sqrt(self.length) + 2) * 2, int(sqrt(self.width) + 2) * 4)

        for row, column in pattern:
            grid[row + adjust_values[0]][column + adjust_values[1]] = self.LIVE

        return grid

    def _live_neighbors(
        self, grid: List[List[str]], cell_coordinates: Tuple[int, int]
    ) -> int:
        """
        Returns the number of live neighbors of a cell on the grid.

        Parameters
        ----------
        grid: List[List[str]]
            A generation of cells.
        cell_coordinates: Tuple[int, int]
            The coordinates of a cell on the grid.
        """

        row, column = cell_coordinates

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

        live_neighbors = 0

        for neighbor_row, neighbor_column in directions:
            if 0 <= neighbor_row < self.length and 0 <= neighbor_column < self.width:
                live_neighbors += int(grid[neighbor_row][neighbor_column])

        return live_neighbors

    def _evolve(self, grid: List[List[str]]) -> List[List[str]]:
        """
        Returns the next generation of a grid.

        Parameters
        ----------
        grid: List[List[int]]
            A generation of cells.
        """

        next_gen = self._new_grid()

        for row in range(self.length):
            for column in range(self.width):
                match (grid[row][column], self._live_neighbors(grid, (row, column))):
                    case (self.LIVE, 2 | 3):
                        next_gen[row][column] = self.LIVE

                    case (self.DEAD, 3):
                        next_gen[row][column] = self.LIVE

        return next_gen

    def _chain(self, grid: List[List[str]]) -> str:
        """
        Returns the string representation of a grid.

        Parameters
        ----------
        grid: List[List[int]]
            A generation of cells.
        """

        chained = ""
        for row in grid:
            chained += "".join(row) + "\n"

        return chained


if __name__ == "__main__":
    patterns: Dict[str, List[Tuple[int, int]]] = {
        "block": [(1, 1), (1, 2), (2, 1), (2, 2)],
        "bee-hive": [(1, 2), (1, 3), (2, 1), (2, 4), (3, 2), (3, 3)],
        "loaf": [(1, 2), (1, 3), (2, 1), (2, 4), (3, 3), (3, 5), (4, 3)],
        "boat": [(1, 1), (1, 2), (2, 1), (2, 3), (3, 2)],
        "tub": [(1, 2), (2, 1), (2, 3), (3, 2)],
        "blinker": [(1, 2), (2, 2), (3, 2)],
        "toad": [(2, 1), (2, 2), (2, 3), (1, 2), (1, 3), (1, 4)],
        "beacon": [(1, 1), (1, 2), (2, 1), (3, 4), (4, 3), (4, 4)],
        "pulsar": [
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
        "r-petomino": [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)],
        "die-hard": [(1, 0), (1, 1), (2, 1), (0, 6), (2, 5), (2, 6), (2, 7)],
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
        "gosper-gun": [
            (5, 1),
            (5, 2),
            (6, 1),
            (6, 2),
            (3, 13),
            (3, 14),
            (4, 12),
            (5, 11),
            (6, 11),
            (7, 11),
            (8, 12),
            (9, 13),
            (9, 14),
            (4, 16),
            (5, 17),
            (6, 15),
            (6, 17),
            (6, 18),
            (7, 17),
            (8, 16),
            (3, 21),
            (3, 22),
            (4, 21),
            (4, 22),
            (5, 21),
            (5, 22),
            (2, 23),
            (2, 25),
            (1, 25),
            (6, 23),
            (6, 25),
            (7, 25),
            (3, 35),
            (3, 36),
            (4, 35),
            (4, 36),
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
        help="size of the grid on a scale of 1-5.",
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

    pattern = args.pattern if args.pattern and args.pattern in patterns else "pulsar"

    scale = int(args.scale if args.scale and 1 <= int(args.scale) <= 5 else 1)

    gen = int(args.gen if args.gen and 0 < int(args.gen) else 100)

    rate = float(args.rate if args.rate and 1 <= float(args.rate) <= 10 else 8)

    game = Life(scale, patterns.get(pattern)).play()

    for curr_gen in range(gen):
        print(f"Generation: {curr_gen + 1}\n" + next(game))
        sleep(1 - float(rate) / 10)
