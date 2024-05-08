from sys import argv
from Encryption import Encryption

def main() -> None:
    ...
    if len(argv) == 2:
        Encryption.CTR(argv[1])
    else:
        raise ValueError('Invalid number of arguments')

if __name__ == '__main__':
    main()