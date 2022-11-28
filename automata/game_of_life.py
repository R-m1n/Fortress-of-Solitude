from time import sleep
from typing import List, Tuple
import numpy as np


def neighbors(coordinates: tuple, row_length: int) -> List[Tuple[int]]:
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
        if (neighbor[0] < 0 or neighbor[0] >= row_length) or (neighbor[1] < 0 or neighbor[1] >= row_length):
            continue

        neighbors.append(neighbor)

    return neighbors


def evolve(first_gen: List[List[int]]) -> List[List[int]]:
    length = len(first_gen)
    next_gen = np.zeros((length, length), np.int0)
    alive, dead = 1, 0

    for row in range(length):
        for column in range(length):
            cell = first_gen[row][column]
            coordinates = (row, column)
            alive_neighbors = 0

            for neighbor in neighbors(coordinates, length):
                if first_gen[neighbor[0]][neighbor[1]] == alive:
                    alive_neighbors += 1

            if cell == dead:
                if alive_neighbors == 0 or alive_neighbors == 1 or alive_neighbors == 2:
                    next_gen[row][column] = dead

                elif alive_neighbors == 3:
                    next_gen[row][column] = alive

            if cell == alive:
                if alive_neighbors == 0 or alive_neighbors == 1:
                    next_gen[row][column] = dead

                elif alive_neighbors == 2 or alive_neighbors == 3:
                    next_gen[row][column] = alive

                elif alive_neighbors > 3:
                    next_gen[row][column] = dead

    return next_gen


first_gen = np.zeros((25, 25), np.int0)

first_gen[2 + 8][0 + 10] = 1
first_gen[2 + 8][1 + 10] = 1
first_gen[2 + 8][2 + 10] = 1
first_gen[1 + 8][2 + 10] = 1
first_gen[0 + 8][1 + 10] = 1

# first_gen[2 + 8][1 + 10] = 1
# first_gen[2 + 8][2 + 10] = 1
# first_gen[2 + 8][3 + 10] = 1
# first_gen[1 + 8][3 + 10] = 1
# first_gen[1 + 8][0 + 10] = 1

# first_gen[0 + 20][0 + 22] = 1
# first_gen[0 + 20][1 + 22] = 1
# first_gen[0 + 20][2 + 22] = 1
# first_gen[0 + 20][3 + 22] = 1
# first_gen[0 + 20][4 + 22] = 1
# first_gen[1 + 20][2 + 22] = 1
# first_gen[2 + 20][2 + 22] = 1
# first_gen[3 + 20][2 + 22] = 1
# first_gen[4 + 20][2 + 22] = 1
# first_gen[5 + 20][2 + 22] = 1


gen = 1
while True:
    print("\n")
    print(f"Generation: {gen}")
    next_gen = evolve(first_gen)
    string = ""

    for i in next_gen:
        string += "".join(map(lambda cell: str(cell), i)) + "\n"

    print(string)
    first_gen = next_gen
    gen += 1
    sleep(0.25)
