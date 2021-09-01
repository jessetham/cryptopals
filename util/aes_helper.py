import collections
from random import choice, randbytes, randint

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from util import padding

# This stuff really only uses CBC or ECB mode


def generateBlackBox():
    mode = choice([modes.ECB(), modes.CBC(randbytes(16))])
    cipher = Cipher(
        algorithms.AES(randbytes(16)),
        mode,
    )

    def bb(bs):
        encryptor = cipher.encryptor()
        plaintext = padding.pkcs7Pad(
            randbytes(randint(5, 10)) + bs + randbytes(randint(5, 10)), 16
        )
        return encryptor.update(plaintext) + encryptor.finalize()

    return bb, mode.name


def oracle(bb):
    plaintext = b"a" * 128
    ciphertext = bb(plaintext)
    counter = collections.Counter(
        ciphertext[i - 16 : i] for i in range(16, len(ciphertext), 16)
    )
    return "ECB" if max(counter.values()) > 1 else "CBC"


def getCBCCipher(key=randbytes(16), iv=randbytes(16)):
    assert len(key) == len(iv)
    return Cipher(algorithms.AES(key), modes.CBC(iv))
