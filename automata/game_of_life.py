import math
from time import sleep
from typing import List, Tuple
import numpy as np


class Life():
    def __init__(self, length: int = 50) -> None:
        self.first_gen = np.zeros((length, length), np.int0)
        self.length = length
        self.pivot = int(math.sqrt(length) + 2) * 2

    def evolve(self, first_gen: List[List[int]]) -> List[List[int]]:
        next_gen = np.zeros((self.length, self.length), np.int0)
        alive, dead = 1, 0

        for row in range(self.length):
            for column in range(self.length):
                cell, coordinates = first_gen[row][column], (row, column)
                alive_neighbors = 0

                for neighbor in self.neighbors(coordinates, self.length):
                    if first_gen[neighbor[0]][neighbor[1]] == alive:
                        alive_neighbors += 1

                if cell == dead:
                    if alive_neighbors == 0 or alive_neighbors == 1 or alive_neighbors == 2:
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

    def sandbox(self, points: List[Tuple[int]]):
        for point in points:
            row = point[0] + self.pivot
            column = point[1] + self.pivot

            self.first_gen[row][column] = 1

        self.__play()

    def block(self):
        points = [(1, 1), (1, 2), (2, 1), (2, 2)]

        self.sandbox(points)

    def bee_hive(self):
        points = [(1, 2), (1, 3), (2, 1), (2, 4), (3, 2), (3, 3)]

        self.sandbox(points)

    def loaf(self):
        points = [(1, 2), (1, 3), (2, 1), (2, 4), (3, 3), (3, 5), (4, 3)]

        self.sandbox(points)

    def boat(self):
        points = [(1, 1), (1, 2), (2, 1), (2, 3), (3, 2)]

        self.sandbox(points)

    def tub(self):
        points = [(1, 2), (2, 1), (2, 3), (3, 2)]

        self.sandbox(points)

    def blinker(self):
        points = [(1, 2), (2, 2), (3, 2)]

        self.sandbox(points)

    def toad(self):
        points = [(2, 1), (2, 2), (2, 3), (1, 2), (1, 3), (1, 4)]

        self.sandbox(points)

    def beacon(self):
        points = [(1, 1), (1, 2), (2, 1),
                  (3, 4), (4, 3), (4, 4)]

        self.sandbox(points)

    def polsar(self):
        points = [(0, 2), (0, 3), (0, 4), (0, 8), (0, 9), (0, 10),
                  (2, 0), (2, 5), (2, 7), (2, 12), (3, 0), (3, 5),
                  (3, 7), (3, 12), (4, 0), (4, 5), (4, 7), (4, 12),
                  (5, 2), (5, 3), (5, 4), (5, 8), (5, 9), (5, 10),
                  (7, 2), (7, 3), (7, 4), (7, 8), (7, 9), (7, 10),
                  (8, 0), (8, 5), (8, 7), (8, 12), (9, 0), (9, 5),
                  (9, 7), (9, 12), (10, 0), (10, 5), (10, 7), (10, 12),
                  (12, 2), (12, 3), (12, 4), (12, 8), (12, 9), (12, 10), ]

        self.sandbox(points)

    def pentadecathlon(self):
        points = [(0, 1), (0, 2), (0, 3), (1, 0), (1, 4),
                  (2, 0), (2, 4), (3, 1), (3, 2), (3, 3),
                  (8, 1), (8, 2), (8, 3), (9, 0), (9, 4),
                  (10, 0), (10, 4), (11, 1), (11, 2), (11, 3), ]

        self.sandbox(points)

    def glider(self):
        points = [(2, 0), (2, 1), (2, 2), (1, 2), (0, 1)]

        self.sandbox(points)

    def lwss(self):
        points = [(0, 3), (1, 4), (2, 0), (2, 4), (3, 1),
                  (3, 2), (3, 3), (3, 4)]

        self.sandbox(points)

    def mwss(self):
        points = [(0, 4), (1, 5), (2, 0), (2, 5), (3, 1),
                  (3, 2), (3, 3), (3, 4), (3, 5)]

        self.sandbox(points)

    def hwss(self):
        points = [(0, 5), (1, 6), (2, 0), (2, 6), (3, 1),
                  (3, 2), (3, 3), (3, 4), (3, 5), (3, 6)]

        self.sandbox(points)

    def r_pentomino(self):
        points = [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)]

        self.sandbox(points)

    def die_hard(self):
        points = [(1, 0), (1, 1), (2, 1), (0, 6), (2, 5), (2, 6), (2, 7)]

        self.sandbox(points)

    def acorn(self):
        points = [(0, 1), (1, 3), (2, 0), (2, 1), (2, 4), (2, 5), (2, 6)]

        self.sandbox(points)

    def flint(self):
        points = [(2, 1), (2, 2), (2, 3), (1, 3), (1, 0)]

        self.sandbox(points)

    def ti(self):
        points = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                  (1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]

        self.sandbox(points)

    def __play(self):
        gen = 1
        first_gen = self.first_gen

        while True:
            print("\n")
            print(f"Generation: {gen}")
            next_gen = self.evolve(first_gen)
            string = ""

            for i in next_gen:
                string += "".join(map(lambda cell: str(cell), i)) + "\n"

            print(string)
            first_gen = next_gen
            gen += 1
            sleep(0.2)

    @staticmethod
    def neighbors(coordinates: tuple, length: int) -> List[Tuple[int]]:
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
            if (neighbor[0] < 0 or neighbor[0] >= length) or (neighbor[1] < 0 or neighbor[1] >= length):
                continue

            neighbors.append(neighbor)

        return neighbors


life = Life(60)

life.polsar()
