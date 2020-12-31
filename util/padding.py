import itertools


def pkcs7Pad(bs, blockSize):
    assert blockSize < 256
    padded = bytearray(bs)
    padSize = blockSize - ((len(bs) + blockSize) % blockSize)
    padded.extend(itertools.repeat(padSize, padSize))
    return bytes(padded)


def pkcs7Strip(bs):
    padSize = bs[-1]
    return bs[:-padSize]