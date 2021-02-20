import base64
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms


def ctr(ciphertext, key, nonce):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    res = bytearray()
    for i, b in enumerate(range(0, len(ciphertext), 16)):
        encryptor = cipher.encryptor()
        keystream = (
            encryptor.update(
                nonce.to_bytes(8, byteorder="little")
                + i.to_bytes(8, byteorder="little")
            )
            + encryptor.finalize()
        )
        res.extend(c ^ k for c, k in zip(ciphertext[b : b + 16], keystream))
    return bytes(res)


if __name__ == "__main__":
    target = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    target = base64.b64decode(target)

    print(ctr(target, b"YELLOW SUBMARINE", 0))