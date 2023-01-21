
from math import sqrt
from pprint import pprint

from numpy import arccos


class Unit():
    def __init__(self, i: int | float, j: int | float, k: int | float) -> None:
        self.i = i
        self.j = j
        self.k = k

    def __str__(self) -> str:
        return f"Unit({self.i}, {self.j}, {self.k})"

    def __repr__(self) -> str:
        if self.j > 0 and self.k > 0:
            return f"{self.i}i + {self.j}j + {self.k}k"

        elif self.j < 0 and self.k > 0:
            return f"{self.i}i - {abs(self.j)}j + {self.k}k"

        elif self.j > 0 and self.k < 0:
            return f"{self.i}i + {self.j}j - {abs(self.k)}k"

        elif self.j < 0 and self.k < 0:
            return f"{self.i}i - {abs(self.j)}j - {abs(self.k)}k"


class Vector3():
    def __init__(self, x: int | float, y: int | float, z: int | float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def unit(self):
        return self * (1 / abs(self))

    def cross(self, other):
        i = (self.y * other.z) - (self.z * other.y)
        j = -((self.x * other.z) - (self.z * other.x))
        k = (self.x * other.y) - (self.y * other.x)

        return Vector3(i, j, k)

    def dist(self, other) -> float:
        return abs(Vector3(self.x - other.x, self.y - other.y, self.z - other.z))

    def angle(self, other) -> float:
        return arccos((self * other) / (abs(self) * abs(other)))

    def project(self, other):
        return other * ((self * other) / (other * other))

    def is_parallel(self, other):
        return (self.cross(other)).unit() == 0

    def is_perpendicular(self, other):
        return self * other == 0

    def __str__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

        elif isinstance(other, int) or isinstance(other, float):
            return Vector3(other * self.x, other * self.y, other * self.z)

    def __truediv__(self, other):
        if isinstance(other, Vector3):
            return self * (1 / abs(other))

        elif isinstance(other, int) or isinstance(other, float):
            return Vector3(self.x / other, self.y / other, self.z / other)

    def __eq__(self, other):
        return abs(self) == abs(other)

    def __ge__(self, other):
        return abs(self) >= abs(other)

    def __gt__(self, other):
        return abs(self) > abs(other)

    def __abs__(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))


v1 = Vector3(2, 4, 5)
v2 = Vector3(7, 2, 6)

pprint(v1 / v2)
