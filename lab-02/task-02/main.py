#!/usr/bin/env python3

import gmpy2
from sympy import factorint

# Given values
c = 28822365203577929536184039125870638440692316100772583657817939349051546473185
n = 70736025239265239976315088690174594021646654881626421461009089480870633400973
e = 3

# Step 1: Factor n into p and q
factors = factorint(n)

# Check if we have exactly two prime factors
if len(factors) != 2:
    raise ValueError("n does not have exactly two prime factors. Found: {}".format(factors))

# Extract p and q
p, q = list(factors.keys())

# Verify the factorization
if p * q != n:
    raise ValueError("p and q do not multiply to n. Check the factorization.")

# Step 2: Compute phi(n)
phi_n = (p - 1) * (q - 1)

# Check if e is coprime with phi(n)
if gmpy2.gcd(e, phi_n) != 1:
    raise ValueError(f"e ({e}) is not coprime with phi(n) ({phi_n}).")

# Step 3: Find d such that e * d ≡ 1 (mod phi(n))
d = gmpy2.invert(e, phi_n)

# Step 4: Decrypt the ciphertext
message = gmpy2.powmod(c, d, n)

# Convert the message from decimal to ASCII
# Ensure to convert the message to bytes
decoded_message = bytearray.fromhex(hex(message)[2:]).decode('utf-8', errors='ignore')

# Print the decrypted message
print("Decrypted message:", decoded_message)
