from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Create a random 128-bit key
key = get_random_bytes(16)

# Create AES cipher object
cipher = AES.new(key, AES.MODE_ECB)

# Encrypt a 128-bit block of data
plaintext = b'0123456789101112'
ciphertext = cipher.encrypt(plaintext)

# Decrypt the ciphertext
decrypted_text = cipher.decrypt(ciphertext)

print("Original:", type(plaintext))
print("Encrypted:", ciphertext)
print("Decrypted:", decrypted_text)
