import operator
import base64
import itertools

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from util import padding


def cbcDecryptUsingEcb(plaintext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    plaintext = padding.pkcs7Pad(plaintext, len(key))
    prev = iv
    blocks = [
        plaintext[i - len(key) : i] for i in range(len(key), len(plaintext), len(key))
    ]
    decoded = []
    for block in blocks:
        decryptor = cipher.decryptor()
        decoded.append(
            bytes(
                map(operator.xor, decryptor.update(block) + decryptor.finalize(), prev)
            )
        )
        prev = block
    return padding.pkcs7Strip(b"".join(decoded))


if __name__ == "__main__":
    fileContents = []
    with open("input.txt") as f:
        lines = f.read().splitlines()
        fileContents.extend(map(base64.b64decode, lines))
    fileContents = b"".join(fileContents)
    key = b"YELLOW SUBMARINE"
    print(cbcDecryptUsingEcb(fileContents, key, b"0" * len(key)))
