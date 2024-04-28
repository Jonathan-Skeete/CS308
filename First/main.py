from sys import argv
from Encryption import Encryption

def main() -> None:
    ...
    Encryption.CBC('plain_text.txt', b'0123456789101112')
    Encryption.decrypt('CBC_plain_text_cipher_text.txt', b'0123456789101112')
if __name__ == '__main__':
    main()