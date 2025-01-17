# Lab 02 - Cryptography

## Task 00 | AES ECB (warm up)

Am folosit un editor online de `hexedit`
si am inlocuit head-ul fisierului din arhiva
si header-ul corect pentru o imagine `.bmp`.

Cu https://hexed.it/, a mers sa dau direct drag-and-drop
la fisier din folder in site, iar apoi, in comparatia cu tool-ul CLI,
am editat omeneste octetii.


```
42 4D 66 CA D7 00 00 00 00 00 36 00 00 00 28 00 00 00 D0 07 00 00 35 09 00 00 01 00 18 00 00 00 00 00 30 CA D7 00 74 12 00 00 74 12 00 00 00 00 00 00 00 00 00 00
```

Pasi pt https://hexed.it/:
- Copy paste la octetii de mai sus
- Am pus frumos cursorul pe primul numar 
- **CTRL V**
- Am ales "overwrite the bytes at the cursor position" (actiunea)
- Am ales "Hexadecima Values" (formatul datelor)



## Task 01 | AES

Fisierul criptat cu:

```py
from Crypto.Cipher import AES
from Crypto import Random
 
BLOCK_SIZE = 32
PADDING = b'#'
iv = b"\x00" * 16
 
def encrypt(key, iv, data):
    aes = AES.new(key, AES.MODE_CBC, iv)
    data = aes.encrypt(data)
    return data
 
def pad(s):
    return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING 
 
 
key = Random.new().read(BLOCK_SIZE)
 
with open('plain.jpg', 'rb') as f:
    data = f.read()
 
enc = encrypt(key, iv, pad(data))
 
f_out = open("secret.enc", 'wb')
f_out.write(key)
f_out.write(enc)
f_out.close()
```


Se decripteaza cu:

```py
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
```



## Task 02 | RSA - Known factorisation



```
c = 28822365203577929536184039125870638440692316100772583657817939349051546473185
n = 70736025239265239976315088690174594021646654881626421461009089480870633400973
e = 3
```

Conform [FactorDB](https://factordb.com/),
n poate fi scris ca produs intre doua numere `n = p * q`, unde:
```
p = 238324208831434331628131715304428889871
q = 296805874594538235115008173244022912163
```


```py
#!/usr/bin/env python3

import gmpy2

# Given values
p = 238324208831434331628131715304428889871
q = 296805874594538235115008173244022912163
n = 70736025239265239976315088690174594021646654881626421461009089480870633400973
e = 3
c = 28822365203577929536184039125870638440692316100772583657817939349051546473185

phi_n = (p - 1) * (q - 1)

d = gmpy2.invert(e, phi_n)
m = gmpy2.powmod(c, d, n)

message = bytearray.fromhex(hex(m)[2:]).decode()

print("Decrypted message:", message)
```

> Rezultat: `small_numbers_are_not_safe`.


## Task 03 | Is this even OTP?

Text initial: **wAyk{mmAwjAuwpzAwmAqjn**.

Pentru codul ASCII 62, adica caracterul `>`, obtin umratorul text: **IGUESSITKINDAISOTP**
(formatat sa fie si human-readable, s-ar rescrie: "I guess it kinda is OTP")


OTP Byte: '>' (ASCII: 62) -> Decrypted Text: IGUESSITKINDAISOTP


```py
def decrypt_one_time_pad(ciphertext):
    ciphertext_bytes = bytes(ciphertext, 'utf-8')
    
    potential_plaintexts = []
    
    for key in range(32, 127):
        decrypted = ''.join(chr(c ^ key) for c in ciphertext_bytes)
        potential_plaintexts.append((chr(key), decrypted))
    
    return potential_plaintexts

ciphertext = "wAyk{mmAwjAuwpzAwmAqjn"
results = decrypt_one_time_pad(ciphertext)

for otp_byte, result in results:
    print(f"OTP Byte: '{otp_byte}' (ASCII: {ord(otp_byte)}) -> Decrypted Text: {result}")
```



## Task 04 | Many Time Pad



## Task 05 

```
Plaintext = Decrypt(Ciphertext) ⊕ IV
Ciphertext = Encrypt(Plaintext) ⊕ IV
```



Known Values:
- Original IV (hex): 7ec00bc6fd663984c1b6c6fd95ceeef1
- Original plaintext: "FIRE_NUKES_MELA!"
- Desired plaintext: "SEND_NUDES_MELA!"

```
Delta = Desired Plaintext ⊕ Original Plaintext
New IV = Delta ⊕ Original IV

```

```sh
$ unzip isc-lab02-oracle.zip
$ ls -al     # Sunt niste fisiere ascunse
$ cd .src/   # Dintre care un folder ascuns :)
```


```sh
$ ./oracle 
(oracle.c, 32): ./oracle hexlify(IV): Success
```

Executabilul asteapta **IV**-ul in CLI.


```sh
# IV initial
$ ./oracle 7ec00bc6fd663984c1b6c6fd95ceeef1
Decrypted text is: FIRE_NUKES_MELA!
```

```sh
# IV alterat
$ ./oracle 6bcc17c7fd66398bc1b6c6fd95ceeef1
Decrypted text is: SEND_NUDES_MELA!
```


🤢🤢🤢🤢
Ce task urat! Vomit...

