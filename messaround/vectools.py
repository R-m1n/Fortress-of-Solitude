from math import sqrt, cos, sin

from numpy import arccos


class Vector3():
    def __init__(self, x: int | float, y: int | float, z: int | float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def unit(self):
        return self * (1 / abs(self))

    def cross(self, other):
        x = (self.y * other.z) - (self.z * other.y)
        y = -((self.x * other.z) - (self.z * other.x))
        z = (self.x * other.y) - (self.y * other.x)

        return Vector3(x, y, z)

    def dist(self, other) -> float:
        return abs(Vector3(self.x - other.x, self.y - other.y, self.z - other.z))

    def angle(self, other) -> float:
        return arccos((self * other) / (abs(self) * abs(other)))

    def project(self, other):
        return other * ((self * other) / (other * other))

    def is_parallel(self, other):
        return abs(self.cross(other)) == 0

    def is_perpendicular(self, other):
        return self * other == 0

    def triangle_area(self, other):
        return 0.5 * abs(self.cross(other))

    def parallelogram_area(self, other):
        return abs(self.cross(other)) if self.angle(self, other) != 0 else -1

    def parallelepiped_volume(self, other, another):
        return abs(another * (self.cross(other)))

    def prism_volume(self, other, another):
        return 0.5 * self.parallelepiped_volume(other, another)

    def pyramid_volume(self, other, another):
        return (1 / 6) * self.parallelepiped_volume(other, another)

    def x_rotate(self, theta: float):
        y = self.y * cos(theta) - self.z * sin(theta)
        z = self.y * sin(theta) - self.z * cos(theta)

        return Vector3(self.x, y, z)

    def y_rotate(self, theta: float):
        x = self.x * cos(theta) - self.z * sin(theta)
        z = -(self.x * sin(theta)) - self.z * cos(theta)

        return Vector3(x, self.y, z)

    def z_rotate(self, theta: float):
        x = self.x * cos(theta) - self.y * sin(theta)
        y = self.x * sin(theta) - self.y * cos(theta)

        return Vector3(x, y, self.z)

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


class Vector2(Vector3):
    def __init__(self, x: int | float, y: int | float) -> None:
        super().__init__(x, y, 0)

    def rotate(self, theta):
        x = self.x * cos(theta) - self.y * sin(theta)
        y = self.x * sin(theta) + self.y * cos(theta)

        return Vector2(x, y)
