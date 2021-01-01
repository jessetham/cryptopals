from util import aes_helper

if __name__ == "__main__":
    bb, name = aes_helper.generateBlackBox()
    print(f"AES mode: {name}")
    print(f"Guess: {aes_helper.oracle(bb)}")