#!/bin/bash


rm -f isc-lab02-secret.zip

wget -O isc-lab02-secret.zip https://ocw.cs.pub.ro/courses/_media/isc/labs/isc-lab02-secret.zip


unzip isc-lab02-secret.zip
# Va genera: isc-lab02-secret.enc


# Am scris acest frumusel script Python:
python3 decrypt.py