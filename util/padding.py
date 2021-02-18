import itertools


class BadPaddingException(Exception):
    def __init__(self, padSize):
        self.message = f"bad padding of size {padSize}"


def pkcs7Pad(bs, blockSize=16):
    assert blockSize < 256
    padded = bytearray(bs)
    padSize = blockSize - ((len(bs) + blockSize) % blockSize)
    padded.extend(itertools.repeat(padSize, padSize))
    return bytes(padded)


def pkcs7Strip(bs, blockSize=16):
    padSize = bs[-1]
    if padSize > blockSize or any(p != padSize for p in bs[-padSize:]):
        raise BadPaddingException(padSize)
    return bs[:-padSize]