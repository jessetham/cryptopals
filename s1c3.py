from util import english
import operator
from pprint import pprint

if __name__ == "__main__":
    ciphertext = bytes.fromhex(
        "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    )
    possibles = [
        bytes(map(lambda b: b ^ possibleKey, ciphertext)) for possibleKey in range(256)
    ]
    print(min(possibles, key=english.scoreText))
