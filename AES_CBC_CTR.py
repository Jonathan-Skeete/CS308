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
    iv: bytes = get_random_bytes(16) # Initialization Vector: 16 bytes
    counter = Counter.new(128) # 128-bit counter
    
    @classmethod
    def validate_file(cls, input_file: str) -> None:
        if not os.path.exists(input_file): 
            raise FileNotFoundError('File not found') # Raise an exception if the file does not exist
    
    @classmethod
    def CBC(cls, input_file: str) -> None: # Cipher Block Chaining
        cls.validate_file(input_file) # Check if the file exists
        
        key = get_random_bytes(16) # Generate a random 16-byte key
            
        cipher = AES.new(key, AES.MODE_CBC, iv=cls.iv) # Create a new AES cipher object
        
        with open(input_file, 'rb') as f:
            plain_text: bytes = f.read() # plain_text is the content of the file
            if plain_text.startswith(b'ENCRYPTED'): # Check if the file is already encrypted
                cls.CBC_decrypt(input_file) # Decrypt the file if it is already encrypted
                return

        cipher_text = cipher.encrypt(pad(plain_text, AES.block_size)) # Pad the plain_text if padding is needed, then encrypt it

        with open(input_file, 'wb') as f:
            f.write(b'ENCRYPTED') # Write 'ENCRYPTED' to the file
            f.write(cipher.iv) # Write the IV to the file
            f.write(cipher_text) # Write the cipher_text to the file
            
        with open(f"key_{input_file.split('.')[0]}.txt", 'wb') as f:
            f.write(key) # Write the key to a file
            
            
    @classmethod 
    def CTR(cls, input_file: str) -> None:
        cls.validate_file(input_file) # Check if the file exists
        
        key = get_random_bytes(16) # Generate a random 16-byte key
            
        cipher = AES.new(key, AES.MODE_CTR, counter=cls.counter) # Create a new AES cipher object
        
        with open(input_file, 'rb') as f:
            plain_text: bytes = f.read() # plain_text is the content of the file
            if plain_text.startswith(b'ENCRYPTED'): # Check if the file is already encrypted
                cls.CTR_decrypt(input_file) # Decrypt the file if it is already encrypted
                return
            
        cipher_text = cipher.encrypt(plain_text) # Encrypt the key and counter, then XOR the result with the plain_text 
        
        with open(input_file, 'wb') as f:
            f.write(b'ENCRYPTED') # Write 'ENCRYPTED' to the file
            f.write(cipher_text) # Write the cipher_text to the file
            
        with open(f"key_{input_file.split('.')[0]}.txt", 'wb') as f:
            f.write(key) # Write the key to a file
    
    @classmethod
    def CBC_decrypt(cls, input_file: str) -> None:
        cls.validate_file(input_file) # Check if the file exists
        
        if not os.path.exists(f'key_{input_file.split(".")[0]}.txt'):
            raise FileNotFoundError('Key file not found') # Raise an exception if the key file does not exist
        
        with open(f'key_{input_file.split(".")[0]}.txt', 'rb') as f:
            key = f.read()
            
        with open(input_file, 'rb') as f:
            if f.read(9) != b'ENCRYPTED': # Check if the file is encrypted
                raise ValueError('File is not encrypted') # Raise an exception if the file is not encrypted
            iv = f.read(16) # Read the IV from the file
            cipher_text = f.read() # Read the cipher_text from the file
            
        cipher = AES.new(key, AES.MODE_CBC, iv=iv) # Create a new AES cipher object
        
        decrypted_plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size) # Decrypt the cipher_text and unpad the result if unpadding is needed

        with open(input_file, 'wb') as f:
            f.write(decrypted_plain_text) # Write the decrypted_plain_text to the file
            
        os.remove(f'key_{input_file.split(".")[0]}.txt') # Remove the key file
            
    @classmethod
    def CTR_decrypt(cls, input_file: str) -> None:
        cls.validate_file(input_file) # Check if the file exists
        
        if not os.path.exists(f'key_{input_file.split(".")[0]}.txt'):
            raise FileNotFoundError('Key file not found') # Raise an exception if the key file does not exist
        
        with open(f'key_{input_file.split(".")[0]}.txt', 'rb') as f:
            key = f.read() # Read the key from the file
        
        with open(input_file, 'rb') as f:
            if f.read(9) != b'ENCRYPTED': # Check if the file is encrypted
                raise ValueError('File is not encrypted') # Raise an exception if the file is not encrypted
            cipher_text = f.read() # Read the cipher_text from the file
        
        cipher = AES.new(key, AES.MODE_CTR, counter=cls.counter) # Create a new AES cipher object
        
        decrypted_plain_text = cipher.decrypt(cipher_text) # Decrypt the cipher_text by XORing it with the encrypted key and counter
        
        with open(input_file, 'wb') as f:
            f.write(decrypted_plain_text) # Write the decrypted_plain_text to the file
            
        os.remove(f'key_{input_file.split(".")[0]}.txt') # Remove the key file
        
        

def main() -> None:
    ...
    
if __name__ == '__main__':
    main()