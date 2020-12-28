import collections

letterFrequenciesLowercase = {
    "e": 12.02,
    "t": 9.10,
    "a": 8.12,
    "o": 7.68,
    "i": 7.31,
    "n": 6.95,
    "s": 6.28,
    "r": 6.02,
    "h": 5.92,
    "d": 4.32,
    "l": 3.98,
    "u": 2.88,
    "c": 2.71,
    "m": 2.61,
    "f": 2.30,
    "y": 2.11,
    "w": 2.09,
    "g": 2.03,
    "p": 1.82,
    "b": 1.49,
    "v": 1.11,
    "k": 0.69,
    "x": 0.17,
    "q": 0.11,
    "j": 0.10,
    "z": 0.07,
}


def mse(observed, predicted):
    return sum(map(lambda o, p: (o - p) ** 2, observed, predicted)) / len(observed)


def scoreText(bs):
    # We only take into account English letters, but adding spaces and/or punctuation would probably help as well
    letters = filter(lambda b: 65 <= b <= 90 or 97 <= b <= 122, bs)
    letters = map(lambda b: chr(b).lower(), letters)
    count = collections.Counter(letters)
    # The idea behind dividing by the length of the input is that it will penalize counts that have
    # a small amount of ASCII letters compared to the input
    for c in count.keys():
        count[c] /= len(bs)
    observed = [count[c] for c in letterFrequenciesLowercase.keys()]
    return mse(observed, letterFrequenciesLowercase.values())