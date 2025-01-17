#!/bin/bash

echo "<YOUR FLAG WAS HERE>" > flag.txt

# Step 1: gzip compression
gzip_file="data2.bin"
gzip -c flag.txt > "$gzip_file"
echo "Created: $gzip_file"

# Step 2: bzip2 compression
bzip2_file="data3.bin"
bzip2 -c "$gzip_file" > "$bzip2_file"
echo "Created: $bzip2_file"

# Step 3: gzip compression again
gzip_file_2="data4.bin"
gzip -c "$bzip2_file" > "$gzip_file_2"
echo "Created: $gzip_file_2"

# Step 4: tar compression
tar_file_1="data5.tar"
tar -cf "$tar_file_1" "$gzip_file_2"
echo "Created: $tar_file_1"

# Step 5: tar compression again
tar_file_2="data6.tar"
tar -cf "$tar_file_2" "$tar_file_1"
echo "Created: $tar_file_2"

# Step 6: bzip2 compression again
bzip2_file_2="data7.bz2"
bzip2 -c "$tar_file_2" > "$bzip2_file_2"
echo "Created: $bzip2_file_2"

# Step 7: tar compression again
tar_file_3="data8.tar"
tar -cf "$tar_file_3" "$bzip2_file_2"
echo "Created: $tar_file_3"

# Step 8: gzip compression for the final step
gzip_file_3="data9.gz"
gzip -c "$tar_file_3" > "$gzip_file_3"
echo "Created: $gzip_file_3"

xxd data9.gz > bin
rm data*

echo "Created bin hexdump file and removed the archives."
