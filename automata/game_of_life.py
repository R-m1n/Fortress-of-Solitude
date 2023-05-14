import math
from time import sleep
from typing import List, Tuple, Generator
import numpy as np


class Life:
    def __init__(self, pattern: List[Tuple[int]], length: int = 40) -> None:
        self.first_gen = np.zeros((length, length * 2), np.int0)
        self.length = length
        self.adjust_value = int(math.sqrt(length) + 2) * 2
        self._adjust(pattern)

    def play(self) -> Generator:
        gen = 1
        first_gen = self.first_gen

        while True:
            plain = "\n"
            plain += f"Generation: {gen}\n"
            next_gen = self._evolve(first_gen)

            for row in next_gen:
                plain += "".join(map(lambda cell: str(cell), row)) + "\n"

            first_gen = next_gen
            gen += 1

            yield plain

    def _adjust(self, points: List[Tuple[int]]) -> None:
        for point in points:
            row = point[0] + self.adjust_value - 4
            column = point[1] + self.adjust_value * 2

            self.first_gen[row][column] = 1

    def _neighbors(self, coordinates: tuple, length: int) -> List[Tuple[int]]:
        row, column = coordinates

        n = (row - 1, column)
        ne = (row - 1, column + 1)
        e = (row, column + 1)
        se = (row + 1, column + 1)
        s = (row + 1, column)
        sw = (row + 1, column - 1)
        w = (row, column - 1)
        nw = (row - 1, column - 1)

        potential_neighbors = (n, ne, e, se, s, sw, w, nw)
        neighbors = []

        for neighbor in potential_neighbors:
            if (neighbor[0] < 0 or neighbor[0] >= length) or (
                neighbor[1] < 0 or neighbor[1] >= length * 2
            ):
                continue

            neighbors.append(neighbor)

        return neighbors

    def _evolve(self, first_gen: List[List[int]]) -> List[List[int]]:
        next_gen = np.zeros((self.length, self.length * 2), np.int0)
        alive, dead = 1, 0

        for row in range(self.length):
            for column in range(self.length * 2):
                cell, coordinates = first_gen[row][column], (row, column)
                alive_neighbors = 0

                for neighbor in self._neighbors(coordinates, self.length):
                    if first_gen[neighbor[0]][neighbor[1]] == alive:
                        alive_neighbors += 1

                if cell == dead:
                    if (
                        alive_neighbors == 0
                        or alive_neighbors == 1
                        or alive_neighbors == 2
                    ):
                        next_gen[row][column] = dead

                    elif alive_neighbors == 3:
                        next_gen[row][column] = alive

                elif cell == alive:
                    if alive_neighbors == 0 or alive_neighbors == 1:
                        next_gen[row][column] = dead

                    elif alive_neighbors == 2 or alive_neighbors == 3:
                        next_gen[row][column] = alive

                    elif alive_neighbors > 3:
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

    game = Life(patterns.get("acorn")).play()
    speed = 9

    for i in range(100):
        print(next(game))
        sleep(1 - speed / 10)
