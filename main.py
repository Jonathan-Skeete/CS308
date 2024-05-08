from sys import argv
from Encryption import Encryption

def main() -> None:
    ...
    Encryption.CBC('plain_text.txt')
    Encryption.CTR('AES_CBC_CTR.py')
if __name__ == '__main__':
    main()