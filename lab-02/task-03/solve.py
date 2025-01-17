# TODO


# Define the ciphertext
ciphertext = b'wAyk{mmAwjAuwpz\x7fAwmAqjn'

# Function to decrypt using a single-byte key
def decrypt_with_key(ciphertext, key):
    return bytes([ord(c) ^ key for c in ciphertext])

# Iterate through all possible single-byte keys
for key in range(256):
    decrypted_message = decrypt_with_key(ciphertext, key)
    print(f"Key: {key} | Decrypted Message: {decrypted_message.decode('latin-1')}")
