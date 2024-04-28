from sys import argv
from Crypto.Cipher import AES
import random
from string import printable, hexdigits as hx

def XOR(a: str, b: str) -> str:
    result: str = ""
    for i in range(len(a)):
        result += "1" if a[i] != b[i] else "0"
    return result

def toBinary(text: str) -> str:
    result: str = ""
    for c in text:
        result += format(ord(c), '08b')
    return result

def binToText(binary: str) -> str:
    result: str = ""
    for i in range(0, len(binary), 8):
        result += chr(int(binary[i:i+8], 2))
    return result

def Encrypt(plain_text: str, key: str) -> str:
    m: int = 16 - len(plain_text) % 16
    pad = hx[m % 16] * (m % 16)
    plain_text = f"{plain_text}{pad}"
    
    pool = printable 
    iv = "".join(random.choices(pool, k=16))
    
    pre_cipher: str = toBinary(iv)
    
    for i in range(0, len(plain_text), 16):
        block = plain_text[i:i+16]
        block = toBinary(block)
        pre_cipher += XOR(block, pre_cipher[i*8:i*8+128])
    
    cipher = binToText(pre_cipher)
    print(cipher)
    
    
    
    

def main() -> None:
    ...
    Encrypt("Hello World", "key")
    
    # pool = printable
    # iv = "".join(random.choices(pool, k=16))
    # print(iv)
    # print(len(iv))
    # print(bin(ord('z')))
    # print(toBinary("AA"))
    # print(binToText("0100000101000001"))
        
if __name__ == '__main__':
    main()