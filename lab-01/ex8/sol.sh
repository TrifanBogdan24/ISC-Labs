#!/bin/bash

# Ne uitam la fisierul 'bin'
# Seamana foarte mult cu 'https://media.descopera.ro/FNtEnEUpiIrzoEfpQFG4YMb9SH0=/610x0/smart/filters:contrast(5):format(webp):quality(80)/https://www.descopera.ro/wp-content/uploads/media/401/321/5106/12367893/2/hieroglife.jpg'

xxd -r bin > copie_bin
file copie_bin 
# Va genera:
# copie_bin: gzip compressed data, was "data8.tar", last modified: Mon Oct  7 06:22:14 2024, from Unix, original size modulo 2^32 10240