import base64
import random
from collections import deque

from util import aes_helper, padding

texts = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]


def oracle(decryptor, ciphertext):
    try:
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()
        padding.pkcs7Strip(decrypted)
    except padding.BadPaddingException:
        return False
    return True


def backtrack(cipher, current, previous, prefix, guessed, padSize):
    if len(guessed) == 16:
        return True
    res = False
    for g in range(256):
        parr = bytearray(previous)
        parr[16 - padSize] = parr[16 - padSize] ^ g ^ padSize
        for j, gu in zip(range(16 - padSize + 1, 16), guessed):
            parr[j] = parr[j] ^ gu ^ padSize
        if oracle(cipher.decryptor(), prefix + bytes(parr) + current):
            guessed.appendleft(g)
            if backtrack(cipher, current, previous, prefix, guessed, padSize + 1):
                res = True
                break
            guessed.popleft()
    return res


def encrypt(encryptor, text):
    # The CBC cipher from the cryptography library passes the IV into the cipher,
    # which makes it tough to edit it for the padding attack. We're just going to
    # prepend the message with a fake IV.
    iv = random.randbytes(16)
    message = padding.pkcs7Pad(iv + text)
    return encryptor.update(message) + encryptor.finalize()


def attack(cipher, ciphertext):
    result = b""
    for i in range(16, len(ciphertext), 16):
        guessed = deque([])
        backtrack(
            cipher,
            ciphertext[i : i + 16],
            ciphertext[i - 16 : i],
            ciphertext[: i - 16],
            guessed,
            1,
        )
        result += bytes(guessed)
    return padding.pkcs7Strip(result)


if __name__ == "__main__":
    cipher = aes_helper.getCBCCipher()
    texts = [base64.b64decode(t) for t in texts]
    ciphertexts = [encrypt(cipher.encryptor(), t) for t in texts]
    results = [attack(cipher, c) for c in ciphertexts]
    for t, r in zip(texts, results):
        assert t == r
