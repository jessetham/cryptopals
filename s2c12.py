import base64
import random

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from util import aes_helper, padding


def randomKeyEncryptor():
    cipher = Cipher(algorithms.AES(random.randbytes(16)), modes.ECB())

    def bb(message):
        encryptor = cipher.encryptor()
        return encryptor.update(message) + encryptor.finalize()

    return bb


def chosenPlaintextAttackECB(encryptor, unknownMessage):
    result = bytearray()
    ciphertexts = [
        encryptor(padding.pkcs7Pad((b"a" * (16 - i - 1)) + unknownMessage, 16))
        for i in range(16)
    ]
    for i in range(len(unknownMessage)):
        blockIdx = 16 * (i // 16)
        block = ciphertexts[i % 16][blockIdx : blockIdx + 16]
        prefix = (
            bytes(result[-15:]) if len(result) >= 15 else bytes(result).rjust(15, b"a")
        )
        mapping = {encryptor(prefix + bytes([j])): j for j in range(256)}
        result.append(mapping[block])
    return bytes(result)


if __name__ == "__main__":
    unknownMessage = []
    with open("input.txt") as f:
        lines = f.read().splitlines()
        unknownMessage.extend(map(base64.b64decode, lines))
    unknownMessage = b"".join(unknownMessage)
    encryptor = randomKeyEncryptor()

    # Determine block size by finding the first input that produces a consistent output
    # for i in range(1, 20):
    #     print(f"{i} -> {encryptor(b'a' * i)}")

    # Determine that the encryptor is using ECB mode
    # assert aes_helper.oracle(encryptor) == "ECB"

    resultingMessage = chosenPlaintextAttackECB(encryptor, unknownMessage)
    assert resultingMessage == unknownMessage
    print(resultingMessage)
