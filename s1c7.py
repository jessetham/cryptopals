from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64

if __name__ == "__main__":
    ciphertext = []
    with open("input.txt") as f:
        lines = f.read().splitlines()
        ciphertext.extend(map(base64.b64decode, lines))
    key = bytes("YELLOW SUBMARINE", "utf-8")
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    print(decryptor.update(b"".join(ciphertext)) + decryptor.finalize())
