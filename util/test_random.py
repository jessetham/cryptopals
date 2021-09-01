import unittest
import random
from .random import MT19937, MT19937_64

# Tests based on example given in https://en.cppreference.com/w/cpp/numeric/random/mersenne_twister_engine
class TestMT19937(unittest.TestCase):
    def test_extract(self):
        mt = MT19937(5489)
        for _ in range(9999):
            mt.extract()
        self.assertEqual(mt.extract(), 4123659995)


class TestMT19937_64(unittest.TestCase):
    def test_extract(self):
        mt = MT19937_64(5489)
        for _ in range(9999):
            mt.extract()
        self.assertEqual(mt.extract(), 9981545732273789042)


if __name__ == "__main__":
    unittest.main()
