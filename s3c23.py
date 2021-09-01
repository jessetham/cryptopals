from util.random import MTParams
from z3 import *
from util.random import MT19937, MTParams

# I got the idea to use Z3 from https://www.schutzwerk.com/en/43/posts/attacking_a_random_number_generator/
# This probably isn't what the challenge had in mind but I wanted to try using Z3.
def untwist(out: int, params: MTParams) -> int:
    initial = BitVec("initial", 32)
    y1 = BitVec("y1", 32)
    y2 = BitVec("y2", 32)
    y3 = BitVec("y3", 32)
    final = BitVecVal(out, 32)
    equations = [
        y1 == initial ^ (LShR(initial, params.u) & params.d),
        y2 == y1 ^ ((y1 << params.s) & params.b),
        y3 == y2 ^ ((y2 << params.t) & params.c),
        final == y3 ^ LShR(y3, params.l),
    ]

    solver = Solver()
    solver.add(equations)
    solver.check()
    res = solver.model()[initial]
    return res.as_long()


if __name__ == "__main__":
    mt = MT19937()
    outputs = [mt.extract() for _ in range(624)]
    state = mt.state.copy()

    untwisted = [untwist(out, mt.params) for out in outputs]
    assert state == untwisted

    splicedmt = MT19937(seed=1)
    splicedmt.state = untwisted
    assert all([mt.extract() == splicedmt.extract() for _ in range(100)])
