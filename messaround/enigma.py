import string


class Rotor:
    ALPHABET_SIZE = len(string.ascii_lowercase)

    def __init__(self, alternative: str, rotation: int = 0) -> None:
        self.alphabet = list(string.ascii_lowercase)
        self.alternative = list(alternative)

        self.rotations = 0

        self.rotate(rotation)

    def rotate(self, rotation: int = 1):
        for n in range(rotation):
            self._count_rotation()
            self.alternative.append(self.alternative.pop(0))

        self.combination = dict(zip(self.alphabet, self.alternative))

    def get(self, letter: str, reverse: bool = False):
        return self.combination.get(letter, "#") if not reverse else dict(zip(self.alternative, self.alphabet)).get(letter, "#")

    def _count_rotation(self):
        self.rotations += 1
        self.rotations %= self.ALPHABET_SIZE


class Plugboard:
    def __init__(self, alternative: str) -> None:
        self.alphabet = list(string.ascii_lowercase)
        self.alternative = list(alternative)

        self.combination = dict(zip(self.alphabet, self.alternative))
        self.reverse_combination = dict(zip(self.alternative, self.alphabet))

    def get(self, letter: str, reverse: bool = False):
        return self.combination.get(letter, "#") if not reverse else self.reverse_combination.get(letter, "#")


class Enigma:
    def __init__(self, rotor_1: Rotor, rotor_2: Rotor, rotor_3: Rotor, plugboard: Plugboard) -> None:
        self.rotor_1 = rotor_1
        self.rotor_2 = rotor_2
        self.rotor_3 = rotor_3

        self.plugboard = plugboard

        self.reflector = dict(zip(list(string.ascii_lowercase),
                                  list(string.ascii_lowercase[::-1])))

    def convert(self, text: str):
        cipher = ""
        for letter in text:
            cipher += self._encode(letter)
            self._rotate()

        return cipher

    def _encode(self, letter: str):
        letter = letter.lower()

        encoded = self.plugboard.get(letter)

        encoded = self.rotor_1.get(encoded)
        encoded = self.rotor_2.get(encoded)
        encoded = self.rotor_3.get(encoded)

        encoded = self.reflector.get(encoded)

        encoded = self.rotor_3.get(encoded, reverse=True)
        encoded = self.rotor_2.get(encoded, reverse=True)
        encoded = self.rotor_1.get(encoded, reverse=True)

        encoded = self.plugboard.get(encoded, reverse=True)

        return encoded

    def _rotate(self):
        self.rotor_1.rotate()

        if self.rotor_1.rotations == 0:
            self.rotor_2.rotate()

            if self.rotor_2.rotations == 0:
                self.rotor_3.rotate()
