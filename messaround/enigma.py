import string
import random

import copy


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
            self.cipher.append(self.cipher.pop(0))

        self.combination = dict(zip(self.alphabet, self.cipher))

    def get(self, letter: str, reverse: bool = False):
        return self.combination.get(letter) if not reverse else dict(zip(self.cipher, self.alphabet)).get(letter)

    def _count_rotation(self):
        self.rotations += 1
        self.rotations %= self.ALPHABET_SIZE


class Enigma:
    def __init__(self, rotors: list[Rotor]) -> None:
        self.rotor_1 = rotors[0]
        self.rotor_2 = rotors[1]
        self.rotor_3 = rotors[2]

        self.reflector = dict(zip(list(string.ascii_lowercase),
                                  list(string.ascii_lowercase[::-1])))

    def convert(self, text: str):
        cipher = ""
        for char in text:
            cipher += self._encode(char)
            self._rotate()

        return cipher

    def _encode(self, char: str):
        char = char.lower()

        encoded = self.rotor_1.get(char)
        encoded = self.rotor_2.get(encoded)
        encoded = self.rotor_3.get(encoded)

        encoded = self.reflector.get(encoded)

        encoded = self.rotor_3.get(encoded, True)
        encoded = self.rotor_2.get(encoded, True)
        encoded = self.rotor_1.get(encoded, True)

        return encoded

    def _rotate(self):
        self.rotor_1.rotate()

        if self.rotor_1.rotations == 0:
            self.rotor_2.rotate()

            if self.rotor_2.rotations == 0:
                self.rotor_3.rotate()


rotor_list = [Rotor(), Rotor(), Rotor()]
rotor_list1 = copy.deepcopy(rotor_list)

e1 = Enigma(rotor_list)

result = e1.convert("armin")

e2 = Enigma(rotor_list1)

print(result)
print(e2.convert(result))
