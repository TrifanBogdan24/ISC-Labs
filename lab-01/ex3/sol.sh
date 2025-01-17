#!/bin/bash

find inhere/ -type f -readable -size 987c ! -executable

for file in $(find inhere/ -type f -readable -size 987c ! -executable) ; do
    cat "$file"
done


# It should obtain: 'ISC{manual-pages-are-your-friends}'