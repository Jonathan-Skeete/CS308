from sys import argv
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

class StaticClass(type):
    def __call__(cls):
        if cls is Encryption:
            raise TypeError('Cannot create an instance of a static class')

class Encryption(metaclass=StaticClass):
    iv: bytes = get_random_bytes(16)
    counter = Counter.new(128)
    
    @classmethod
    def validate_file(cls, input_file: str) -> None:
        if not os.path.exists(input_file):
            raise FileNotFoundError('File not found')
    
    @classmethod
    def CBC(cls, input_file: str) -> None:
        cls.validate_file(input_file)
        
        key = get_random_bytes(16)
            
        cipher = AES.new(key, AES.MODE_CBC, iv=cls.iv)
        
        with open(input_file, 'rb') as f:
            plain_text: bytes = f.read()
            if plain_text.startswith(b'ENCRYPTED'):
                cls.CBC_decrypt(input_file)
                return

        cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))

        with open(input_file, 'wb') as f:
            f.write(b'ENCRYPTED')
            f.write(cipher.iv)
            f.write(cipher_text)
            
        with open(f"key_{input_file.split('.')[0]}.txt", 'wb') as f:
            f.write(key)
            
            
    @classmethod 
    def CTR(cls, input_file: str) -> None:
        cls.validate_file(input_file)
        
        key = get_random_bytes(16)
            
        cipher = AES.new(key, AES.MODE_CTR, counter=cls.counter)
        
        with open(input_file, 'rb') as f:
            plain_text: bytes = f.read()
            if plain_text.startswith(b'ENCRYPTED'):
                cls.CTR_decrypt(input_file)
                return
            
        cipher_text = cipher.encrypt(plain_text)
        
        with open(input_file, 'wb') as f:
            f.write(b'ENCRYPTED')
            f.write(cipher_text)
            
        with open(f"key_{input_file.split('.')[0]}.txt", 'wb') as f:
            f.write(key)
    
    @classmethod
    def CBC_decrypt(cls, input_file: str) -> None:
        cls.validate_file(input_file)
        
        if not os.path.exists(f'key_{input_file.split(".")[0]}.txt'):
            raise FileNotFoundError('Key file not found')
        
        key = None
        
        with open(f'key_{input_file.split(".")[0]}.txt', 'rb') as f:
            key = f.read()
            
        with open(input_file, 'rb') as f:
            if f.read(9) != b'ENCRYPTED':
                raise ValueError('File is not encrypted')
            iv = f.read(16)
            cipher_text = f.read()
            
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        
        decrypted_plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size)

        with open(input_file, 'wb') as f:
            f.write(decrypted_plain_text)
            
        os.remove(f'key_{input_file.split(".")[0]}.txt')
            
    @classmethod
    def CTR_decrypt(cls, input_file: str) -> None:
        cls.validate_file(input_file)
        
        if not os.path.exists(f'key_{input_file.split(".")[0]}.txt'):
            raise FileNotFoundError('Key file not found')
        
        key = None
        
        with open(f'key_{input_file.split(".")[0]}.txt', 'rb') as f:
            key = f.read()
        
        with open(input_file, 'rb') as f:
            if f.read(9) != b'ENCRYPTED':
                raise ValueError('File is not encrypted')
            cipher_text = f.read()
        
        cipher = AES.new(key, AES.MODE_CTR, counter=cls.counter)
        
        decrypted_plain_text = cipher.decrypt(cipher_text)
        
        with open(input_file, 'wb') as f:
            f.write(decrypted_plain_text)
            
        os.remove(f'key_{input_file.split(".")[0]}.txt')
        
        

def main() -> None:
    ...
    
if __name__ == '__main__':
    main()