import math
from time import sleep
from turtle import *
from typing import List
import random


def factors(number: int) -> List[int]:
    list = []

    for i in range(1, number + 1):
        if number % i == 0:
            list.append(i)

    return list


def gcf(n1: int, n2: int):
    return max(set(factors(n1)).intersection(set(factors(n2))))


def polygon(sides: int = 4, sidelength: int = 100):
    for i in range(sides):
        forward(sidelength)
        right(360 // sides)


def star(sidelength: int = 100):
    for i in range(5):
        forward(sidelength)
        right(144)


def ninja_star(sidelength: int = 100):
    for i in range(12):
        forward(sidelength)
        right(150)


def sun(sidelength: int = 100):
    for i in range(30):
        forward(sidelength)
        right(156)


def wander():
    while True:
        forward(3)
        if xcor() >= 200 or xcor() <= -200 or ycor() <= -200 or ycor() >= 200:
            left(random.randint(90, 180))


def fib(limit: int):
    d = {0: 1, 1: 1}
    for i in range(2, limit + 1):
        d[i] = d[i - 1] + d[i - 2]

    return d


def rightangle(angle: int = 45, base: int = 100):
    h = base / math.cos(angle)
    f = h * math.sin(angle)
    forward(base)
    left(90)
    forward(f)
    left(180 - angle)
    forward(h)


def warp():
    sides = list(fib(16).values())[3:]
    colors = ['white', 'blue']
    for k in range(30):
        pencolor(colors[k % len(colors)])

        for j in range(6):
            for i in range(13):
                polygon(3, sides[i])

            right(60)

        right(2)


def weave():
    sides = list(fib(16).values())[3:]
    colors = ['white', 'blue']
    for k in range(17):
        pencolor(colors[k % len(colors)])

        for j in range(10):
            for i in range(8):
                star(sides[i])

            right(36)

        right(2)


speed('fastest')
bgcolor('white')

sides = list(fib(16).values())[3:]
colors = ['black', 'red']
for k in range(30):
    pencolor(colors[k % len(colors)])

    for j in range(6):
        for i in range(11):
            polygon(3, sides[i])

        right(60)

    right(2)


sleep(1000)
