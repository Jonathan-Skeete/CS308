from sys import argv
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class StaticClass(type):
    def __call__(cls):
        if cls is Encryption:
            raise TypeError('Cannot create an instance of a static class')

class Encryption(metaclass=StaticClass):
    iv: bytes = get_random_bytes(16)
    counter = Counter.new(128)
    
    @classmethod
    def get_key(cls) -> bytes:
        return input('Enter your 16, 24, or 32 byte key: ').encode()
    
    @classmethod
    def CBC(cls, input_file: str, key: bytes = None,) -> None:
        while (key is None) or (len(key) not in (16, 24, 32)):
            key = cls.get_key()
            
        cipher = AES.new(key, AES.MODE_CBC, iv=cls.iv)
        
        with open(input_file, 'rb') as f:
            plain_text: bytes = f.read() 

        cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))

        with open(f'CBC_{input_file.split(".")[0]}_cipher_text.txt', 'wb') as f:
            f.write(cipher.iv)
            f.write(cipher_text)
            
    @classmethod 
    def CTR(cls, input_file: str, key: bytes = None) -> None:
        while (key is None) or (len(key) not in (16, 24, 32)):
            key = cls.get_key()
            
        cipher = AES.new(key, AES.MODE_CTR, counter=cls.counter)
        
        with open(input_file, 'rb') as f:
            plain_text: bytes = f.read()
            
        cipher_text = cipher.encrypt(plain_text)
        
        with open(f'CTR_{input_file.split(".")[0]}_cipher_text.txt', 'wb') as f:
            f.write(cipher_text)
    
    @classmethod
    def CBC_decrypt(cls, cipher_file: str, key: bytes = None) -> None:
        while (key is None) or (len(key) not in (16, 24, 32)):
            key = cls.get_key()
            
        with open(cipher_file, 'rb') as f:
            iv = f.read(16)
            cipher_text = f.read()
            
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted_plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size)

        with open(f'decrypted_{cipher_file}.txt', 'wb') as f:
            f.write(decrypted_plain_text)
            
    @classmethod
    def CTR_decrypt(cls, cipher_file: str, key: bytes = None) -> None:
        while (key is None) or (len(key) not in (16, 24, 32)):
            key = cls.get_key()
            
        with open(cipher_file, 'rb') as f:
            cipher_text = f.read()
        
        cipher = AES.new(key, AES.MODE_CTR, counter=cls.counter)
        decrypted_plain_text = cipher.decrypt(cipher_text)
        
        with open(f'decrypted_{cipher_file}.txt', 'wb') as f:
            f.write(decrypted_plain_text)
        
            
    @classmethod        
    def decrypt(cls, cipher_file: str = None, key: bytes = None) -> None: 
        if cipher_file[:3] == 'CBC':
            cls.CBC_decrypt(cipher_file, key)
        elif cipher_file[:3] == 'CTR':
            cls.CTR_decrypt(cipher_file, key)
        
        
    

def main() -> None:
    ...
    Encryption.CTR('plain_text.txt', b'0123456789101112')
    Encryption.decrypt('CTR_plain_text_cipher_text.txt', b'0123456789101112')
    
if __name__ == '__main__':
    main()