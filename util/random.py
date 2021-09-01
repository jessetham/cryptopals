import dataclasses
from util.bits import lowestBits


@dataclasses.dataclass
class MTParams:
    w: int
    n: int
    m: int
    r: int
    a: int
    u: int
    d: int
    s: int
    b: int
    t: int
    c: int
    l: int
    f: int


class MT:
    def __init__(self, params: MTParams, seed: int):
        self.params = params
        self.index = params.n
        self.lowerMask = (1 << params.r) - 1
        self.upperMask = lowestBits(~self.lowerMask, params.w)
        self.state = [0] * params.n
        self.state[0] = seed
        for i in range(1, params.n):
            self.state[i] = lowestBits(
                params.f * (self.state[i - 1] ^ (self.state[i - 1] >> (params.w - 2)))
                + i,
                params.w,
            )

    def extract(self) -> int:
        if self.index == self.params.n:
            self.twist()

        y = self.state[self.index]
        y ^= (y >> self.params.u) & self.params.d
        y ^= (y << self.params.s) & self.params.b
        y ^= (y << self.params.t) & self.params.c
        y ^= y >> self.params.l

        self.index += 1
        return lowestBits(y, self.params.w)

    def twist(self):
        for i in range(self.params.n):
            x = (self.state[i] & self.upperMask) + (
                self.state[(i + 1) % self.params.n] & self.lowerMask
            )
            xA = x >> 1
            if x % 2 != 0:
                xA ^= self.params.a
            self.state[i] = self.state[(i + self.params.m) % self.params.n] ^ xA
        self.index = 0


class MT19937(MT):
    def __init__(self, seed: int = 5489):
        super().__init__(
            MTParams(
                *(32, 624, 397, 31),
                0x9908B0DF,
                *(11, 0xFFFFFFFF),
                *(7, 0x9D2C5680),
                *(15, 0xEFC60000),
                18,
                1812433253,
            ),
            seed,
        )


class MT19937_64(MT):
    def __init__(self, seed: int = 5489):
        super().__init__(
            MTParams(
                *(64, 312, 156, 31),
                0xB5026F5AA96619E9,
                *(29, 0x5555555555555555),
                *(17, 0x71D67FFFEDA60000),
                *(37, 0xFFF7EEE000000000),
                43,
                6364136223846793005,
            ),
            seed,
        )
