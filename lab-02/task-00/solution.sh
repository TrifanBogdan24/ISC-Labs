#!/bin/bash

rm -rf isc-lab02-encrypted.zip Image/

wget -O isc-lab02-encrypted.zip https://ocw.cs.pub.ro/courses/_media/isc/labs/isc-lab02-encrypted.zip


unzip isc-lab02-encrypted.zip -d Image/

sudo apt-get install hexedit -y

cd Image
head -c 10 isc-lab02-encrypted.bmp
# �W���D!


ls -alh isc-lab02-encrypted.bmp



cp isc-lab02-encrypted.bmp corrected.bmp


hexedit
# 00000000   98 17 57 CC  FD 1B F0 E9  44 21 22 67  5A A7 51 AF  ..W.....D!"gZ.Q.
# 00000010   23 09 91 2E  8E BE 0A 7F  77 BC AC 5F  39 C8 86 E5  #.......w.._9...
# 00000020   89 6B 0A 6D  E9 F4 56 A7  2D EC D7 A9  AF 16 BB 49  .k.m..V.-......I
# 00000030   6B 64 4A B8  F6 9A 51 0B  D7 80 91 B0  77 E3 EA 93  kdJ...Q.....w...
# 00000040   E5 0A CA E0  59 0A F3 7F  41 FC 54 91  C5 19 4D 32  ....Y...A.T...M2
# 00000050   11 D9 DE FB  AC 62 03 6C  43 55 53 72  2D BB 20 84  .....b.lCUSr-. .






# The online tools is better: https://hexed.it/



# Corrected header: 42 4D 66 CA D7 00 00 00 00 00 36 00 00 00 28 00 00 00 D0 07 00 00 35 09 00 00 01 00 18 00 00 00 00 00 30 CA D7 00 74 12 00 00 74 12 00 00 00 00 00 00 00 00 00 00