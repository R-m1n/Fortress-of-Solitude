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
        self.reverse_combination = dict(zip(self.cipher, self.alphabet))

        self.rotations = 0
        self.rotate(rotation)

    def rotate(self, n: int = 1):
        for rotation in range(n):
            self._count_rotation()
            self.cipher.append(self.cipher.pop(0))

        self.combination = dict(zip(self.alphabet, self.cipher))

    def get(self, letter: str):
        return self.combination.get(letter)

    def reverse(self, letter: str):
        return self.reverse_combination.get(letter)

    def _count_rotation(self):
        self.rotations += 1
        self.rotations %= self.ALPHABET_SIZE


class Enigma:
    def __init__(self, rotors: list[Rotor]) -> None:
        self.rotors = rotors
        self.reflector = dict(zip(list(string.ascii_lowercase),
                                  list(string.ascii_lowercase[::-1])))

    def encode(self, char: str):
        char = char.lower()

        encoded = self.rotors[0].get(char)
        encoded = self.rotors[1].get(encoded)
        encoded = self.rotors[2].get(encoded)

        encoded = self.reflect(encoded)

        encoded = self.rotors[2].reverse(encoded)
        encoded = self.rotors[1].reverse(encoded)
        encoded = self.rotors[0].reverse(encoded)

        self.rotors[0].rotate()

        if self.rotors[0].rotations == 0:
            self.rotors[1].rotate()

            if self.rotors[1].rotations == 0:
                self.rotors[2].rotate()

        return encoded

    def enigma(self, text):
        cipher = ""
        for char in text:
            cipher += self.encode(char)

        return cipher

    def reflect(self, letter):
        return self.reflector.get(letter)


rotor_list = [Rotor(), Rotor(), Rotor()]
rotor_list1 = copy.deepcopy(rotor_list)

e1 = Enigma(rotor_list)

result = e1.enigma("hihi")

e2 = Enigma(rotor_list1)

print(result)
print(e2.enigma(result))
