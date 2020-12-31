from util import padding

if __name__ == "__main__":
    initial = b"YELLOW SUBMARINE"
    padded = padding.pkcs7Pad(initial, 20)

    print(padded)
    assert padded == b"YELLOW SUBMARINE\x04\x04\x04\x04"
