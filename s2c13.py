import random
from urllib.parse import parse_qs, urlencode

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from util import padding


def initializeCipher():
    cipher = Cipher(algorithms.AES(random.randbytes(16)), modes.ECB())

    def e(plaintext):
        encryptor = cipher.encryptor()
        return encryptor.update(padding.pkcs7Pad(plaintext, 16)) + encryptor.finalize()

    def d(ciphertext):
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()

    return e, d


def initializeProfileFor(encrypt):
    def profileFor(email):
        profile = bytes(urlencode({"email": email, "uid": 10, "role": "user"}), "utf-8")
        return encrypt(profile)

    return profileFor


# I'm not sure how to pass PKCS#7 padding with admin through urlencode or if there's a better spot to cut and paste.
# Still works with parse_qs though.
def cutAndPasteAttackECB(profileFor):
    # Craft an email input that leaves the value of the "role" key in its own block
    firstEmail = "a" * 13
    firstProfile = profileFor(firstEmail)

    # Craft another email input that leaves "admin" to start the second block.
    secondEmail = "a" * 10 + "admin"
    secondProfile = profileFor(secondEmail)

    # Replace the last block that only contains "user" in the first profile with the "admin" block in the second profile
    return firstProfile[:32] + secondProfile[16:32]


if __name__ == "__main__":
    e, d = initializeCipher()
    profileFor = initializeProfileFor(e)

    edited = cutAndPasteAttackECB(profileFor)
    decryptedEdited = d(edited).decode("utf-8")
    print(decryptedEdited)
    print(parse_qs(decryptedEdited))
