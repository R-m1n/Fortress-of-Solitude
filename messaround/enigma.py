import string
import random


class Rotor:
    ALPHABET_SIZE = len(string.ascii_lowercase)

    def __init__(self, rotation: int = 0) -> None:
        self.alphabet = list(string.ascii_lowercase)
        self.cipher = self.alphabet.copy()
        random.shuffle(self.cipher)

        self.combination = dict(zip(self.alphabet, self.cipher))
        self.rotations = 0
        self.rotate(rotation)

    def rotate(self, n: int = 1):
        for rotation in range(n):
            self._count_rotation()
            self.cipher.insert(0, self.cipher.pop())

        self.combination = dict(zip(self.alphabet, self.cipher))

    def get(self, letter: str):
        return self.combination.get(letter)

    def _count_rotation(self):
        self.rotations += 1
        self.rotations %= self.ALPHABET_SIZE


class Enigma:
    def __init__(self, rotors: list[Rotor]) -> None:
        self.rotors = rotors


r1 = Rotor()
r2 = Rotor()
r3 = Rotor()
r4 = Rotor()
r5 = Rotor()

print(r1.cipher, end="\n\n")
r1.rotate(0)
print(r1.cipher)
print(r1.rotations)
