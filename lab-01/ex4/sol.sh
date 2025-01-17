#!/bin/bash

file 04-File
# 04-File: gzip compressed data, was "01-File", last modified: Sun May 14 01:10:24 2017, from Unix, original size modulo 2^32 25

# extracting the archive 04-File
gunzip -c 04-File > resulted-file

cat resulted-file
# ISC{file_is_our_friend}
