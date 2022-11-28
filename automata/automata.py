from pprint import pprint
from typing import Any


class DFA():
    def __init__(self, states: set, alphabet: set, delta: dict, start: str, accept: set) -> None:
        self.states = states
        self.alphabet = alphabet
        self.delta = delta
        self.start = start
        self.accept = accept

    def next(self, state: Any, move: str) -> Any:
        return self.delta[(state, move)]

    def test(self, string: str):
        state = self.start
        for move in string:
            state = self.next(state, move)

        return state in self.accept

    def intersection(self, other):
        states = self.prod(self.states, other.states)

        alphabet = self.alphabet

        delta = dict()
        for move in alphabet:
            for state in states:
                delta[((state[0], state[1]), move)] = (
                    self.next(state[0], move), other.next(state[1], move))

        start = (self.start, other.start)

        accept = self.prod(self.accept, other.accept)

        return DFA(states, alphabet, delta, start, accept)

    def union(self, other):
        states = self.prod(self.states, other.states)

        alphabet = self.alphabet

        delta = dict()
        for move in alphabet:
            for state in states:
                delta[((state[0], state[1]), move)] = (
                    self.next(state[0], move), other.next(state[1], move))

        start = (self.start, other.start)

        accept = self.prod(self.accept, other.states).union(
            self.prod(self.states, other.accept))

        return DFA(states, alphabet, delta, start, accept)

    def complement(self):
        accept = self.states.difference(self.accept)

        return DFA(self.states, self.alphabet, self.delta, self.start, accept)

    @staticmethod
    def prod(set1: set, set2: set) -> set:
        result = set()

        for i in set1:
            for j in set2:
                result.add((i, j))

        return result


d1 = {('q1', 'a'): 'q1', ('q1', 'b'): 'q1', ('q1', '#'): 'q1', ('q1', '/'): 'q2',
      ('q2', 'a'): 'q6', ('q2', 'b'): 'q6', ('q2', '#'): 'q3', ('q2', '/'): 'q6',
      ('q3', 'a'): 'q3', ('q3', 'b'): 'q3', ('q3', '#'): 'q4', ('q3', '/'): 'q3',
      ('q4', 'a'): 'q6', ('q4', 'b'): 'q6', ('q4', '#'): 'q4', ('q4', '/'): 'q5',
      ('q5', 'a'): 'q6', ('q5', 'b'): 'q6', ('q5', '#'): 'q3', ('q5', '/'): 'q2',
      ('q6', 'a'): 'q6', ('q6', 'b'): 'q6', ('q6', '#'): 'q6', ('q6', '/'): 'q6'}

m1 = DFA({'q1', 'q2', 'q3', 'q4', 'q5', 'q6'}, {
         'a', 'b', '/', '#'}, d1, 'q1', {'q5'})


input = "/#abaababbabababababab"
print(f"{input} => ", end="")
pprint(m1.test(input))
