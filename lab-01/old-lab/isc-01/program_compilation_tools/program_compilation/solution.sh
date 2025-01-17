#!/bin/bash

# Downloading the following 'program'
wget -O simple.html https://curl.haxx.se/libcurl/c/simple.html

# After so,
# In `VS Code`, open `simple.html` with `Live Server`




# Installing `curl` for C (in Ubuntu)
sudo apt-get install libcurl4-openssl-dev



gcc -o example main_example.c -lcurl
./example > example.html 
# Open the HTML file with `Live Server` in `VS Code`

gcc -o localhost main_localhost.c -lcurl
./localhost > localhost.html
# Open the HTML file with `Live Server` in `VS Code`


