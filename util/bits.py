import operator


def hammingDistance(bytes1, bytes2):
    xorResult = map(operator.xor, bytes1, bytes2)
    setBits = map(lambda x: bin(x).count("1"), xorResult)
    return sum(setBits)
