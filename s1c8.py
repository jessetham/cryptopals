import collections

if __name__ == "__main__":
    encoded = []
    with open("input.txt") as f:
        lines = f.read().splitlines()
        encoded.extend(map(bytes.fromhex, lines))

    # There's only one line that has duplicate blocks so it works out pretty nice
    for i, e in enumerate(encoded):
        counter = collections.Counter(e[i - 16 : i] for i in range(16, len(e), 16))
        mostCommon = counter.most_common()[0]
        if mostCommon[1] > 1:
            print("Line {}".format(i))
