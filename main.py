from sys import argv
from Encryption import Encryption

def main() -> None:
    ...
    Encryption.CBC('plain_text.txt')
    # Encryption.CTR_decrypt('plain_text.txt')
if __name__ == '__main__':
    main()