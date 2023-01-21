

class Vector3():
    def __init__(self, x: int | float, y: int | float, z: int | float) -> None:
        self.x = x
        self.y = y
        self.z = z

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


v1 = Vector3(2, 4, 5)
v2 = Vector3(7, 2, 6)

print(v1 + v2)
