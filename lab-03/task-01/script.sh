#!/bin/bash

docker pull ghcr.io/cs-pub-ro/isc-auth-pam:latest
mkdir ~/auth-lab
docker run --rm --name auth-lab -v $(pwd)/auth-lab/:/home/hacker/auth-lab -it ghcr.io/cs-pub-ro/isc-auth-pam

# In Docker
wget https://ocw.cs.pub.ro/courses/_media/isc/labs/lab03-pam.zip -O lab03-pam.zip
unzip lab03-pam.zip -d lab03-pam