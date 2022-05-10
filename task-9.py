from enum import Enum


class State(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6


class StateMachine:
    state = State.A

    def throw(self):
        return self.update({
            State.A: [State.B, 0],
            State.B: [State.G, 3],
            State.C: [State.D, 4],
            State.D: [State.E, 5],
            State.E: [State.F, 6],
        })

    def peep(self):
        return self.update({
            State.A: [State.D, 1],
            State.B: [State.C, 2],
            State.E: [State.G, 7],
            State.F: [State.G, 8],
            State.G: [State.G, 9],
        })

    def update(self, transitions):
        self.state, signal = transitions[self.state]
        return signal


def main():
    o = StateMachine()
    return o

# o = StateMachine()
# o.throw() # 0
# o.peep() # 2
# o.throw() # 4
# #o.peep() # KeyError
# o.throw() # 5
# o.throw() # 6
# o.peep() # 8
# o.peep() # 9
# #o.throw() # KeyError
# o.peep() # 9
# o.peep() # 9
# o.peep() # 9
# o.peep() # 9
# o.peep() # 9
# o.peep() # 9
# o.peep() # 9