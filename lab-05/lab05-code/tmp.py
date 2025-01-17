# Constants from the C code
S1 = b"7\xdf\xc3\xa9\x81,q\xe0j\xf7\x04\xa9\xf1\x83\x17\xf7\xf0\xb0 \x11"
S2 = b"\t\xfb\xf7\xa5\x91?d\xc8{\xb0\x01\x81\xf2\xc7\b\xdf\xf0\xf6\x39\x1b"

# Decrypt the flag
decrypted_flag = bytearray()
for i in range(len(S1)):
    decrypted_flag.append(S1[i] ^ S2[i])

# Convert to string
print(decrypted_flag.decode('utf-8'))
