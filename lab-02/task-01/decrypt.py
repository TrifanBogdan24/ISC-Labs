#!/usr/bin/env python3


from Crypto.Cipher import AES

BLOCK_SIZE = 32
PADDING = b'#'
iv = b"\x00" * 16

def decrypt(key, iv, data):
    aes = AES.new(key, AES.MODE_CBC, iv)
    data = aes.decrypt(data)
    return data

def unpad(s):
    return s.rstrip(PADDING)

# Read the encrypted file
with open('isc-lab02-secret.enc', 'rb') as f:
    key = f.read(BLOCK_SIZE)  # Read the first 32 bytes (the key)
    enc_data = f.read()       # Read the rest (the encrypted data)

# Decrypt the data
decrypted_data = decrypt(key, iv, enc_data)

# Remove padding
unpadded_data = unpad(decrypted_data)

# Save the decrypted file
with open('decrypted.jpg', 'wb') as f_out:
    f_out.write(unpadded_data)

print("Decryption complete! The decrypted file is saved as 'decrypted.jpg'.")
