from time import sleep
from typing import List, Tuple
import numpy as np


class Life():
    def __init__(self, length) -> None:
        self.first_gen = np.zeros((length, length), np.int0)
        self.length = length

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

    def glider(self):
        self.first_gen[2 + 8][0 + 10] = 1
        self.first_gen[2 + 8][1 + 10] = 1
        self.first_gen[2 + 8][2 + 10] = 1
        self.first_gen[1 + 8][2 + 10] = 1
        self.first_gen[0 + 8][1 + 10] = 1

        self.__play()

    def skull(self):
        self.first_gen[2 + 8][1 + 10] = 1
        self.first_gen[2 + 8][2 + 10] = 1
        self.first_gen[2 + 8][3 + 10] = 1
        self.first_gen[1 + 8][3 + 10] = 1
        self.first_gen[1 + 8][0 + 10] = 1

        self.__play()

    def ti(self):
        self.first_gen[0 + 8][0 + 10] = 1
        self.first_gen[0 + 8][1 + 10] = 1
        self.first_gen[0 + 8][2 + 10] = 1
        self.first_gen[0 + 8][3 + 10] = 1
        self.first_gen[0 + 8][4 + 10] = 1
        self.first_gen[1 + 8][2 + 10] = 1
        self.first_gen[2 + 8][2 + 10] = 1
        self.first_gen[3 + 8][2 + 10] = 1
        self.first_gen[4 + 8][2 + 10] = 1
        self.first_gen[5 + 8][2 + 10] = 1

        self.__play()

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
            sleep(0.25)

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


life = Life()

life.ti()
