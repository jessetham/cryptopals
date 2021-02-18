from urllib import parse
from util import aes_helper, padding


def getCiphertext(userdata, encryptor):
    userdata = parse.quote(userdata)
    message = (
        b"comment1=cooking%20MCs;userdata="
        + bytes(userdata, "ascii")
        + b";comment2=%20like%20a%20pound%20of%20bacon"
    )
    message = padding.pkcs7Pad(message)
    return encryptor.update(message) + encryptor.finalize()


def isAdmin(ciphertext, decryptor):
    message = decryptor.update(ciphertext) + decryptor.finalize()
    message = padding.pkcs7Strip(message)
    print(message)
    return b";admin=true;" in message


def editCiphertext(userdata, ciphertext):
    ciphertext = bytearray(ciphertext)
    for i, u in zip(range(16), b";admin=true"):
        ciphertext[i + 16] = ciphertext[i + 16] ^ userdata[i] ^ u
    return bytes(ciphertext)


# Garbled block doesn't parse nicely into ascii.
# I am able to inject the target into the plaintext by manipulating the ciphertext though.
if __name__ == "__main__":
    cipher = aes_helper.getRandomCBCCipher()
    userdata = b"1" * 11
    ct = getCiphertext(userdata, cipher.encryptor())
    print(isAdmin(ct, cipher.decryptor()))
    ct = editCiphertext(userdata, ct)
    print(isAdmin(ct, cipher.decryptor()))