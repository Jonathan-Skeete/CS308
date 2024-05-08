from sys import argv
from Encryption import Encryption

def main() -> None:
    ...
    if len(argv) == 2:
        Encryption.CTR(argv[1])

if __name__ == '__main__':
    main()