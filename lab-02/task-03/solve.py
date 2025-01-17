def decrypt_one_time_pad(ciphertext):
    for key in range(256):  # Iterate over all possible byte values
        decrypted = ''.join(chr(c ^ key) for c in ciphertext.encode('latin1'))  # XOR and decode
        if is_readable(decrypted):  # Check if the result is readable
            print(f"Key: {key}, Decrypted Text: {decrypted}")

def is_readable(text):
    # Check if text contains mostly printable characters
    return all(32 <= ord(c) <= 126 for c in text)

ciphertext = "wAyk{mmAwjAuwpzAwmAqjn"
decrypt_one_time_pad(ciphertext)
