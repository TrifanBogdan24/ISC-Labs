#!/bin/bash

sudo apt install binwalk -y

binwalk -e 06-Idea.jpg
binwalk -D='.*' 06-Idea.jpg
cd _06-Idea.jpg.extracted/
7z x 82EF

# See flag4.zip
# Flag obtain: ISC{fileception_is_real}