def decrypt_one_time_pad(ciphertext):
    # Convert ciphertext to bytes
    ciphertext_bytes = bytes(ciphertext, 'utf-8')
    
    # Store potential plaintexts with their corresponding key
    potential_plaintexts = []
    
    # Iterate over all printable ASCII characters
    for key in range(32, 127):
        # Decrypt using XOR
        decrypted = ''.join(chr(c ^ key) for c in ciphertext_bytes)
        potential_plaintexts.append((chr(key), decrypted))  # Store key and decrypted text
    
    return potential_plaintexts

ciphertext = "wAyk{mmAwjAuwpzAwmAqjn"
results = decrypt_one_time_pad(ciphertext)

# Print potential plaintexts with their corresponding OTP byte
for otp_byte, result in results:
    print(f"OTP Byte: '{otp_byte}' (ASCII: {ord(otp_byte)}) -> Decrypted Text: {result}")
