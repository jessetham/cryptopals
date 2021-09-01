import operator

if __name__ == "__main__":
    bytes1 = bytes.fromhex("1c0111001f010100061a024b53535009181c")
    bytes2 = bytes.fromhex("686974207468652062756c6c277320657965")
    print(bytes(map(operator.xor, bytes1, bytes2)))
