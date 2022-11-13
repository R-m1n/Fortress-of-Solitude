from pprint import pprint
from typing import Any


class State():
    def __init__(self, label: set, next: dict = {}, start: bool = False, accept: bool = False) -> None:
        self.label = label
        self.next = next
        self.start = start
        self.accept = accept

    def setNext(self, label: str, move: str) -> None:
        self.next[move] = State(label)

    def move(move: str) -> object:
        return next[move]


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
        states = self.__prod(self.states, other.states)

        alphabet = self.alphabet

        delta = dict()
        for move in alphabet:
            for state in states:
                delta[((state[0], state[1]), move)] = (
                    self.next(state[0], move), other.next(state[1], move))

        start = (self.start, other.start)

        accept = self.__prod(self.accept, other.accept)

        return DFA(states, alphabet, delta, start, accept)

    def union(self, other):
        states = self.__prod(self.states, other.states)

        alphabet = self.alphabet

        delta = dict()
        for move in alphabet:
            for state in states:
                delta[((state[0], state[1]), move)] = (
                    self.next(state[0], move), other.next(state[1], move))

        start = (self.start, other.start)

        accept = self.__prod(self.accept, other.states).union(
            self.__prod(self.states, other.accept))

        return DFA(states, alphabet, delta, start, accept)

    def complement(self):
        accept = self.states.difference(self.accept)

        return DFA(self.states, self.alphabet, self.delta, self.start, accept)

    def __prod(self, set1: set, set2: set) -> set:
        result = set()

        for i in set1:
            for j in set2:
                result.add((i, j))

        return result


d1 = {('q1', 'a'): 'q2', ('q1', 'b'): 'q1',
      ('q2', 'a'): 'q2', ('q2', 'b'): 'q3',
      ('q3', 'a'): 'q3', ('q3', 'b'): 'q3'}

m1 = DFA({'q1', 'q2', 'q3'}, {'a', 'b'}, d1, 'q1', {'q3'})

m = m1.complement()

pprint(m.test("bbbbbbbbbaaab"))
