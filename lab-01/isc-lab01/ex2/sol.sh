#!/usr/bin/env bash

for passwd in $(cat passwords.txt) ; do
    unzip -P "$passwd" crack_me.zip
    exit_code=$?
    if [[ $exit_code == 0 ]] ; then
        echo "Yuppi! Password found: $passwd"
        # The "$passwd" should be "sunshine"
        exit 0
    fi
done


echo "[ERROR] The 'passwords.txt' does NOT contain a valid password!"
exit 1



# In the end, in this scenario, the script optains flag.txt
# ISC{991e7f7d-ac8e-4570-a012-8fb9314b4380}
