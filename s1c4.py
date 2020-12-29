from util import english

if __name__ == "__main__":
    input = []
    with open("input.txt") as f:
        input.extend(map(bytes.fromhex, f.read().splitlines()))

    possibles = map(
        lambda ciphertext: min(
            [
                bytes(map(lambda b: b ^ possibleKey, ciphertext))
                for possibleKey in range(256)
            ],
            key=english.scoreText,
        ),
        input,
    )
    print(min(possibles, key=english.scoreText))