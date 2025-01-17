#!/bin/bash

# Displays the whole file with base16 characters


hexdump 05-Corrupted.jpg
cp 05-Corrupted.jpg 05-Corrupted-backup.jpg
cp 05-Corrupted.jpg good-image.jpg

# Step 2: Fix the corrupted SOI (Start of Image) and header issues
# This command replaces the first 4 bytes with the correct SOI and fixes the JFIF marker's endian issue
printf '\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00' | dd conv=notrunc bs=1 seek=0 of=good-image.jpg


# Flag: ISC{no_more_ideas_for_flags}