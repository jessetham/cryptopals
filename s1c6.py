from util import bits, english
import base64
import statistics
from pprint import pprint
import operator
import itertools
from string import ascii_letters, punctuation, whitespace


def calculateNormalizedDistance(bs, keysize):
    chunks = [bs[i : i + keysize] for i in range(0, len(bs), keysize)]
    return statistics.mean(
        bits.hammingDistance(chunks[i - 1], chunks[i]) / keysize
        for i in range(1, len(chunks), 2)
    )


if __name__ == "__main__":
    text = []
    with open("input.txt") as f:
        lines = f.read().splitlines()
        text.extend(map(base64.b64decode, lines))
    combined = b"".join(text)

    # First, get the key size
    normalizedDistances = [
        (possibleKeysize, calculateNormalizedDistance(combined, possibleKeysize))
        for possibleKeysize in range(2, 41)
    ]

    # Then, use that keysize to get the characters
    keysize = min(normalizedDistances, key=lambda d: d[1])[0]
    blocks = [combined[i - keysize : i] for i in range(keysize, len(combined), keysize)]
    transpose = [bytes(block[i] for block in blocks) for i in range(keysize)]
    chars = [
        min(
            ascii_letters + whitespace + punctuation,
            key=lambda k: english.scoreText(bytes(map(lambda b: b ^ ord(k), t))),
        )
        for t in transpose
    ]
    # It's kind of garbled but still understandable
    print("".join(chars))
